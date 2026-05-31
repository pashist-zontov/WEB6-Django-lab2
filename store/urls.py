from django.urls import path, include
from . import views

app_name = "store"
urlpatterns = [
    path('', views.index, name='index'), # <-- страница по умолчанию
    path('carts/', views.carts_list, name='carts_list'),
    path('carts/<int:cart_id>/', views.cart_detail, name='cart_detail'),
    path('carts/add/', views.add_to_cart, name='add_to_cart')
]