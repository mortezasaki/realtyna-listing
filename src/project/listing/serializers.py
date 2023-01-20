from rest_framework import serializers

from .models import Booking, Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    listing = serializers.HyperlinkedIdentityField(view_name='listing:listing-detail')
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = ('id', 'name', 'start_date', 'end_date', 'total_price', 'listing')
