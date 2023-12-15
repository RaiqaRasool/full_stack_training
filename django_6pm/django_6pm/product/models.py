from django.db import models
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    name = models.CharField(max_length=250)
    logo = models.URLField()


class Category(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)


class Product(models.Model):
    class Gender(models.IntegerChoices):
        WOMEN = 1, _("women")
        MEN = 2, _("men")
        UNISEX_ADULTS = 3, _("unisex-adults")
        BOYS = 4, _("boys")
        GIRLS = 5, _("girls")
        UNISEX_KIDS = 6, _("unisex-kids")

    name = models.TextField()
    gender = models.IntegerField(choices=Gender.choices)
    description = models.TextField()
    currency = models.CharField(max_length=10)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)


class ProdColor(models.Model):
    color = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProdColorSize(models.Model):
    size = models.CharField(max_length=100)
    price = models.FloatField()
    previous_price = models.FloatField()
    is_in_stock = models.BooleanField(default=True)
    prod_color = models.ForeignKey(ProdColor, on_delete=models.CASCADE)


class ProdColorImage(models.Model):
    image = models.URLField()
    prod_color = models.ForeignKey(ProdColor, on_delete=models.CASCADE)
