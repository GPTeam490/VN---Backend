import unittest
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

    def test_generate_itinerary_function(self):
        days = 3
        location = 'Paris'
        month = 'June'
        itinerary = generate_itinerary(days, location, month)
        self.assertTrue(isinstance(itinerary, str))
        self.assertIn('Paris', itinerary)
        self.assertIn('Eiffel Tower', itinerary)

    def test_generate_route(self):
        response = self.client.post('/generate', data={
            'days': '3',
            'location': 'Paris',
            'month': 'June'
        })
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('index.html')
        self.assertIn(b'Eiffel Tower', response.data)

if __name__ == '__main__':
    unittest.main()

