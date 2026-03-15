from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    duration = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to='event_images/')

    is_active = models.BooleanField(default=True)

    def _str_(self):
        return self.title

class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=200)

    event_date = models.DateField()
    booked_on = models.DateTimeField(auto_now_add=True)

    # ✅ NEW FIELD (SAFE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    class Meta:
        unique_together = ('event', 'event_date')

    def __str__(self):
        return f"{self.event.title} - {self.event_date}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
