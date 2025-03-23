from ctypes.wintypes import SIZE
from django.contrib import admin
from store.models import Category, Product, Specification, Gallery, Size, Color


class GalleryInline(admin.TabularInline):
    model = Gallery

class SpecificationInline(admin.TabularInline):
    model = Specification

class ColorInline(admin.TabularInline):
    model = Color

class SizeInline(admin.TabularInline):
    model = Size

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'shipping_amount', 'stock_qty', 'in_stock', 'vendor', 'featured']
    list_editable = ['featured']
    list_filter = ['date']
    search_fields = ['title']
    inlines = [GalleryInline, SpecificationInline, ColorInline, SizeInline]
    

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

