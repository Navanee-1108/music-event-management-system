from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User

from .models import Event, Booking, Contact


class MSDAdminSite(AdminSite):
    site_header = "MSD Events – Admin"
    site_title = "MSD Events Admin"
    index_title = "Admin Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context["total_events"] = Event.objects.count()
        extra_context["total_bookings"] = Booking.objects.count()
        extra_context["total_customers"] = User.objects.count()

        return super().index(request, extra_context)


# create admin site
msd_admin_site = MSDAdminSite(name="msd_admin")


# EVENT ADMIN
@admin.register(Event, site=msd_admin_site)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "duration", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)


# BOOKING ADMIN
@admin.register(Booking, site=msd_admin_site)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "name",
        "phone",
        "event_date",
        "location",
        "booked_on",
    )
    list_filter = ("event", "event_date")
    search_fields = ("name", "phone", "email")


# CONTACT ADMIN
@admin.register(Contact, site=msd_admin_site)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")