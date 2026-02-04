from django.urls import path, include
from orders.admin import admin_site

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin_site.urls),
    path("", include("orders.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
