import os
from datetime import datetime
from uuid import uuid4

from django.db import models


def get_file_path(instance, filename):
    """
    To avoid name collision, we generate a new name for the image
    """
    ext = filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("images", filename)


class Listing(models.Model):
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    sqft = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_reserved(self, date):
        bookings = self.bookings.filter(start_date__lte=date, end_date__gte=date)
        return len(bookings) == 0

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]


class Booking(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bookings"
    )
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.listing.price * self.get_days

    @property
    def get_days(self):
        return (self.end_date - self.start_date).days

    def save(self, *args, **kwargs):
        if self.start_date > self.end_date:
            raise ValueError("Start date must be less than end date")

        if self.start_date < datetime.now().date():
            raise ValueError("Start date must be greater than today")

        # Check if listing does not reserved for the given dates
        if not self.listing.get_reserved(
            self.start_date
        ) or not self.listing.get_reserved(self.end_date):
            raise ValueError("Listing is not available for the given dates")

        self.total_price = self.get_total_price
        super(Booking, self).save(*args, **kwargs)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.listing.title} - {self.start_date} - {self.end_date}"
