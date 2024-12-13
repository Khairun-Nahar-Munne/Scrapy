# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Hotel
from PIL import Image
import requests
from io import BytesIO

class ScrapingcourseScraperPipeline:

    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def open_spider(self, spider):
        self.session = self.Session()

    def close_spider(self, spider):
        if self.session:
            self.session.commit()
            self.session.close()

    def process_item(self, item, spider):
        hotel = Hotel(
            city_id=item['city_id'],
            hotel_name=item['hotelName'],
            hotel_address=item['hotelAddress'],
            hotel_img=self.save_image(item['hotelImg'], item['hotelName']),
            price=item['price'],
            comment_score=item['commentScore'],
            physical_room_name=item['physicalRoomName'],
            lat=item['lat'],
            lng=item['lng']
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
            spider.logger.error(f"Failed to download image {img_url}: {e}")
            return None

