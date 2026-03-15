from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from events import views
from events.admin import msd_admin_site

urlpatterns = [
    # ✅ CUSTOM ADMIN
    path("admin/", msd_admin_site.urls),

    # AUTH
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # EVENTS APP
    path("", include("events.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
