from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User


class Brand(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=256)
    logo = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Brand: {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=256)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True,
        blank=True, related_name="subcategories",
    )

    def __str__(self) -> str:
        return f"Category: {self.name}"


class Color(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    color = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f"Color: {self.color}"


class Product(models.Model):
    class Gender(models.IntegerChoices):
        WOMEN = 1, _("women")
        MEN = 2, _("men")
        UNISEX_ADULTS = 3, _("unisex-adults")
        BOYS = 4, _("boys")
        GIRLS = 5, _("girls")
        UNISEX_KIDS = 6, _("unisex-kids")

    retailer_sku = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    gender = models.IntegerField(choices=Gender.choices)
    description = models.TextField()
    currency = models.CharField(max_length=16)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="products",
    )

    def __str__(self) -> str:
        return f"Product: {self.name}"


class ProductColorSize(models.Model):
    sku_id = models.PositiveBigIntegerField(primary_key=True)
    size = models.CharField(max_length=64)
    price = models.FloatField()
    previous_price = models.FloatField()
    is_in_stock = models.BooleanField(default=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name="sizes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sizes")

    def __str__(self) -> str:
        return f"{self.color}, Size: {self.size}"


class ProductColorImage(models.Model):
    image = models.URLField()
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name="images")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    def __str__(self) -> str:
        return f"{self.color}, Image: {self.image}"


class SkuSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    sku = models.ForeignKey(ProductColorSize, on_delete=models.CASCADE, related_name="subscriptions")
    email = models.EmailField(max_length=256)
    subscribed_at = models.DateField(auto_now_add=True) 

    class Meta:
        unique_together = ["user", "sku"]

    def save(self, *args, **kwargs) -> None:
        existing_subscription = SkuSubscription.objects.filter(user=self.user, sku=self.sku).exists()
        if not existing_subscription:
            super().save(*args, **kwargs)

