from django.contrib import admin
from core.models import CartOrderProducts, Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address,Banner,Coupon,Wallet,Transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_editable = ['title', 'price', 'featured', 'product_status']
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'vendor', 'featured', 'product_status', 'stock_count']

    def stock_count_display(self, obj):
        return obj.stock_count  # Assuming 'stock_count' is a field in your Product model

    stock_count_display.short_description = 'Stock Count'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','cid','category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']


class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status','product_status','sku']
    list_display = ['user',  'price', 'paid_status', 'order_date','product_status', 'sku']


class CartOrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image','qty', 'price', 'total']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']


class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']

class BannerAdmin(admin.ModelAdmin):
    list_display = ['images', 'brand','date']

class CouponAdmin(admin.ModelAdmin):
    list_editable =[ 'discount','valid_from','valid_to','active'] 
    list_display =['code', 'discount','valid_from','valid_to','active']

class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
    list_editable = [ 'balance']









admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProducts, CartOrderProductsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(wishlist_model, wishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Wallet,WalletAdmin)