from django.contrib import admin
from django.contrib.auth.models import User, Group as auth_group

from texnomart import models


# Register your models here.

@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    prepopulated_fields = {'slug': ('category_name',)}


admin.site.register(models.Image)
admin.site.register(models.Comment)
admin.site.unregister(models.User)
admin.site.unregister(auth_group)
admin.site.register(models.Attribute)
admin.site.register(models.AttributeValue)
admin.site.register(models.ProductAttribute)

@admin.register(models.Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug']
    prepopulated_fields = {'slug': ('product_name',)}