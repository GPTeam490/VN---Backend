import unittest
from unittest.mock import patch
from flask_testing import TestCase
from flask import Flask
from app import app, generate_itinerary


class FlaskAppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')

    @patch('app.model.generate_content')
    def test_generate_itinerary_function(self, mock_generate_content):
        mock_response = type('MockResponse', (object,), {'text': 'Visit the Eiffel Tower in Paris.'})()
        mock_generate_content.return_value = mock_response

        days = 3
        location = 'Paris'
        month = 'June'
        itinerary = generate_itinerary(days, location, month)

        self.assertTrue(isinstance(itinerary, str))
        self.assertIn('Paris', itinerary)
        self.assertIn('Eiffel Tower', itinerary)

    @patch('app.model.generate_content')
    def test_generate_route(self, mock_generate_content):
        mock_response = type('MockResponse', (object,), {'text': 'Visit the Eiffel Tower in Paris.'})()
        mock_generate_content.return_value = mock_response

        response = self.client.post('/generate', data={
            'city': 'Paris',
            'month': 'June',
            'duration': '3'
        })

        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')
        self.assertIn(b'Paris', response.data)
        self.assertIn(b'Eiffel Tower', response.data)


if __name__ == '__main__':
    unittest.main()


