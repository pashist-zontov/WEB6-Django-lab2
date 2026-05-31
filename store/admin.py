from django.contrib import admin
from .models import Products, Carts, Customers, CartsProducts
from django.db.models import Min, Max

class CartsProductsInline(admin.TabularInline):
    model = CartsProducts
    extra = 1
    can_delete = True
    autocomplete_fields = ('product',)
    

class CartsInline(admin.TabularInline):
    model = Carts
    extra = 1
    can_delete = True
    fields = ('status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Информация о корзине", {
            "fields": ("customer", "status"),
            "description": "Заполняется админом"
        }),
        ("Статистические данные", {
            "fields": ("created_at", "updated_at"),
            "description": "Не заполняются"
        }),
    )
    
    list_display = ('customer', 'status', 'created_at', 'updated_at', 'products_amount_display', 'total_price_display')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__name', "customer__email", "customer__phone")
    inlines = [CartsProductsInline]
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Число товаров в корзине")
    def products_amount_display(self, obj):
        return obj.products_amount()

    @admin.display(description="Сумма всех товаров в корзине")
    def total_price_display(self, obj):
        return obj.total_price()
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')
    list_filter = ('name',)
    search_fields = ('product',)

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('name',)
    inlines = [CartsInline]


# Я не одобряю такой подход
# admin.site.register(Customers)
# admin.site.register(Products)