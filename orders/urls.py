from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/<str:order_id>/', views.order_success, name='order_success'),
]
