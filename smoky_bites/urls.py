from django.urls import path, include
from orders.admin import admin_site

urlpatterns = [
    path("admin/", admin_site.urls),
    path("", include("orders.urls")),
]
