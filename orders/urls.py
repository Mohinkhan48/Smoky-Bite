from django.urls import path
from . import views, views_notifications

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/<str:order_id>/', views.order_success, name='order_success'),
    path('api/latest_order/', views_notifications.get_latest_order_id, name='latest_order_id'),
]
