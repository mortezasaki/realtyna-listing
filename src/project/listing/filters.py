from django_filters import FilterSet, filters

from .models import Booking, Listing


class ListingFitler(FilterSet):
    price = filters.RangeFilter()

    class Meta:
        model = Listing
        fields = ['city', 'state', 'bedrooms', 'bathrooms', 'price', 'is_published']


class BookingFilter(FilterSet):
    start_date = filters.DateFromToRangeFilter(label='Date range')

    class Meta:
        model = Booking
        fields = ['listing', 'start_date']
