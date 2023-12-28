from django.db.models.query import QuerySet

from product.models import Brand, Category, Color
from product.utils.utils import generate_mapping, generate_slug, print_status_msg


class BrandCategoryColorLoader:
    def __init__(self, items):
        self._items = items

    def get_brand(self, data: dict[str, str]) -> Brand:
        name = data["name"]
        brand = Brand(slug=generate_slug(name), name=name, logo=data["logo"])
        return brand

    def get_category(self, categories: list[str]) -> list[Category]:
        categories_objs: list[Category] = []
        for category in categories:
            category_obj = Category(slug=generate_slug(category), name=category)
            categories_objs.append(category_obj)
        return categories_objs

    def get_color(self, colors_data: dict[str, dict]) -> list[Color]:
        color_objs: list[Color] = []
        for color, value in colors_data.items():
            color_obj = Color(color=color, color_id=int(value["color_id"]))
            color_objs.append(color_obj)
        return color_objs

    def save_brand_category_color(self) -> tuple[QuerySet[Brand], QuerySet[Color]]:
        brands_mapping = {}
        categories_mapping = {}
        db_brands = Brand.objects.all()
        db_brands_mapping = generate_mapping(db_brands, "slug")
        db_categories = Category.objects.all()
        db_categories_mapping = generate_mapping(db_categories, "slug")
        db_colors = Color.objects.all()
        db_colors_mapping = generate_mapping(db_colors, "color_id")
        colors_mapping = {}
        for item in self._items:
            brand = self.get_brand(item["brand"])
            if (brand.slug not in db_brands_mapping) and (brand.slug not in brands_mapping):
                brands_mapping[brand.slug] = brand
            product_categories = self.get_category(item["category"])
            for product_category in product_categories:
                if (product_category.slug not in categories_mapping) and (
                    product_category.slug not in db_categories_mapping
                ):
                    categories_mapping[product_category.slug] = product_category
            product_colors = self.get_color(item["skus"])
            for color in product_colors:
                color_id = color.color_id
                if (color_id not in db_colors_mapping) and (color_id not in colors_mapping):
                    colors_mapping[color_id] = color

        Brand.objects.bulk_create(brands_mapping.values())
        print_status_msg("Successfully!Saved brands")
        Category.objects.bulk_create(categories_mapping.values())
        print_status_msg("Successfully!Saved categories")
        Color.objects.bulk_create(colors_mapping.values())
        print_status_msg("Successfully!Saved colors")
        saved_brands = Brand.objects.all()
        saved_colors = Color.objects.all()
        return saved_brands, saved_colors

    def update_category_parent(self) -> QuerySet[Category]:
        updating_categories_mapping = {}
        db_categories = Category.objects.all()
        db_categories_mapping = generate_mapping(db_categories, "slug")

        for item in self._items:
            product_categories_slug = [generate_slug(category) for category in item["category"]]
            for i in range(len(product_categories_slug) - 1, 0, -1):
                category = db_categories_mapping[product_categories_slug[i]]
                parent = db_categories_mapping[product_categories_slug[i - 1]]
                parent_id = category.parent_id
                if (not parent_id) and (category.slug not in updating_categories_mapping):
                    category.parent_id = parent.id
                    updating_categories_mapping[category.slug] = category

        Category.objects.bulk_update(updating_categories_mapping.values(), ["parent_id"])
        saved_categories = Category.objects.all()
        print_status_msg("Successfully!Updated categories parents")
        return saved_categories
