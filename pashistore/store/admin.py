from django.contrib import admin
from .models import Products, Carts, Customers, CartsProducts
from django.db.models import Min, Max

# Возникла идея использовать ползунки как фильтр цены товара, но не удалось
# class NumericSlider()

class CartsProductsInline(admin.TabularInline):
    model = CartsProducts
    extra = 1

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at', 'updated_at', 'products_amount_display')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name', "customer__email", "customer__phone")
    inlines = [CartsProductsInline]
    readonly_fields = ("created_at", "updated_at")

    def products_amount_display(self, obj):
        return obj.products_amount()
    products_amount_display.short_description = "Число товаров"

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')
    list_filter = ('name')

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('name')


# Я не одобряю такой подход, но если можно будет - использую
# admin.site.register(Customers)
# admin.site.register(Products)