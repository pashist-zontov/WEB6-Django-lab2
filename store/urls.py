from django.urls import path, include
from . import views

app_name = "store"
urlpatterns = [
    path('', views.index, name='index'), # <-- страница по умолчанию
    path('carts/', views.carts_list, name='carts_list'),
    path('carts/<int:cart_id>/', views.cart_detail, name='cart_detail'),
    path('carts/add/', views.add_to_cart, name='add_to_cart'),
    path('carts/<int:cart_id>/remove/<int:product_id>', views.remove_from_cart, name='remove_from_cart') # Вьюха для удаления
]