from django.db import models

class Customers(models.Model):
    name = models.CharField("Имя покупателя", max_length=100)
    email = models.EmailField("email", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    created_at = models.DateTimeField("Дата и время регистрации", auto_now_add=True)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
    
    def __str__(self):
        return "Покупатель " + self.name

class Carts(models.Model):
    STATUS_CHOICES = (
        ("Active", "Активна"),
        ("Completed", "Оформлена"),
        ("Forgotten", "Заброшена")
    )

    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="carts", verbose_name="Покупатель")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата и время обновления", auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ["-updated_at", "-created_at"]
    
    def __str__(self):
        return f"Корзина покупателя #{self.customer_id} от {self.created_at}"
    
    # Число позиций в одной корзине (???)
    def total_amount(self):
        pass