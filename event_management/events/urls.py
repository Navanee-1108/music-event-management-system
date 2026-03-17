from django.urls import path
from . import views

urlpatterns = [

    # USER SIDE
    path("", views.home, name="home"),
    path("events/", views.event_list, name="event_list"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("book/<int:event_id>/", views.book_event, name="book_event"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("contact/", views.contact, name="contact"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # ADMIN SIDE (CUSTOM)
    path("admin-login/", views.admin_login, name="admin_login"),


    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-panel/add-service/", views.admin_add_service, name="admin_add_service"),
    path("admin-panel/customer-bookings/", views.admin_customer_bookings, name="admin_customer_bookings"),
    path("admin-panel/accept-booking/<int:booking_id>/", views.admin_accept_booking, name="admin_accept_booking"),
    path('admin-panel/edit-service/<int:event_id>/', views.admin_edit_service, name='admin_edit_service'),
    path('admin-panel/edit-services/', views.admin_edit_services, name='admin_edit_services'),
    path('admin-panel/toggle-service/<int:event_id>/', views.admin_toggle_service, name='admin_toggle_service'),
    path("admin-panel/users/", views.admin_users, name="admin_users"),
    path("admin-forgot-password/", views.admin_forgot_password, name="admin_forgot_password"),

    path("admin-logout/", views.admin_logout, name="admin_logout"),
]
