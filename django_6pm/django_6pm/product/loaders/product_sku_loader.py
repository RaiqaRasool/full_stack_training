from django.db.models import BaseManager

from product.models import Color, Product, ProductColorImage, ProductColorSize
from product.utils.utils import generate_mapping, print_status_msg, validate_float


class ProductSkuLoader:
    def __init__(self, items):
        self._items = items

    def get_sku_size(self, data: dict[str, str], color: Color, product: Product) -> ProductColorSize:
        size_variant = ProductColorSize(
            sku_id=int(data["sku_id"]),
            size=data["size"],
            price=validate_float(data["price"]),
            previous_price=validate_float(data["previous_price"]),
            is_in_stock=data["out_of_stock"] == "false",
            color=color,
            product=product,
        )
        return size_variant

    def get_sku_image(self, image: str, color: Color, product: Product) -> ProductColorImage:
        image_obj = ProductColorImage(image=image, color=color, product=product)
        return image_obj

    def save_sku(self, saved_products: BaseManager[Product], saved_colors: BaseManager[Color]) -> None:
        saved_products_mapping = generate_mapping(saved_products, "retailer_sku")
        saved_colors_mapping = generate_mapping(saved_colors, "color_id")
        db_images = ProductColorImage.objects.all()
        db_images_mapping = generate_mapping(db_images, "image")
        images_mapping = {}
        db_sizes = ProductColorSize.objects.all()
        db_sizes_mapping = generate_mapping(db_sizes, "sku_id")
        sizes_mapping = {}
        for item in self._items:
            for color, value in item["skus"].items():
                retailer_sku = int(item["retailer_sku"])
                product = saved_products_mapping[retailer_sku]
                color_id = int(value["color_id"])
                color = saved_colors_mapping[color_id]
                for image in value["image_urls"]:
                    image_obj = self.get_sku_image(image, color, product)
                    if (image not in db_images_mapping) and (image not in images_mapping):
                        images_mapping[image] = image_obj
                for size in value["size_versions"]:
                    size_obj = self.get_sku_size(size, color, product)
                    size_id = size_obj.sku_id
                    if (size_id not in db_sizes_mapping) and (size_id not in sizes_mapping):
                        sizes_mapping[size_id] = size_obj

        ProductColorImage.objects.bulk_create(images_mapping.values())
        print_status_msg("Successfully!Saved product images")
        ProductColorSize.objects.bulk_create(sizes_mapping.values())
        print_status_msg("Successfully!Saved product sizes")
