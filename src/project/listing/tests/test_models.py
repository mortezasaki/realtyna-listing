from datetime import datetime, timedelta

from django.test import TestCase

from ..models import Booking, Listing


class BookingTestCase(TestCase):
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

        Booking.objects.create(
            listing=Listing.objects.get(title='Test Listing'),
            name='Test Name',
            start_date=datetime.now().date() + timedelta(days=1),
            end_date=datetime.now().date() + timedelta(days=3),
        )

    def test_get_total_price(self):
        booking = Booking.objects.get(name='Test Name')
        self.assertEqual(booking.get_total_price, 200.00)

    def test_reserved_for_yesterday(self):
        try:
            Booking.objects.create(
                listing=Listing.objects.get(title='Test Listing'),
                name='Test Name',
                start_date=datetime.now().date() - timedelta(days=1),
                end_date=datetime.now().date() + timedelta(days=3),
            )
            self.fail('Booking created for yesterday')
        except ValueError:
            self.assertTrue(True)

    def test_end_date_less_than_start_date(self):
        try:
            Booking.objects.create(
                listing=Listing.objects.get(title='Test Listing'),
                name='Test Name',
                start_date=datetime.now().date() + timedelta(days=3),
                end_date=datetime.now().date() + timedelta(days=1),
            )
            self.fail('Booking created with end date less than start date')
        except ValueError:
            self.assertTrue(True)

    def test_days_reserved(self):
        booking = Booking.objects.get(name='Test Name')
        self.assertEqual(booking.get_days, 2)

    def test_prevent_reserve_day_reserved(self):
        try:
            Booking.objects.create(
                listing=Listing.objects.get(title='Test Listing'),
                name='Test Name',
                start_date=datetime.now().date() + timedelta(days=2),
                end_date=datetime.now().date() + timedelta(days=3),
            )
            self.fail('Booking created for day reserved')
        except ValueError:
            self.assertTrue(True)
