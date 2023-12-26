from product.models import Product, Category, Brand
from product.utils.utils import generate_slug, print_status_msg


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

    def save_product(self, saved_brands, saved_categories) -> list[Product]:
        saved_brands_slug = [brand.slug for brand in saved_brands]
        saved_categories_slug = [category.slug for category in saved_categories]
        products: list[Product] = []
        products_retailer_sku: list[int] = []
        db_products = Product.objects.all()
        db_products_retailer_sku: list[int] = [product.retailer_sku for product in db_products]
        for item in self._items:
            product_categories_slug = [generate_slug(category) for category in item["category"]]
            saved_category_idx = saved_categories_slug.index(product_categories_slug[-1])
            category = saved_categories[saved_category_idx]

            brand_slug = generate_slug(item["brand"]["name"])
            saved_brand_idx = saved_brands_slug.index(brand_slug)
            brand = saved_brands[saved_brand_idx]

            retailer_sku = int(item["retailer_sku"])

            if (retailer_sku not in db_products_retailer_sku) and (retailer_sku not in products_retailer_sku):
                products.append(self.get_product(item, brand, category))
                products_retailer_sku.append(retailer_sku)

        Product.objects.bulk_create(products)
        saved_products = Product.objects.all()

        print_status_msg("Successfully!Saved products and added parents to categories")
        return saved_products
