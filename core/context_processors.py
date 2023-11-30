from core.models import CartOrderProducts, Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address
from django.contrib import messages
def default(request):
    products = Product.objects.filter(product_status ="published", featured ="True")
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    new_arrival = Product.objects.filter(product_status ="published", featured ="True").order_by('-date')
    
    # try:
    #     wishlist_count = wishlist_model.objects.filter( user = request.user)
    # except:
    #     wishlist_count =None
    #     messages.warning(request, "you need to login before add wishlist")
        


    return {
        "categories":categories,
        "vendors":vendors,
        "new_arrival":new_arrival,
        "product": products,
        # "wishlist":wishlist_count,

    }