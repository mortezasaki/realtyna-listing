from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Booking, Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'address',
        'city',
        'state',
        'bedrooms',
        'bathrooms',
        'sqft',
        'price',
        'is_published',
        'created_at',
        'updated_at',
    )
    list_display_links = ('title',)
    list_filter = ('city', 'state', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'address', 'city', 'state', 'price')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'link_to_listing',
        'name',
        'start_date',
        'end_date',
        'total_price',
        'created_at',
    )
    list_display_links = ('name',)
    list_filter = ('listing', 'start_date')
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25

    def link_to_listing(self, obj):
        link = reverse("admin:listing_listing_change", args=[obj.listing.id])
        return format_html(f'<a href="{link}">{obj.listing.title}</a>')
