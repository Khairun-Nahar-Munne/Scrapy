import os
from scrapy import Spider
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scrapingcourse_scraper.models import Hotel, Base, engine
from PIL import Image
import requests
from io import BytesIO

class ScrapingcourseScraperPipeline:

    def __init__(self):
         self.Session = sessionmaker(bind=engine)
         

    def open_spider(self, spider):
        self.session = self.Session()

    def close_spider(self, spider):
        if self.session:
            self.session.commit()
            self.session.close()

    def process_item(self, item, spider):
    # Convert empty strings to None for numeric fields
        def convert_to_numeric(value):
            if value == '' or value is None:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None 
        hotel = Hotel(
            city_id=item['city_id'],
            hotel_name=item['hotelName'],
            hotel_address=item['hotelAddress'],
            hotel_img=self.save_image(item['hotelImg'], item['hotelName']),
            price=convert_to_numeric(item['price']),
            rating=convert_to_numeric(item['rating']),
            room_type=item['roomType'] or None,
            lat=convert_to_numeric(item['lat']),
            lng=convert_to_numeric(item['lng'])
        )
        self.session.add(hotel)
        return item

    def save_image(self, img_url, hotel_name):
        try:
            # Ensure the images directory exists
            img_dir = "images"
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)

            # Download the image
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            img_name = f"{hotel_name.replace(' ', '_')}.jpg"
            img_path = os.path.join(img_dir, img_name)
            img.save(img_path)
            return img_path
        except Exception as e:
            Spider.logger.error(f"Failed to download image {img_url}: {e}")
            return None

