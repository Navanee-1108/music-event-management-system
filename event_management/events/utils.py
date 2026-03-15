from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


# ======================================================
# 📩 BOOKING EMAILS (User receipt + Admin notification)
# ======================================================

def send_booking_emails(user_email, booking):

    # ---------------- USER CONFIRMATION MAIL ----------------
    subject = "✅ Event Booking Confirmation - MSD Events"

    text_content = f"""
Hi {booking.name},

Your event booking is confirmed successfully 🎉

Event    : {booking.event.title}
Date     : {booking.event_date}
Location : {booking.location}
Price    : ₹{booking.event.price}

Thank you,
MSD Events Team
"""

    html_content = render_to_string("emails/booking_user.html", {
        "name": booking.name,
        "event": booking.event.title,
        "date": booking.event_date,
        "location": booking.location,
        "price": booking.event.price,
    })

    user_msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email]
    )
    user_msg.attach_alternative(html_content, "text/html")
    user_msg.send()


    # ---------------- ADMIN NOTIFICATION MAIL ----------------
    admin_subject = "📩 New Event Booking Received"

    admin_text = f"""
New Event Booking Received

Name     : {booking.name}
Email    : {booking.email}
Phone    : {booking.phone}

Event    : {booking.event.title}
Date     : {booking.event_date}
Location : {booking.location}
Price    : ₹{booking.event.price}
"""

    admin_html = render_to_string("emails/booking_admin.html", {
        "name": booking.name,
        "email": booking.email,
        "phone": booking.phone,
        "event": booking.event.title,
        "date": booking.event_date,
        "location": booking.location,
        "price": booking.event.price,
    })

    admin_msg = EmailMultiAlternatives(
        subject=admin_subject,
        body=admin_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL]
    )
    admin_msg.attach_alternative(admin_html, "text/html")
    admin_msg.send()


# ======================================================
# 📩 CONTACT FORM EMAIL (Admin only)
# ======================================================

def send_contact_email(contact):

    subject = "📩 New Contact Enquiry - MSD Events"

    text_content = f"""
New Contact Message Received

Name    : {contact.name}
Email   : {contact.email}
Phone   : {contact.phone}

Message:
{contact.message}
"""

    html_content = render_to_string("emails/contact_admin.html", {
        "name": contact.name,
        "email": contact.email,
        "phone": contact.phone,
        "message": contact.message,
    })

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
