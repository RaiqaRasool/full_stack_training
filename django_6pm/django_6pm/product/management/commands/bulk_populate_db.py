from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection

from product.loaders.brand_category_loader import BrandCategoryLoader
from product.loaders.data_loader import DataLoader
from product.loaders.product_color_loader import ProductColorLoader
from product.loaders.product_loader import ProductLoader
from product.loaders.product_size_image_loader import ProductSizeImageLoader


class Command(BaseCommand):
    help = "Populates DB with given json file data"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("-f", "--filepath", type=str, help="Data file path", required=True)

    def handle(self, *args: dict[str, Any], **kwargs: dict[str, Any]) -> None:
        data_loader = DataLoader(kwargs["filepath"])
        items = data_loader.load_data()
        if not items:
            return

        self.save_items(items)

    def save_items(self, items):
        brand_category_loader = BrandCategoryLoader(items)
        saved_brands = brand_category_loader.save_brand_and_category()
        saved_categories = brand_category_loader.update_category_parent()

        product_loader = ProductLoader(items)
        saved_products = product_loader.save_product(saved_brands, saved_categories)

        product_color_loader = ProductColorLoader(items)
        saved_colors = product_color_loader.save_sku_color(saved_products)

        size_image_loader = ProductSizeImageLoader(items)
        size_image_loader.save_sku_size_and_image(saved_colors)

        self.stdout.write(self.style.SUCCESS("---- DB IS POPULATED COMPLETELY ----"))
        print("Queries run: ", len(connection.queries))
