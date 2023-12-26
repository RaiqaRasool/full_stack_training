from product.models import ProductColor, ProductColorImage, ProductColorSize
from product.utils.utils import validate_float, print_status_msg


class ProductSizeImageLoader:
    def __init__(self, items):
        self._items = items

    def get_sku_size(
        self, data: dict[str, str], color: ProductColor
    ) -> ProductColorSize:
        size_variant = ProductColorSize(
            sku_id=int(data["sku_id"]),
                size=data["size"],
                color=color,
                price=validate_float(data["price"]),
                previous_price=validate_float(data["previous_price"]),
                is_in_stock=data["out_of_stock"] == "false",
        )
        return size_variant

    def get_sku_image(self, image: str, color: ProductColor) -> ProductColorImage:
        image_obj = ProductColorImage(image=image, color=color)
        return image_obj

    def save_sku_size_and_image(self, saved_colors):
        saved_colors_ids = [{"color": color.color, "retailer_sku": color.product_id} for color in saved_colors] 
        db_sizes = ProductColorSize.objects.all()
        db_sizes_ids = [size.sku_id for size in db_sizes]
        db_images = ProductColorImage.objects.select_related().all()
        db_images_ids = [{"color":image.color, "image":image.image} for image in db_images]
        sizes = []
        sizes_ids = []
        images = []
        image_ids = []
        for item in self._items:
            for color, value in item["skus"].items():
                color_id = {"color": color, "retailer_sku": int(item["retailer_sku"])}
                color_idx = saved_colors_ids.index(color_id)
                saved_color = saved_colors[color_idx]

                for size_variant in value["size_versions"]:
                    sku_id = int(size_variant["sku_id"])
                    if (sku_id not in sizes_ids) and (sku_id not in db_sizes_ids):
                        sizes.append(self.get_sku_size(size_variant, saved_color))
                        sizes_ids.append(sku_id)

                for image in value["image_urls"]:
                    image_obj = self.get_sku_image(image, saved_color)
                    image_id = {"color": image_obj.color, "image": image} 
                    if (image_id not in db_images_ids) and (image_id not in image_ids):
                        images.append(image_obj)
                        image_ids.append(image_id)

        ProductColorSize.objects.bulk_create(sizes)
        ProductColorImage.objects.bulk_create(images)

        print_status_msg("Successfully!Saved products sizes and images")
