import unittest
from scrapingcourse_scraper.models import Hotel  # Import Hotel class from your SQLAlchemy model file

class TestHotelModel(unittest.TestCase):
    def test_hotel_model_creation(self):
        # Create a test hotel instance using SQLAlchemy model
        hotel = Hotel(
            city_id=123,
            hotel_name='Test Hotel',
            hotel_address='123 Test St',
            hotel_img='images/Imperial_Lexis_Kuala_Lumpur.jpg',
            price=100.50,
            rating=4.5,
            room_type='Standard',
            lat=40.7128,
            lng=-74.0060
        )
        
        # Test attribute setting
        self.assertEqual(hotel.city_id, 123)
        self.assertEqual(hotel.hotel_name, 'Test Hotel')
        self.assertEqual(hotel.hotel_address, '123 Test St')
        self.assertEqual(hotel.hotel_img, 'images/Imperial_Lexis_Kuala_Lumpur.jpg')
        self.assertEqual(hotel.price, 100.50)
        self.assertEqual(hotel.rating, 4.5)
        self.assertEqual(hotel.room_type, 'Standard')
        self.assertEqual(hotel.lat, 40.7128)
        self.assertEqual(hotel.lng, -74.0060)
    
    def test_hotel_model_repr(self):
        # Test the __repr__ method
        hotel = Hotel(
            city_id=123,
            hotel_name='Test Hotel',
            hotel_address='123 Test St',
            hotel_img='images/Imperial_Lexis_Kuala_Lumpur.jpg'
        )
        
        expected_repr = "<Hotel(name=Test Hotel, city_id=123)>"
        self.assertEqual(repr(hotel), expected_repr)

if __name__ == '__main__':
    unittest.main()
