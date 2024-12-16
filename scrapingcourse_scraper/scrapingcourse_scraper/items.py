# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapingcourseScraperItem(scrapy.Item):
    city_id = scrapy.Field()
    hotelName = scrapy.Field()
    hotelAddress = scrapy.Field()
    hotelImg = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()  # Updated field
    roomType = scrapy.Field()  # Updated field
    lat = scrapy.Field()
    lng = scrapy.Field()
