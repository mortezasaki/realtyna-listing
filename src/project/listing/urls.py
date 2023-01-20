from django.urls import include, path
from rest_framework import routers

from .api import BookingViewSet, ListingView

app_name = 'listing'

router = routers.DefaultRouter()
router.register(r'listings', ListingView)
router.register(
    r'listings/(?P<listing_id>[0-9]+)/reserve', BookingViewSet, basename='bookings'
)
router.register(
    r'listings/(?P<listing_id>[0-9]+)/reserve/(?P<reserve_id>[0-9]+)/',
    BookingViewSet,
    basename='bookings',
)

urlpatterns = [path('', include(router.urls))]
