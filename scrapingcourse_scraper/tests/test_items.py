import unittest
from scrapingcourse_scraper.items import ScrapingcourseScraperItem

class TestScrapingcourseScraperItem(unittest.TestCase):

    def test_scrapingcourse_scraper_item_fields(self):
        # Create an instance of ScrapingcourseScraperItem
        item = ScrapingcourseScraperItem()

        # Set values for each field
        item['city_id'] = 1
        item['hotelName'] = 'Test Hotel'
        item['hotelAddress'] = '123 Test St'
        item['hotelImg'] = 'https://example.com/image.jpg'
        item['price'] = '100.50'
        item['rating'] = '4.5'
        item['roomType'] = 'Single'
        item['lat'] = '40.7128'
        item['lng'] = '-74.0060'

        # Verify that the fields were set correctly
        self.assertEqual(item['city_id'], 1)
        self.assertEqual(item['hotelName'], 'Test Hotel')
        self.assertEqual(item['hotelAddress'], '123 Test St')
        self.assertEqual(item['hotelImg'], 'https://example.com/image.jpg')
        self.assertEqual(item['price'], '100.50')
        self.assertEqual(item['rating'], '4.5')
        self.assertEqual(item['roomType'], 'Single')
        self.assertEqual(item['lat'], '40.7128')
        self.assertEqual(item['lng'], '-74.0060')

    def test_empty_item(self):
        # Create an empty instance of ScrapingcourseScraperItem
        item = ScrapingcourseScraperItem()

        # Verify that the fields are empty by default (None)
        self.assertIsNone(item.get('city_id'))
        self.assertIsNone(item.get('hotelName'))
        self.assertIsNone(item.get('hotelAddress'))
        self.assertIsNone(item.get('hotelImg'))
        self.assertIsNone(item.get('price'))
        self.assertIsNone(item.get('rating'))
        self.assertIsNone(item.get('roomType'))
        self.assertIsNone(item.get('lat'))
        self.assertIsNone(item.get('lng'))

    

if __name__ == '__main__':
    unittest.main()
