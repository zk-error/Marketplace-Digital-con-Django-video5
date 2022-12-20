from django.contrib import admin
from .models import Product,producto_comprado,likes,comentarios,postview

admin.site.register(Product)
admin.site.register(producto_comprado)
admin.site.register(likes)
admin.site.register(comentarios)
admin.site.register(postview)