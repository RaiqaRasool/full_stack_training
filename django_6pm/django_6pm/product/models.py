from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=250)
    logo = models.URLField()


class Category(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)


class Product(models.Model):
    gender_choices = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('unisex-adults', 'Unisex Adults'),
        ('boys','Boys'),
        ('girls', 'Girls'),
        ('unisex-kids', 'Unisex Kids')
    ]

    name = models.CharField(max_length=1000)
    gender = models.CharField(max_length=100, choices=gender_choices)
    description = models.TextField()
    currency = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)


class Sku(models.Model):
    size = models.CharField(max_length=250)
    color = models.CharField(max_length=1000)
    price = models.FloatField()
    previous_price = models.FloatField()
    is_in_stock = models.BooleanField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Sku_image(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE)
    image = models.URLField()
