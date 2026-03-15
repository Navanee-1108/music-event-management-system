from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Event, Booking, Contact
from .utils import send_booking_emails, send_contact_email
from django.contrib.admin.views.decorators import staff_member_required




def login_view(request):
    next_url = request.GET.get("next")  
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)

            if next_url:
                return redirect(next_url)

            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "auth/login.html")



def register_view(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        p1 = request.POST.get("password1")
        p2 = request.POST.get("password2")

        if p1 != p2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        User.objects.create_user(
            username=email,
            email=email,
            password=p1,
            first_name=name
        )

        messages.success(request, "Registered successfully")
        return redirect("login")

    return render(request, "auth/register.html")


def logout_view(request):
    logout(request)
    return redirect("home")



def home(request):
    return render(request, "events/home.html")


def event_list(request):
    events = Event.objects.filter(is_active=True)
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    return render(request, "events/event_detail.html", {"event": event})


@login_required(login_url="login")
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event_date = date.fromisoformat(request.POST.get("event_date"))

        if event_date < date.today():
            messages.error(request, "Past dates not allowed")
            return redirect("book_event", event_id=event.id)

        if Booking.objects.filter(event=event, event_date=event_date).exists():
            messages.error(request, "Already booked")
            return redirect("book_event", event_id=event.id)

        booking = Booking.objects.create(
            user=request.user,
            event=event,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            location=request.POST.get("location"),
            event_date=event_date
        )

        send_booking_emails(booking.email, booking)
        messages.success(request,"Booking successful! Confirmation email has been sent. ")


    return render(request, "events/book_event.html", {"event": event})


def contact(request):
    if request.method == "POST":
        contact = Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message")
        )
        send_contact_email(contact)
        messages.success(request, "Message sent successfully! Our team will contact you shortly.")

    return render(request, "events/contact.html")


@login_required(login_url="login")
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-booked_on")

    return render(request, "events/my_bookings.html", {
        "bookings": bookings
    })




def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, "custom_admin/login.html")


@login_required(login_url="admin_login")
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("admin_login")

    context = {
        "total_events": Event.objects.count(),
        "total_customers": Booking.objects.values("email").distinct().count(),
        "total_bookings": Booking.objects.count(),
    }

    return render(request, "custom_admin/dashboard.html", context)


@login_required(login_url="admin_login")
def admin_add_service(request):
    if not request.user.is_staff:
        return redirect("admin_login")

    if request.method == "POST":
        Event.objects.create(
        title=request.POST.get("title"),
        description=request.POST.get("description"),
        duration=request.POST.get("duration"),
        price=request.POST.get("price"),
        image=request.FILES.get("image"),
        )
        messages.success(request, "Service added successfully")
        return redirect("admin_add_service")

    return render(request, "custom_admin/add_service.html")


@login_required(login_url="admin_login")
def admin_customer_bookings(request):
    if not request.user.is_staff:
        return redirect("admin_login")

    bookings = Booking.objects.all().order_by("-booked_on")  # OLD → NEW order

    return render(request, "custom_admin/customer_bookings.html", {
        "bookings": bookings
    })
@login_required(login_url="admin_login")

@login_required(login_url="admin_login")
def admin_accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = "accepted"
    booking.save()
    return redirect("admin_customer_bookings")






def admin_logout(request):
    logout(request)
    return redirect("admin_login")





@staff_member_required(login_url="admin_login")
def admin_edit_services(request):
    events = Event.objects.all().order_by("-id")
    return render(
        request,
        "custom_admin/edit_services.html",
        {"events": events}
    )


@staff_member_required(login_url="admin_login")
def admin_edit_service(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.title = request.POST.get("title")
        event.event_type = request.POST.get("event_type")
        event.short_description = request.POST.get("short_description")
        event.description = request.POST.get("description")
        event.duration = request.POST.get("duration")
        event.price = request.POST.get("price")

        if request.FILES.get("image"):
            event.image = request.FILES.get("image")

        event.save()
        messages.success(request, "Service updated successfully")
        return redirect("admin_edit_services")

    return render(
        request,
        "custom_admin/edit_service_form.html",
        {"event": event}
    )


@staff_member_required(login_url="admin_login")
def admin_toggle_service(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.is_active = not event.is_active
    event.save()
    return redirect("admin_edit_services")

@login_required(login_url="admin_login")
def admin_users(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "custom_admin/users.html", {
        "users": users
    })
    
    

def admin_register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Admin username already exists")
            return render(request, "custom_admin/register_admin.html")

        # create admin
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True
        )

        messages.success(request, "Admin created successfully. Please login.")
        return redirect("admin_login")

    return render(request, "custom_admin/register_admin.html")
