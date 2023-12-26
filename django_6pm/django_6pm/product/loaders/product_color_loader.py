from product.models import ProductColor, Product
from product.utils.utils import print_status_msg



class ProductColorLoader:
    def __init__(self, items):
        self._items = items

    def get_sku_color(self, color: str, product: Product) -> ProductColor:
        color_obj = ProductColor(color=color, product=product)
        return color_obj

    def save_sku_color(self, saved_products):
        saved_products_retailer_sku = [product.retailer_sku for product in saved_products]
        db_colors = ProductColor.objects.all()
        db_colors_ids = [{"color": color.color, "retailer_sku": color.product_id } for color in db_colors]
        colors: list[ProductColor] = []
        colors_ids = []
        for item in self._items:
            for color in item["skus"].keys():
                retailer_sku = int(item["retailer_sku"])
                product_idx = saved_products_retailer_sku.index(retailer_sku)
                product = saved_products[product_idx]
                color_id = {"color": color, "retailer_sku": retailer_sku}
                if (color_id not in db_colors_ids) and (color_id not in colors_ids):
                    colors.append(self.get_sku_color(color, product))
                    colors_ids.append(color_id)

        ProductColor.objects.bulk_create(colors)
        saved_colors = ProductColor.objects.all()

        print_status_msg("Successfully!Saved products colors")
        return saved_colors

