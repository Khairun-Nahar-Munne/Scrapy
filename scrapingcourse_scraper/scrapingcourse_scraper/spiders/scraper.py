import scrapy
import json
import re
import random

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB"]

    def parse(self, response):
        # Extract the script tag containing "window.IBU_HOTEL"
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()
        if ibu_hotel_data:
            # Use regex to extract the JSON-like data within "window.IBU_HOTEL"
            match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', ibu_hotel_data, re.DOTALL)
            if match:
                json_data = match.group(1)
                try:
                    # Parse the JSON data
                    parsed_data = json.loads(json_data)
                    # Extract "htlsData"
                    htls_data = parsed_data.get("initData", {}).get("htlsData", {})

                    # Extract both inboundCities and outboundCities
                    inbound_cities = htls_data.get("inboundCities", [])
                    outbound_cities = htls_data.get("outboundCities", [])

                    # Randomly select between inboundCities and outboundCities
                    city_type = random.choice(["inboundCities", "outboundCities"])
                    selected_cities = inbound_cities if city_type == "inboundCities" else outbound_cities

                    if selected_cities:
                        # Select 3 cities randomly from the list
                        selected_cities = random.sample(selected_cities, min(3, len(selected_cities)))
                        for selected_city in selected_cities:
                            city_id = selected_city.get("id")
                            if city_id:
                                city_url = f"https://uk.trip.com/hotels/list?city={city_id}"
                                self.logger.info(f"Selected city: {selected_city.get('name')} with ID: {city_id}")
                                # Fetch data from the selected city's URL
                                yield scrapy.Request(city_url, callback=self.parse_city_data, meta={"city_id": city_id})
                    else:
                        self.logger.warning(f"No data found in '{city_type}'")

                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to decode JSON: {e}")

    def parse_city_data(self, response):
        # Extract the script tag containing "window.IBU_HOTEL"
        ibu_hotel_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()
        if ibu_hotel_data:
            # Use regex to extract the JSON-like data within "window.IBU_HOTEL"
            match = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', ibu_hotel_data, re.DOTALL)
            if match:
                json_data = match.group(1)
                try:
                    # Parse the JSON data
                    parsed_data = json.loads(json_data)
                    # Extract the "initData" field from "ibu_hotel_data"
                    init_data = parsed_data.get("initData", {})

                    # Extract "firstPageList" and "hotelList"
                    first_page_list = init_data.get("firstPageList", {})
                    hotel_list = first_page_list.get("hotelList", [])

                    for hotel in hotel_list:
                        # Extract only the required fields
                        hotel_basic_info = hotel.get("hotelBasicInfo", {})
                        hotel_name = hotel_basic_info.get("hotelName")
                        hotel_address = hotel_basic_info.get("hotelAddress")
                        hotel_img = hotel_basic_info.get("hotelImg")
                        price = hotel_basic_info.get("price")

                        # Extract comment score
                        comment_info = hotel.get("commentInfo", {})
                        comment_score = comment_info.get("commentScore")

                        # Extract room info (physical room name)
                        room_info = hotel.get("roomInfo", {})
                        physical_room_name = room_info.get("physicalRoomName")

                        # Extract position info (latitude and longitude)
                        position_info = hotel.get("positionInfo", {})
                        coordinate = position_info.get("coordinate", {})
                        lat = coordinate.get("lat")
                        lng = coordinate.get("lng")

                        yield {
                            "city_id": response.meta["city_id"],
                            "hotelName": hotel_name,
                            "hotelAddress": hotel_address,
                            "hotelImg": hotel_img,
                            "price": price,
                            "commentScore": comment_score,
                            "physicalRoomName": physical_room_name,
                            "lat": lat,
                            "lng": lng
                        }

                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to decode JSON for city {response.meta['city_id']}: {e}")
