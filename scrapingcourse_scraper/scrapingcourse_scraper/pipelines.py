import os
from scrapy import Spider
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from scrapingcourse_scraper.models import Hotel, Base, get_engine_and_session
from PIL import Image
import requests
from io import BytesIO

class ScrapingcourseScraperPipeline:

    def open_spider(self, spider):
        # Initialize database session
        database_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://munne:munne123@postgres:5432/scraping_db")
        self.engine, self.session = get_engine_and_session(database_url)  # Unpack the tuple here

    def close_spider(self, spider):
        # Close database session
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):

        hotel = Hotel(
            city_id=item['city_id'],
            hotel_name=item['hotelName'],
            hotel_address=item['hotelAddress'],
            hotel_img=self.save_image(item['hotelImg'], item['hotelName']),
            price=(item['price']) or None,
            rating=(item['rating']) or None,
            room_type=item['roomType'] or None,
            lat=item['lat'] or None,
            lng=item['lng'] or None,
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
            img_name = f"{hotel_name}_{os.path.basename(img_url)}"
            img_path = os.path.join(img_dir, img_name)
            img.save(img_path)
            return img_path  # Return the image path to store in the database
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
