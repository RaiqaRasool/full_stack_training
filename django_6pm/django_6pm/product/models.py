from django.db import models


class Brand(models.Model):
    brand_name = models.CharField(max_length=250)
    brand_logo = models.URLField()


class Category(models.Model):
    cat_name = models.CharField(max_length=250)
    parent_cat_id = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)


class Product(models.Model):
    product_id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=1000)
    gender = models.CharField(max_length=100)
    description = models.TextField()
    currency = models.CharField(max_length=50)
    brand_id = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    cat_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)


class Sku(models.Model):
    sku_size = models.CharField(max_length=250)
    sku_color = models.CharField(max_length=1000)
    sku_price = models.FloatField()
    previous_price = models.FloatField()
    out_of_stock = models.BooleanField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Sku_image(models.Model):
    sku_id = models.ForeignKey(Sku, on_delete=models.CASCADE)
    image_url = models.URLField()
