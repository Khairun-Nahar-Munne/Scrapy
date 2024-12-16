import os
import unittest
import tempfile
import requests
from unittest.mock import patch, MagicMock, mock_open
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PIL import Image
from io import BytesIO

# Import the classes and modules to test
from scrapingcourse_scraper.pipelines import ScrapingcourseScraperPipeline
from scrapingcourse_scraper.models import Base, Hotel

class TestScrapingcourseScraperPipeline(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test method"""
        # Create a temporary SQLite in-memory database
        self.test_engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.test_engine)
        
        # Create a session
        TestSessionLocal = sessionmaker(bind=self.test_engine)
        self.test_session = TestSessionLocal()

        # Create pipeline instance
        self.pipeline = ScrapingcourseScraperPipeline()
        self.pipeline.engine = self.test_engine
        self.pipeline.session = self.test_session

    def tearDown(self):
        """Clean up after each test method"""
        self.test_session.close()

    
    @patch('requests.get')
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    def test_save_image_successful(self, mock_makedirs, mock_exists, mock_requests_get):
        """Test save_image method with a successful image download"""
        # Create a mock image
        mock_img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = BytesIO()
        mock_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Setup mocks
        mock_response = MagicMock()
        mock_response.content = img_byte_arr
        mock_requests_get.return_value = mock_response

        # Test image saving
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('os.path.join', return_value=os.path.join(tmpdir, 'test_hotel_image.png')):
                result = self.pipeline.save_image('http://example.com/image.png', 'Test Hotel')
                
                # Verify
                self.assertTrue(os.path.exists(result))
                mock_requests_get.assert_called_once_with('http://example.com/image.png')

    def test_save_image_error_handling(self):
        """Test save_image method error handling"""
        # Simulate a request exception
        with patch('requests.get', side_effect=requests.RequestException):
            result = self.pipeline.save_image('http://example.com/image.png', 'Test Hotel')
            self.assertIsNone(result)

    def test_process_item_creates_hotel_record(self):
        """Test process_item method creates a Hotel record"""
        # Prepare test item
        test_item = {
            'city_id': 1,
            'hotelName': 'Test Hotel',
            'hotelAddress': '123 Test St',
            'hotelImg': 'http://example.com/image.png',
            'price': '100.50',
            'rating': '4.5',
            'roomType': 'Standard',
            'lat': '40.7128',
            'lng': '-74.0060'
        }

        # Mock image saving
        with patch.object(self.pipeline, 'save_image', return_value='test_image_path.jpg'):
            # Process the item
            processed_item = self.pipeline.process_item(test_item, None)

            # Verify the item was processed
            self.assertEqual(processed_item, test_item)

            # Check database record
            hotels = self.test_session.query(Hotel).all()
            self.assertEqual(len(hotels), 1)
            hotel = hotels[0]
            
            # Verify hotel details
            self.assertEqual(hotel.hotel_name, 'Test Hotel')
            self.assertEqual(hotel.price, 100.50)
            self.assertEqual(hotel.rating, 4.5)

if __name__ == '__main__':
    unittest.main()