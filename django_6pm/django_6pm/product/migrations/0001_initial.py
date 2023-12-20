# Generated by Django 4.2.8 on 2023-12-20 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("slug", models.SlugField(max_length=256, unique=True)),
                ("logo", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("slug", models.SlugField(max_length=256, unique=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subcategories",
                        to="product.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "retailer_sku",
                    models.PositiveBigIntegerField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=256)),
                (
                    "gender",
                    models.IntegerField(
                        choices=[
                            (1, "women"),
                            (2, "men"),
                            (3, "unisex-adults"),
                            (4, "boys"),
                            (5, "girls"),
                            (6, "unisex-kids"),
                        ]
                    ),
                ),
                ("description", models.TextField()),
                ("currency", models.CharField(max_length=16)),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="product.brand",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="product.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductColor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color", models.CharField(max_length=128)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="colors",
                        to="product.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductColorSize",
            fields=[
                (
                    "sku_id",
                    models.PositiveBigIntegerField(primary_key=True, serialize=False),
                ),
                ("size", models.CharField(max_length=64)),
                ("price", models.FloatField()),
                ("previous_price", models.FloatField()),
                ("is_in_stock", models.BooleanField(default=True)),
                (
                    "color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sizes",
                        to="product.productcolor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductColorImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.URLField()),
                (
                    "color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="product.productcolor",
                    ),
                ),
            ],
        ),
    ]
