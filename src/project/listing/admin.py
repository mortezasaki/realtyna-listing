from django.contrib import admin

from .models import Booking, Listing

admin.site.register(Listing)
admin.site.register(Booking)
