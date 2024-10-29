from django.contrib import admin
from .models import *

admin.site.register(ProductModel)
admin.site.register(MaterialModel)
admin.site.register(ProductMaterialModel)
admin.site.register(WarehouseModel)

