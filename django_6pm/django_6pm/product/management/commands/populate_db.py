import time
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection

from product.loaders.brand_category_color_loader import BrandCategoryColorLoader
from product.loaders.data_loader import DataLoader
from product.loaders.product_loader import ProductLoader
from product.loaders.product_sku_loader import ProductSkuLoader


class Command(BaseCommand):
    help = "Populates DB with given json file data"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("-f", "--filepath", type=str, help="Data file path", required=True)

    def handle(self, *args: dict[str, Any], **kwargs: dict[str, Any]) -> None:
        t1 = time.time()
        data_loader = DataLoader(kwargs["filepath"])
        items = data_loader.load_data()
        if not items:
            return

        self.save_items(items)
        t2 = time.time()
        print("Time taken: ", t2 - t1)

    def save_items(self, items):
        brand_category_loader = BrandCategoryColorLoader(items)
        saved_brands, saved_colors = brand_category_loader.save_brand_category_color()
        saved_categories = brand_category_loader.update_category_parent()

        product_loader = ProductLoader(items)
        saved_products = product_loader.save_product(saved_brands, saved_categories)

        product_sku_loader = ProductSkuLoader(items)
        product_sku_loader.save_sku(saved_products, saved_colors)

        self.stdout.write(self.style.SUCCESS("---- DB IS POPULATED COMPLETELY ----"))
        print("Queries run: ", len(connection.queries))