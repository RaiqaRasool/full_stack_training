from argparse import ArgumentParser
from django.core.management.base import BaseCommand
import json
import os
from pathlib import Path
from typing import Any

from product.models import Brand, Category, Product
from product.models import ProductColor, ProductColorSize, ProductColorImage
from product.utils.utils import validate_float, generate_slug 


class Command(BaseCommand):
    help = "Populates DB with given json file data"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('-f', '--filename', type=str, help="Data file path", required=True )

    def handle(self, *args: dict[str, Any] , **kwargs: dict[str, Any]) -> None:
        items = self.load_data(kwargs['filename'])
        if not items:
            return 

        for idx, item in enumerate(items):
            try:
                self.save_item(item)
                self.stdout.write(self.style.SUCCESS(f'Successfully! Saved item no. {idx+1}'))
            except Exception as e:
                self.stderr.write(f"Error! Could not save item no. {idx+1}. Exception: {str(e)}")

    def load_data(self, filename) -> list[dict[str, Any]]:
        root_dir = Path(__file__).resolve().parent.parent.parent.parent
        file_path = os.path.join(root_dir, filename)
        if not os.path.exists(file_path):
            self.stderr.write("Given file does not exist")
            return []
        with open(file_path,'r') as f:
            try:
                items = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(f'Error decoding JSON: {str(e)}')
                return []
        self.stdout.write(self.style.SUCCESS(f'Read and parsed JSON data from file'))
        return items

    def save_item(self, item: dict[str, Any]) -> None:
        brand = self.save_brand(item["brand"])
        category = self.save_category(item["category"])
        product = self.save_product(item, brand, category)
        for key, value in item["skus"].items():
            color = self.save_sku_color(key, product)
            for image in value["image_urls"]:
                self.save_sku_image(image,color)
            for size_variant in value["size_versions"]:
                self.save_sku_size(size_variant, color)

    def save_brand(self, data: dict[str, str]) -> Brand:
        name = data["name"]
        brand, _ = Brand.objects.get_or_create(slug=generate_slug(name),defaults={"name":name, "logo":data["logo"]})
        return brand
    
    def save_category(self, categories: list[str]) -> Category:
        parent_category, _ = Category.objects.get_or_create(slug=generate_slug(categories[0]), defaults={"name":categories[0]})
        for category in categories[1:]:
            parent_category, _ = Category.objects.get_or_create(
                slug = generate_slug(category),
                defaults={"name":category,"parent":parent_category}
                )
        return parent_category

    def save_product(self, item: dict[str, str], brand: Brand, category: Category) -> Product:
        retailer_sku = int(item["retailer_sku"])
        gender = item["gender"].upper().replace('-', '_')
        product, _ = Product.objects.get_or_create(
            retailer_sku=retailer_sku,
            defaults={
            "name":item["name"], "gender":Product.Gender[gender],
            "description":item["description"], "currency":item["currency"],
            "brand":brand, "category":category} 
            )
        return product

    def save_sku_color(self, color: str, product: Product) -> ProductColor:
        color_obj, _ = ProductColor.objects.get_or_create(
            color=color,
            product=product
        )
        return color_obj

    def save_sku_size(self, data: dict[str, str], color: ProductColor) -> ProductColorSize:
        size_variant, _ = ProductColorSize.objects.get_or_create(
            sku_id=int(data["sku_id"]),
            defaults={"size":data["size"],"color":color,
            "price":validate_float(data["price"]),"previous_price":validate_float(data["previous_price"]),
            "is_in_stock":data["out_of_stock"]=="false"
            }
        )
        return size_variant

    def save_sku_image(self, image: str, color: ProductColor) -> ProductColorImage:
        image_obj, _ = ProductColorImage.objects.get_or_create(
            image=image,
            color=color
        )
        return image_obj




