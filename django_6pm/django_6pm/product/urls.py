from django.urls import path

from product.views import *

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("g/<gender>", GenderProductListView.as_view(), name="gender_products"),
    path("categories", CategoriesListView.as_view(), name="categories"),
    path("c/<category_slug>", CategoryProductListView.as_view(), name="category_products"),
    path("brands", BrandsListView.as_view(), name="brands"),
    path("b/<brand_slug>", BrandProductListView.as_view(), name="brand_products"),
    path("p/<pk>", ProductDetailView.as_view(), name="product"),
]
