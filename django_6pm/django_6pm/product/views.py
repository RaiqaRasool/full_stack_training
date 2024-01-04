import json
from typing import Any, Dict

from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from product.models import Brand, Category, Product


class HomeListView(ListView):
    template_name = "product/home.html"
    context_object_name = "category_products_mapping"
    model = Category

    def get_category_products(self, cat, products):
        subcats = list(cat.subcategories.all())
        if subcats is None or len(products) >= 4:
            return products
        for subcat in subcats:
            subcat_prods = list(subcat.products.select_related().prefetch_related("images", "sizes")[:4])
            if subcat_prods:
                products.extend(subcat_prods)
            if len(products) >= 4:
                return products
            products = self.get_category_products(subcat, products)
        return products

    def get_categories_products(self):
        categories = Category.objects.filter(parent_id=None)
        category_product_mapping = {}
        for category in categories:
            category_product_mapping[category] = self.get_category_products(category, [])
        return category_product_mapping

    def get_genders(self):
        gender_queryset = Product.objects.values("gender").order_by("gender").distinct()
        gender_values = [item["gender"] for item in gender_queryset]
        return gender_values

    def get_genders_products(self):
        genders = self.get_genders()
        gender_products_mapping = {}
        for gender in genders:
            gender_products_mapping[Product.Gender(gender).label] = (
                Product.objects.filter(gender=gender).select_related().prefetch_related("sizes", "images")[0:4]
            )
        return gender_products_mapping

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["category_products_mapping"] = self.get_categories_products()
        context["gender_products_mappings"] = self.get_genders_products()
        return context


class CategoriesListView(ListView):
    context_object_name = "categories"

    def get_queryset(self) -> QuerySet[Any]:
        categories = Category.objects.filter(parent_id=None)
        return categories


class BrandsListView(ListView):
    model = Brand
    context_object_name = "brands"


class GenderProductListView(ListView):
    template_name = "product/products_by_gender.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        self.gender = self.kwargs["gender"]
        gender_idx = self.gender.upper().replace("-", "_")
        self.products = Product.objects.filter(gender=Product.Gender[gender_idx])
        return self.products

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["gender"] = self.gender
        context["total_products"] = len(self.products)
        return context


class BrandProductListView(ListView):
    template_name = "product/products_by_brand.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        self.brand = get_object_or_404(Brand, slug=self.kwargs["brand_slug"])
        self.products = self.brand.products.all()
        return self.products

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["brand"] = self.brand
        context["total_products"] = len(self.products)
        return context


class CategoryProductListView(ListView):
    template_name = "product/products_by_category.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        self.category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        self.subcategories = self.category.subcategories.all()
        self.products = (
            Product.objects.filter(category=self.category).select_related("brand").prefetch_related("sizes", "images")
        )
        return self.products

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["subcategories"] = self.subcategories
        context["total_products"] = len(self.products)
        return context


class ProductDetailView(DetailView):
    context_object_name = "product"

    def get_color_sizes_mapping(self):
        color_sizes_mapping = {}
        for size in self.product.first().sizes.all():
            if size.color not in color_sizes_mapping:
                color_sizes_mapping[size.color] = [size]
            else:
                color_sizes_mapping[size.color].append(size)
        self.colors = list(color_sizes_mapping.keys())
        return color_sizes_mapping

    def get_color_images_mapping(self):
        color_images_mapping = {}
        for color in self.colors:
            color_images_mapping[color.id] = []
        for image in self.product.first().images.all():
            color_images_mapping[image.color_id].append(image.image)
        return color_images_mapping

    def get_queryset(self):
        self.product = (
            Product.objects.filter(retailer_sku=self.kwargs["pk"]).select_related().prefetch_related("images", "sizes")
        )
        return self.product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["color_sizes_mapping"] = self.get_color_sizes_mapping()
        color_images_mapping = self.get_color_images_mapping()
        context["color_images_mapping"] = json.dumps(color_images_mapping)
        default_color = self.colors[0].id
        context["default_images"] = color_images_mapping[default_color]
        return context
