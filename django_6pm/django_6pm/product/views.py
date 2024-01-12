import json
from typing import Any, Dict

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from product.models import (Brand, Category, Product, ProductColorSize,
                            SkuSubscription)


class HomeListView(ListView):
    template_name = "product/home.html"
    context_object_name = "category_products_mapping"
    model = Category

    def get_category_products(self, cat, products):
        subcats = list(cat.subcategories.all())
        products_limit = settings.HOMEPAGE_PRODUCTS_PER_LIST
        if subcats is None or len(products) >= products_limit:
            return products
        for subcat in subcats:
            subcat_prods = list(
                subcat.products.filter(is_active=True)
                .select_related("brand", "category")
                .prefetch_related("images", "sizes")[:products_limit]
            )
            if subcat_prods:
                products.extend(subcat_prods)
            if len(products) >= products_limit:
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
        return Product.objects.filter(is_active=True).order_by("gender").distinct().values_list("gender", flat=True)

    def get_genders_products(self):
        genders = self.get_genders()
        gender_products_mapping = {}
        for gender in genders:
            gender_products_mapping[Product.Gender(gender).label] = (
                Product.objects.filter(is_active=True, gender=gender)
                .select_related("brand", "category")
                .prefetch_related("sizes", "images")[0 : settings.HOMEPAGE_PRODUCTS_PER_LIST]
            )
        return gender_products_mapping

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["category_products_mapping"] = self.get_categories_products()
        context["gender_products_mappings"] = self.get_genders_products()
        context["featured_products"] = (
            Product.objects.filter(is_active=True, is_featured=True)
            .select_related("brand", "category")
            .prefetch_related("images", "sizes")[: settings.HOMEPAGE_PRODUCTS_PER_LIST]
        )
        return context


class FeaturedProductListView(ListView):
    model = Product
    template_name = "product/featured_products.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        self.product = (
            Product.objects.filter(is_active=True, is_featured=True)
            .select_related("brand", "category")
            .prefetch_related("images", "sizes")
        )
        return self.product

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["total_products"] = len(self.product)
        return context


class InActiveProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/inactive_products.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        self.product = (
            Product.objects.filter(is_active=False)
            .select_related("brand", "category")
            .prefetch_related("images", "sizes")
        )
        return self.product

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["total_products"] = len(self.product)
        return context


class CategoriesListView(ListView):
    context_object_name = "categories"
    queryset = Category.objects.filter(parent_id=None)


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
        self.products = Product.objects.filter(is_active=True, gender=Product.Gender[gender_idx])
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
        self.products = self.brand.products.filter(is_active=True)
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
            Product.objects.filter(is_active=True, category=self.category)
            .select_related("brand")
            .prefetch_related("sizes", "images")
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
            Product.objects.filter(retailer_sku=self.kwargs["pk"])
            .select_related("brand", "category")
            .prefetch_related("images", "sizes")
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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "product/product_update.html"
    model = Product
    fields = ["name", "gender", "description", "currency", "brand", "is_featured", "is_active", "category"]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        ProductFormSet = modelformset_factory(ProductColorSize, exclude=["product", "sku_id"], extra=0)
        product_color_size_formset = ProductFormSet(
            self.request.POST or None, queryset=ProductColorSize.objects.filter(product=self.object)
        )
        context["product_color_size_formset"] = product_color_size_formset
        return context

    def form_valid(self, form, **kwargs):
        context_data = self.get_context_data()
        product_color_size_formset = context_data["product_color_size_formset"]
        if form.is_valid() and product_color_size_formset.is_valid():
            product_color_size_formset.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("product", args=[self.object.retailer_sku])


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product/product_delete.html"
    context_object_name = "product"

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.sizes.all().delete()
        product.images.all().delete()
        return super().delete(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy("product_delete_success")


class ProductDeleteSuccessTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "product/product_delete_success.html"


class SkuSubscriptionCreateView(LoginRequiredMixin, CreateView):
    model = SkuSubscription
    fields = ["email"]

    def form_valid(self, form):
        sku = get_object_or_404(ProductColorSize, sku_id=self.kwargs["sku_id"])
        form.instance.sku = sku
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("product", args=[self.kwargs["pk"]])

