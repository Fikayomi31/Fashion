from ctypes.wintypes import SIZE
from django.contrib import admin
from store.models import Category, Product, Specification, Gallery, Size, Color, Cart, CartOrder, CartOrderItem


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

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'product', 'user', 'qty', 'price', 'total', 'date']
    search_fields = ['cart_id', 'product__name', 'user__username']
    list_filter = ['date', 'product']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['oid', 'buyer', 'total', 'payment_status', 'order_status', 'date']
    search_fields = ['oid', '']
    list_editable = ['payment_status', 'order_status']

class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ['oid', 'order', 'product', 'qty', 'price', 'total']
    search_fields = ['oid', 'order__order_id', 'product__name']
    list_filter = ['order__date']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
