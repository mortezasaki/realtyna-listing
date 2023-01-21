from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from .filters import BookingFilter, ListingFitler
from .models import Booking, Listing
from .serializers import BookingSerializer, ListingSerializer


class ListingView(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filterset_class = ListingFitler


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    filterset_class = BookingFilter

    def get_queryset(self):
        listing_id = self.kwargs.get('listing_id')
        listing = get_object_or_404(Listing, id=listing_id)

        reserve_id = self.kwargs.get('reserve_id')
        if reserve_id is not None:
            reserve = get_object_or_404(Booking, id=reserve_id)
            return Booking.objects.filter(id=reserve.id)
        return Booking.objects.filter(listing=listing)

    def perform_create(self, serializer):
        listing_id = self.kwargs.get('listing_id')
        listing = get_object_or_404(Listing, id=listing_id)
        serializer.validated_data['listing'] = listing
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.media_type == 'text/html':
            reservations = list(self.get_queryset())
            return render(
                request, 'listing/reservations.html', {'reservations': reservations}
            )
        return super().list(request, *args, **kwargs)
