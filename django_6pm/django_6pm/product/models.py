from django.db import models
from django.utils.translation import gettext_lazy as _


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
        blank=True, related_name="subcategories",)

    def __str__(self) -> str:
        return f"Category: {self.name}"


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
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                null=True,blank=True,related_name="products",)

    def __str__(self) -> str:
        return f"Product: {self.name}"


class ProductColor(models.Model):
    color = models.CharField(max_length=128)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="colors"
    )

    def __str__(self) -> str:
        return f"{self.product}, Color: {self.color}"


class ProductColorSize(models.Model):
    sku_id = models.PositiveBigIntegerField(primary_key=True)
    size = models.CharField(max_length=64)
    price = models.FloatField()
    previous_price = models.FloatField()
    is_in_stock = models.BooleanField(default=True)
    color = models.ForeignKey(
        ProductColor, on_delete=models.CASCADE, related_name="sizes"
    )

    def __str__(self) -> str:
        return f"{self.color}, Size: {self.size}"


class ProductColorImage(models.Model):
    image = models.URLField()
    color = models.ForeignKey(
        ProductColor, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self) -> str:
        return f"{self.color}, Image: {self.image}"
