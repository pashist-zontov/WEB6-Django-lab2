from django.shortcuts import render
# Prefetch - для оптимизации связи N:N
from django.db.models import Prefetch, Count
from .models import Carts, CartsProducts

def carts_list(request):
    context = {
        'carts': Carts.objects.select_related("customer").prefetch_related(
        Prefetch("products", queryset=CartsProducts.objects.select_related("product"))
        ).annotate(items_count=Count("products"))
    }

    return render(request, 'store/cart_list.html', context)
