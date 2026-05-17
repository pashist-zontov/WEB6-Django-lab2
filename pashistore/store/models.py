from django.db import models
from django.db.models import Sum, Count

class Customers(models.Model):
    name = models.CharField("Имя покупателя", max_length=100)
    email = models.EmailField("email", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    created_at = models.DateTimeField("Дата и время регистрации", auto_now_add=True)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
    
    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField("Наименование товара", max_length=200)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    description = models.TextField("Описание", blank=True)
    image = models.URLField("Ссылка на изображение", blank=True, null=True)
    

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return self.name

class Carts(models.Model):
    STATUS_CHOICES = (
        ("Active", "Активна"),
        ("Completed", "Оформлена"),
        ("Forgotten", "Заброшена")
    )

    # cart_id = models.IntegerField(primary_key=True) <-- Вопрос: стоит ли создавать свой первичный ключ в работах подобной этой?
    # Или для простых баз можно обойтись без них?
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="carts", verbose_name="Покупатель")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="Active")
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата и время обновления", auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ["-updated_at", "-created_at"]
    
    def __str__(self):
        return f"Корзина покупателя #{self.customer_id} от {self.created_at}"
    
    def products_amount(self):
        return self.products.aggregate(total=Sum("quantity"))['total_amount']
    
    def unique_products_count(self):
        return self.products.count()
    
class CartsProducts(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, related_name="products", verbose_name="Корзина")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции"
        unique_together = ("cart", "product") # !!! Корзина и товары должны отображаться уникальные друг по от
    
    def __str__(self):
        return f"{self.quantity} x {self.product}"