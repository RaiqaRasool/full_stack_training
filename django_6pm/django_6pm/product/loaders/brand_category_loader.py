from product.models import Brand, Category
from product.utils.utils import generate_slug, print_status_msg


class BrandCategoryLoader:
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

    def save_brand_and_category(self) -> list[Brand]:
        brands: list[Brand] = []
        brands_slug: list[str] = []
        categories: list[Category] = []
        categories_slug: list[str] = []
        db_brands = Brand.objects.all()
        db_brands_slug = [brand.slug for brand in db_brands]
        db_categories = Category.objects.all()
        db_categories_slug = [category.slug for category in db_categories]
        for item in self._items:
            brand = self.get_brand(item["brand"])
            if (brand.slug not in db_brands_slug) and (brand.slug not in brands_slug):
                brands.append(brand)
                brands_slug.append(brand.slug)
            product_categories = self.get_category(item["category"])
            for product_category in product_categories:
                if (product_category.slug not in categories_slug) and (product_category.slug not in db_categories_slug):
                    categories.append(product_category)
                    categories_slug.append(product_category.slug)

        Brand.objects.bulk_create(brands)
        Category.objects.bulk_create(categories)
        saved_brands = Brand.objects.all()
        print_status_msg("Successfully!Saved brands and categories")
        return saved_brands

    def update_category_parent(self) -> list[Category]:
        updating_categories: list[Category] = []
        updating_categories_ids: list[int] = []
        db_categories = Category.objects.all()
        saved_categories_slug = [category.slug for category in db_categories]

        for item in self._items:
            product_categories_slug = [generate_slug(category) for category in item["category"]]
            for i in range(len(product_categories_slug) - 1, 0, -1):
                category_idx = saved_categories_slug.index(product_categories_slug[i])
                category = db_categories[category_idx]
                parent_idx = saved_categories_slug.index(product_categories_slug[i - 1])
                parent = db_categories[parent_idx]
                parent_id = db_categories[category_idx].parent_id
                if (not parent_id) and (category.id not in updating_categories_ids):
                    category.parent_id = parent.id
                    updating_categories.append(category)
                    updating_categories_ids.append(category.id)

        Category.objects.bulk_update(updating_categories, ["parent_id"])
        saved_categories = Category.objects.all()
        print_status_msg("Successfully!Updated categories parents")
        return saved_categories
