from django.contrib import admin

from catalog_app.models import Product, Category, Image, Slider, Banner


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Image._meta.fields]


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Slider._meta.fields]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Banner._meta.fields]
