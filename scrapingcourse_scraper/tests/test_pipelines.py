import unittest
from unittest import mock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scrapingcourse_scraper.pipelines import ScrapingcourseScraperPipeline
from scrapingcourse_scraper.models import Hotel, Base, engine
import os

class TestScrapingcourseScraperPipeline(unittest.TestCase):

    def setUp(self):
        # Setup an in-memory SQLite database for testing
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

        # Initialize pipeline and mock database session
        self.pipeline = ScrapingcourseScraperPipeline()
        self.pipeline.session = self.session

        # Create tables for Hotel model
        Base.metadata.create_all(engine)

    def tearDown(self):
        # Close the database session and dispose of the engine
        self.session.close()
        engine.dispose()
        if os.path.exists('images'):
            os.rmdir('images')  # Clean up the images directory if created

    @mock.patch('scrapingcourse_scraper.pipelines.ScrapingcourseScraperPipeline.save_image')
    def test_process_item(self, mock_save_image):
        # Mock save_image method
        mock_save_image.return_value = 'images/mock_image.jpg'

        # Setup an item that the pipeline will process
        item = {
            'city_id': 1,
            'hotelName': 'Test Hotel',
            'hotelAddress': '123 Test St',
            'hotelImg': 'https://example.com/image.jpg',
            'price': '100.50',
            'rating': '4.5',
            'roomType': 'Single',
            'lat': '40.7128',
            'lng': '-74.0060'
        }

        # Call the process_item method
        processed_item = self.pipeline.process_item(item, None)

        # Check if the save_image method was called correctly
        mock_save_image.assert_called_once_with(item['hotelImg'], item['hotelName'])

        # Verify the processed item
        self.assertIsNotNone(processed_item)

    def test_convert_to_numeric(self):
        # Instantiate the pipeline
        pipeline = ScrapingcourseScraperPipeline()

        # Get the convert_to_numeric function
        convert_to_numeric = pipeline.process_item(None, None)

        # Test empty string conversion
        self.assertIsNone(convert_to_numeric(''))

        # Test valid numeric conversion
        self.assertEqual(convert_to_numeric('100.50'), 100.50)

        # Test invalid numeric conversion
        self.assertIsNone(convert_to_numeric('not a number'))

    @mock.patch('scrapy.pipelines.images.Pipeline.save_image')
    def test_save_image(self, mock_save_image):
        # Test the image saving method
        mock_save_image.return_value = 'images/Test_Hotel.jpg'

        result = mock_save_image(
            'https://www.w3schools.com/html/img_girl.jpg',
            'Test Hotel'
        )

        # Check the returned path
        self.assertTrue(result.endswith('Test_Hotel.jpg'))
        self.assertTrue(result.startswith('images/'))

    @mock.patch('scrapingcourse_scraper.pipelines.ScrapingcourseScraperPipeline.save_image')
    def test_save_image_error_handling(self, mock_save_image):
        # Simulate an error in the image saving method
        mock_save_image.side_effect = Exception('Failed to save image')

        result = mock_save_image(
            'https://www.w3schools.com/html/img_girl.jpg',
            'Test Hotel'
        )

        # The result should be None since the image could not be saved
        self.assertIsNone(result)

    def test_directory_creation_for_images(self):
        # Test if images directory is created if it doesn't exist
        if os.path.exists('images'):
            os.rmdir('images')  # Clean up if directory exists

        pipeline = ScrapingcourseScraperPipeline()
        pipeline.save_image('https://www.w3schools.com/html/img_girl.jpg', 'Test Hotel')

        # Check if 'images' directory was created
        self.assertTrue(os.path.exists('images'))

        # Clean up the created directory
        os.rmdir('images')

if __name__ == '__main__':
    unittest.main()