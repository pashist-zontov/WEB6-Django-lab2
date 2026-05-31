from django.shortcuts import render, redirect, get_object_or_404
# Prefetch - для оптимизации связи N:N
from django.db.models import Prefetch, Count
from django.db import transaction
from django.utils import timezone
from .models import Carts, Products, Customers, CartsProducts
from django.core.paginator import Paginator

def carts_list(request):
    context = {
        'carts': Carts.objects.select_related("customer").prefetch_related(
        Prefetch("products", queryset=CartsProducts.objects.select_related("product"))
        ).annotate(items_count=Count("products"))
    }

    return render(request, 'carts/carts_list.html', context)

def index(request):
    products = Products.objects.all().order_by('name')
    paginator = Paginator(products, 10) # 10 товаров на страницу
    page_num = request.GET.get('page')
    products = paginator.get_page(page_num) # Интересный факт: объект paginator - итерируемый объект, такой же, как и QuerySet-"products"

    context = {
        'title' : "Главная",
        'products': products,
    }

    return render(request, 'store/index.html', context)

def add_to_cart(request):
    customer_id = request.POST.get('customer_id') or request.GET.get('customer_id')
    product_id = request.POST.get('product_id') or request.GET.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    if not (customer_id and product_id):
        return redirect('store:index') # Перенаправление в основной адрес при отсутствии либо того, либо другого
    
    customer = get_object_or_404(Customers, id=customer_id)
    product = get_object_or_404(Customers, id=customer_id)
    
    # Всё или ничего
    with transaction.atomic():
        cart, created = Carts.objects.get_or_create(
            customer=customer,
            status='Active',
            defaults={'created_at': timezone.now(), 'updated_at': timezone.now()}
        )

        item, item_created = CartsProducts.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not item_created:
            item.quantity += quantity
            item.save()
    
    return redirect('store:cart_detail', cart_id=cart.id)

def cart_detail(request, cart_id):
    cart = get_object_or_404(
        Carts.objects.select_related('customer').prefetch_related('products__product'),
        id=cart_id
    )

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)

        product = get_object_or_404(Products, id=product_id)

        item, created = CartsProducts.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        
        cart.updated_at = timezone.now()
        cart.save(update_fields=['updated_at'])
        return redirect('store:cart_detail', cart_id=cart.id)
    
    context = {
        'cart': cart,
        'products': Products.objects.all().order_by('name')
    }

    return render(request, 'carts/cart_detail.html', context)