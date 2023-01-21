from datetime import datetime, timedelta

from django.test import Client, TestCase

from ..models import Booking, Listing

csrf_client = Client(enforce_csrf_checks=True)


class ListingTestCase(TestCase):
    def setUp(self):
        Listing.objects.create(
            title='Test Listing',
            description='Test Description',
            address='Test Address',
            city='Test City',
            state='Test State',
            bedrooms=1,
            bathrooms=1,
            sqft=100,
            price=100.00,
            is_published=True,
        )

    def test_create_listing(self):
        response = csrf_client.post(
            '/api/listings/',
            {
                'title': 'Test Post Listing',
                'description': 'Test Description',
                'address': 'Test Address',
                'city': 'Test City',
                'state': 'Test State',
                'bedrooms': 1,
                'bathrooms': 1,
                'sqft': 100,
                'price': 100.00,
                'is_published': True,
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_create_booking(self):
        response = csrf_client.post(
            f'/api/listings/{Listing.objects.get(title="Test Listing").id}/reserve/',
            {
                'name': 'Test Name',
                'start_date': datetime.now().date() + timedelta(days=1),
                'end_date': datetime.now().date() + timedelta(days=3),
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_get_listing(self):
        response = csrf_client.get(
            f'/api/listings/{Listing.objects.get(title="Test Listing").id}/'
        )
        self.assertEqual(response.status_code, 200)
