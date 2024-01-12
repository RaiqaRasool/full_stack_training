from product.models import Brand, Category, Product


def navbar_data(request):
    categories = Category.objects.filter(parent_id=None)
    brands = Brand.objects.all()
    category_subcats_mapping = {}
    for category in categories:
        category_subcats_mapping[category] = category.subcategories.all()
    genders = Product.Gender.choices
    return {"navbar_categories": category_subcats_mapping, "navbar_genders": genders, "navbar_brands": brands}
