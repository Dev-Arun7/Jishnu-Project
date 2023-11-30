from django import views
from django.urls import path, include
from core.views import *


app_name = "core"

urlpatterns = [
    path("",index, name="index"),
    path('show_session/', show_session, name="show_session"),
    path('about_us/', about_us, name="about_us"),
    path('product-list/', product_list, name='product_list'),
    path('product/<pid>/', product_detail_views, name="product_detail"),
    #category
    path('category/', categorie_list_views, name='categorie_list'),
    path('category/<cid>/', categorie_product_list_views, name ="categorie_product_list"),

    # add review
    path('ajax-add-review/<pid>/', ajax_add_review, name="ajax-add-review"),
    #vendors
    path('vendors/',vendors_list_views, name="vendors_list"),
    path('vendors/<vid>/',vendor_detail_views, name="vendor_detail"),
    
    # add to cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    #cart view url
    path('cart/', cart, name="cart"),
    # delete cart product
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    #update-cart
    path("update-cart/",update_cart,name="update-cart"),

    # checkout url
    path("checkout/", checkout_views, name="checkout"),


    # razorpay
    path('proceed-to-pay/', razorpaycheck, name = "proceed-to-pay" ),

    # hot Deals
    path("deal/", deals, name="deal"),



    # payment successfull view
    path("payment-completed/", payment_completed_view, name="payment-completed"),

    path("cod/", CashOnDelivery, name ="cod"),
    #payment faild_view
    path("payment-failed/", payment_failed_view, name="payment-failed"),

    path("invoice/", payment_invoice, name="invoice"),
    # dashbord url
    path("dashboard/", customer_dashboard, name="dashboard"),

    # order detail
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),

    # Making address defauly
    path("make-default-address/", make_address_default, name="make-default-address"),

    # searching products
    path("search/", search_view, name="search"),

    # wishlist
    path("wishlist/", wishlist_view, name="wishlist"),
    # add to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    # remove wishlist
    path("remove-from-wishlist", Remove_wishlist, name="Removewishlist"),

    # apply coupon
    path('apply/', coupon_apply, name='coupon_apply'),

    # cancel product
    path('cancel-product/<int:id>/', cancel_product, name='cancel_product'),

    # Return Product
    path('return-product/<int:id>/', return_product, name='return_product'),

    path("statistics/",statistics_view, name="shop-statistics"),
    path("chart/filter-options/", get_filter_options, name="chart-filter-options"),
    path("chart/sales/<int:year>/", get_sales_chart, name="chart-sales"),
    path("chart/spend-per-customer/<int:year>/", spend_per_customer_chart, name="chart-spend-per-customer"),
    path("chart/payment-success/<int:year>/", payment_success_chart, name="chart-payment-success"),
    path("chart/payment-method/<int:year>/", payment_method_chart, name="chart-payment-method"),

]