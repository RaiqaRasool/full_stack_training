from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from product.models import Category, Product, Brand
from django.db.models import QuerySet
from typing import Any, Dict


class CategoriesListView(ListView):
    context_object_name = "categories"

    def get_queryset(self) -> QuerySet[Any]:
        categories = Category.objects.filter(parent_id=None)
        return categories


class BrandsListView(ListView):
    model = Brand
    context_object_name = "brands"


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

    def get_queryset(self):
        return Product.objects.filter(retailer_sku=self.kwargs["pk"]).select_related().prefetch_related("images", "sizes")
