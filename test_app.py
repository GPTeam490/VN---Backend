import unittest
from unittest.mock import patch
from flask_testing import TestCase
from app import app, generate_itinerary

#Source I Used:
#Flask Testing: https://pythonhosted.org/Flask-Testing/

class FlaskAppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    # Asserts index page
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    # Asserts our team page
    def test_ourteam_page(self):
        response = self.client.get('/ourteam')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('ourteam.html')

    @patch('app.model.generate_content')
    def test_generate_itinerary_route_and_function(self, mock_generate_content):
        mock_response = type('MockResponse', (object,), {'text': 'Visit the Pyramids in Egypt.'})()
        mock_generate_content.return_value = mock_response

        days = 3
        location = 'Egypt'
        month = 'June'
        itinerary = generate_itinerary(days, location, month)

        self.assertTrue(isinstance(itinerary, str))
        self.assertIn('Egypt', itinerary)
        self.assertIn('Pyramids', itinerary)

        response = self.client.post('/generate', data={
            'city': 'Egypt',
            'month': 'August',
            'duration': '3'
        })

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')
        self.assertIn(b'Egypt', response.data)
        self.assertIn(b'Pyramids', response.data)


if __name__ == '__main__':
    unittest.main()


