from django.db.models.query import QuerySet

from product.models import Brand, Category, Product
from product.utils.utils import generate_mapping, generate_slug, print_status_msg


class ProductLoader:
    def __init__(self, items):
        self._items = items

    def get_product(self, item: dict[str, str], brand: Brand, category: Category) -> Product:
        retailer_sku = int(item["retailer_sku"])
        gender = item["gender"].upper().replace("-", "_")
        product = Product(
            retailer_sku=retailer_sku,
            name=item["name"],
            gender=Product.Gender[gender],
            description=item["description"],
            currency=item["currency"],
            brand=brand,
            category=category,
        )
        return product

    def save_product(
        self, saved_brands: QuerySet[Brand], saved_categories: QuerySet[Category]
    ) -> QuerySet[Product]:
        saved_brands_mapping = generate_mapping(saved_brands, "slug")
        saved_categories_mapping = generate_mapping(saved_categories, "slug")
        products_mapping = {}
        db_products = Product.objects.all()
        db_products_mapping = generate_mapping(db_products, "retailer_sku")
        for item in self._items:
            product_categories_slug = [generate_slug(category) for category in item["category"]]
            category = saved_categories_mapping[product_categories_slug[-1]]

            brand_slug = generate_slug(item["brand"]["name"])
            brand = saved_brands_mapping[brand_slug]

            retailer_sku = int(item["retailer_sku"])

            if (retailer_sku not in db_products_mapping) and (retailer_sku not in products_mapping):
                products_mapping[retailer_sku] = self.get_product(item, brand, category)

        Product.objects.bulk_create(products_mapping.values())
        print_status_msg("Successfully!Saved products and added parents to categories")

        saved_products = Product.objects.all()
        return saved_products
