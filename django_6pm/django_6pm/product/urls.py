from django.urls import include, path

from product.views import *

category_urls = [
    path("", CategoriesListView.as_view(), name="categories"),
    path("/<str:category_slug>", CategoryProductListView.as_view(), name="category_products"),
]

brand_urls = [
    path("", BrandsListView.as_view(), name="brands"),
    path("/<str:brand_slug>", BrandProductListView.as_view(), name="brand_products"),
]

gender_urls = [
    path("/<str:gender>", GenderProductListView.as_view(), name="gender_products"),
]

product_urls = [path("/<int:pk>", ProductDetailView.as_view(), name="product")]

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("categories", include(category_urls)),
    path("brands", include(brand_urls)),
    path("genders", include(gender_urls)),
    path("products", include(product_urls)),
]
