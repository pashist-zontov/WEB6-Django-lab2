from django.urls import path, include
from . import views

app_name = "store"
urlpatterns = [
    path('', views.index, name='index'), # <-- страница по умолчанию
    path('carts/', views.carts_list, name='carts_list'),
]