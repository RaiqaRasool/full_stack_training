from django.contrib import admin

from product.models import *

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(ProductColorSize)
admin.site.register(ProductColorImage)