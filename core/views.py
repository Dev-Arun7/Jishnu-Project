from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from core.models import *
from django.db.models import Count, Avg
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import F, FloatField, ExpressionWrapper
from django.views.decorators.csrf import csrf_exempt
from core.forms import ProductReviewForm
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.core import serializers
from django.utils import timezone
from .models import Coupon
from .models import CartOrder
from .forms import CouponApplyForm
import logging


import calendar
from django.db.models.functions import ExtractMonth
from .models import Wallet, Transaction



def show_session(request):
    # for key,value in request.session.items():
    #     print(key)
    return render(request,'core/show_session.html')

# Define a custom test function to check if the user is not a superuser
def is_not_superuser(user):
    return not user.is_superuser

# Create your views here.

def index(request):
    if request.user.is_superuser :
        return  redirect('admin:index')
    else:
        products = Product.objects.filter(product_status ="published", featured ="True")
        banner_img = Banner.objects.all()

    context = {
        "product": products,
        "banner_img":banner_img,
    }

    
    
    return render(request,'core/index.html',context)

# about us
def about_us(request):

    cart = request.session['cart_data_obj']
    
    return render(request, 'core/about_us.html')

def categorie_list_views(request):
    categories = Category.objects.all()

    context = {
        "categories": categories 
    }
    return render(request, 'core/categorie_list.html', context)

def categorie_product_list_views(request,cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status ="published", category = category)

    context ={
        "categories":category,
        "products": products,
    }
    return render(request, 'core/categorie_product_list.html',context)


def vendors_list_views(request):
    vendors =Vendor.objects.all()

    context = {
        "vendors":vendors
    }
    return render(request, 'core/vendors_list.html',context)

def vendor_detail_views(request,vid):
    vendor = Vendor.objects.get(vid=vid)
    products =Product.objects.filter(vendor = vendor)

    context = {
        "vendor":vendor,
        "products":products
    }
    return render(request,'core/vendor-detail.html', context)

def product_detail_views(request,pid):
    product = Product.objects.get(pid=pid)
    vendor = Vendor.objects.get(product = product)
    p_image = product.p_images.all()

    active_address = None
    if request.user.is_authenticated:
        try:
            active_address = Address.objects.get(user=request.user, status=True)
        except Address.DoesNotExist:
            messages.warning(request, "There are multiple addresses, only one should be activated.")

  
    #related product 
    products = Product.objects.filter(category=product.category)

    # Getting review from productreview of each product
    reviews = ProductReview.objects.filter(product = product)
    

    #  getting avg rating about a product from customers
    avg_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))

    # feltching form data from form.py
    review_form = ProductReviewForm()

    context = {
        "product":product,
        "vendor":vendor,
        "p_image":p_image,
        "review_form": review_form,
        "products":products,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "address":active_address,
        }
    return render(request,"core/product_detail.html", context)


# views.py


def product_list(request):
    products = Product.objects.all()
    if request.GET:
        category_ids = request.GET.getlist('category')
        vendor_ids = request.GET.getlist('vendor')
        price_range = request.GET.get('price_range')
        
        # Filter by category
        if category_ids:
            products = products.filter(category__id__in=category_ids)

        # Filter by vendor
        if vendor_ids:
            products = products.filter(vendor__id__in=vendor_ids)

    
        # Filter by price range
        if price_range:
            min_price, max_price = map(int, price_range.split('-'))
            products = products.filter(price__range=(min_price, max_price))

    return render(request, 'core/product-list.html', {'product': products})




def ajax_add_review(request,pid):
    product = Product.objects.get(pid = pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'] 
    )
    if review is not None:
        messages.success(request, "Thanks for your valuable feedback on this product")

    avg_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))

    context = {
        'user' : user,
        'product': product,
        'review': request.POST['review'],
        'rating': request.POST['rating']
    }
    
    return JsonResponse({
        'bool': True, 'context': context, 'avg_rating': avg_rating
        })

# search funtionality
def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "core/search.html", context)
 
# Hot Deals
def deals(request):
    # Calculate the discount percentage for each product
    products = Product.objects.annotate(
        discount_percentage=ExpressionWrapper(
            100 * (F('old_price') - F('price')) / F('old_price'),
            output_field=FloatField()
        )
    )
    # Filter products with a discount of 40% or more directly in the query
    discounted_products = products.filter(discount_percentage__gte=40.0)

    return render(request, 'core/deal.html', {'products': discounted_products})

# add to cart functionality
def add_to_cart(request):
    
    cart_product = {}

    cart_product = {
        str(request.GET['id']): {
            'title': request.GET['title'],
            'qty': request.GET['qty'],
            'price': request.GET['price'],
            'image': request.GET['image'],
            'pid': request.GET['pid'],
        }
    }    


    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_data[str(request.GET['id'])]['qty']) + int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product

    
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

# apply coupon
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, "your coupon added!")
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    else:
        messages.warning(request, "Your cart is empty")

    return redirect('core:cart')  # Redirect to your cart page


def cart(request):

    cart_total_amount = 0
    coupon = None  # Initialize coupon to None
    
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        sub_total = cart_total_amount

        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            try:
                coupon = Coupon.objects.get(id=coupon_id, valid_from__lte=timezone.now(), valid_to__gte=timezone.now(), active=True)
                # Apply discount logic here
                if cart_total_amount >= 500:
                    cart_total_amount -= float(coupon.discount)
                    # Update the cart_total_amount in the session
                    request.session['cart_total_amount'] = cart_total_amount
                else:
                    request.session['cart_total_amount'] = cart_total_amount

                
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
                messages.error(request, "coupon not matcheched ")
        else:
            request.session['cart_total_amount'] = cart_total_amount

        context = {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'form': CouponApplyForm(), 
            'subtotal': sub_total,
            'coupon': coupon.discount if coupon else None,  # Access coupon.discount only if coupon is not None
        }
        return render(request, "core/cart.html", context)
    
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")

    

# delete cart product
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            
            del request.session['cart_data_obj'][product_id]
           
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

from django.db import transaction

@login_required
def checkout_views(request):
    cart_total_amount = 0
    total_amount = 0
    try:
        with transaction.atomic():
            if 'cart_data_obj' in request.session:
                
                cart_total_amount = request.session['cart_total_amount']
                if 'order_id' in request.session:
                    
                    order = CartOrder.objects.get(id=request.session['order_id'])

                else:
                    # create order object
                    order = CartOrder.objects.create(
                        user=request.user,
                        price=cart_total_amount
                    )

                    for p_id, item in request.session['cart_data_obj'].items():

                        cart_order_products = CartOrderProducts.objects.create(
                            order=order,
                            invoice_no="INVOICE_NO-" + str(order.id),
                            item=item['title'],
                            image=item['image'],
                            qty=item['qty'],
                            price=item['price'],
                            total=float(item['qty']) * float(item['price'])
                        )
                    
                    request.session['order_id'] = order.id

    

            try:
                active_address = Address.objects.get(user=request.user, status=True)
            except Address.DoesNotExist:
                messages.warning(request, "There are multiple addresses, only one should be activated.")
                active_address = None

            return render(request, 'core/checkout.html', {
                "cart_data": request.session['cart_data_obj'],
                'totalcartitems': len(request.session['cart_data_obj']),
                'cart_total_amount': cart_total_amount,
                "active_address": active_address
            })

    except Exception as e:
    # Log the full traceback
        import traceback
        traceback.print_exc()

    # Handle exceptions, log errors, or display an error message
        print(f"Error during checkout: {e}")
        messages.error(request, "An error occurred during checkout. Please try again.")
        return redirect("core:index")


@login_required
def razorpaycheck(request):
    cart_total_amount = request.session['cart_total_amount'] 

    print(cart_total_amount)
    return JsonResponse({
        'total_price': cart_total_amount 
    })



@login_required
def payment_completed_view(request):
    print("hello")
    try:
        cart_total_amount = request.session.get('cart_total_amount', 0)

        if 'cart_data_obj' in request.session:
            unpaid_orders = CartOrder.objects.filter(user=request.user, paid_status=False)
            order_id = request.session['order_id']
            unpaid_orders.update(id=order_id )
            if unpaid_orders.exists():
                unpaid_orders.update(product_status="processing", paid_status=True)

                if request.method == 'POST':
                    # Retrieve the payment_id from the POST data
                    payment_id = request.POST.get('payment_id')
                    payment_method = 'Razorpay'
                    # Assuming you want to update each order's payment_method and payment_id
                    unpaid_orders.update(payment_method=payment_method, payment_id=payment_id)
                else:
                    unpaid_orders.update(payment_method='Cod')


                del request.session['cart_data_obj']
                del request.session['cart_total_amount']
                del request.session['order_id']
                del request.session['coupon_id']
                

                return JsonResponse({"status": "Payment completed successfully"})  # Return a JSON response indicating success
            else:
                messages.error(request, "No unpaid orders found for the user.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error during payment completion: {e}")
        messages.error(request, "An error occurred during payment completion. Please try again.")
    
    return JsonResponse({"status": "Error during payment completion" })  # Return a JSON response indicating error


def CashOnDelivery(request):

    cart_total_amount = request.session.get('cart_total_amount', 0)
    if 'cart_data_obj' in request.session:
            unpaid_orders = CartOrder.objects.filter(user=request.user, paid_status=False)
            order_id = request.session['order_id']
            unpaid_orders.update(id=order_id )
            if unpaid_orders.exists():
                unpaid_orders.update(product_status="processing", paid_status=True)

                if request.method == 'POST':
                    payment_method = 'Cod'

                    del request.session['cart_data_obj']
                    del request.session['cart_total_amount']
                    del request.session['order_id']
                
                    
                    return redirect("core:dashboard")
                
                
    return HttpResponse("Cash on Delivery processed successfully")               

@csrf_exempt
def payment_failed_view(request):
    
    return render(request, 'core/payment-failed.html')


@csrf_exempt
def payment_invoice(request):
    
    return render(request, 'core/payment-completed.html')


@login_required
@user_passes_test(is_not_superuser)
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user = request.user).order_by('-id')
    address = Address.objects.filter(user=request.user)

    try:
        wallet = Wallet.objects.get(user=request.user)
        transactions = Transaction.objects.filter(wallet=wallet)
    except Wallet.DoesNotExist:
        # Handle the case where the Wallet does not exist for the user
        # You can create a new wallet for the user or redirect to a page with an error message
        # For simplicity, let's assume you want to create a new wallet for the user
        wallet = Wallet.objects.create(user=request.user, balance=0.0)
    

    orders =  CartOrder.objects.filter(user=request.user).annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month= [] 
    total_orders= []

    for d in orders:
        if 'month' in d and isinstance(d['month'], int):
            month.append(calendar.month_name[d['month']])
            total_orders.append(d['count'])
        else:
            # Handle the case where 'month' is not present or is not an integer
            # You might want to provide a default value or raise an exception
            month.append('Unknown')



    context = {
        "orders_list": orders_list,
        "address": address,
        "orders": orders,
        "month": month,
        "total_orders": total_orders,
        'wallet': wallet,
        'transactions': transactions,
    }
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile
            )
        messages.success(request, "Address Saved")
        return redirect("core:dashboard")

    return render(request, 'core/dashboard.html', context)




def order_detail(request, id):
    order = CartOrder.objects.get(user = request.user, id = id)
    products = CartOrderProducts.objects.filter(order = order)
    

    context = {
        'products': products,
        'order': order,
    }
    return render(request, 'core/order-detail.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})

# wishlist page
@login_required
def wishlist_view(request):
    wishlist = wishlist_model.objects.filter(user = request.user)
    context = {
        "wishlist":wishlist
    }
    return render(request, "core/wishlist.html", context)

    



def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    

    context = {}

    wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()
    

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = wishlist_model.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            "bool": True
        }

    return JsonResponse(context)


import json
from django.core.serializers import serialize

# remove wishlist
def Remove_wishlist(request):
    pid = request.GET['id']
    wishlist = wishlist_model.objects.filter(user=request.user)
    wishlist_d = wishlist_model.objects.get(id=pid)
    delete_product = wishlist_d.delete()
    
    context = {
        "bool":True,
        "wishlist":wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string('core/async/wishlist-list.html', context)
    return JsonResponse({'data':t,'w':wishlist_json})





from django.shortcuts import get_object_or_404, redirect

# Cancel Order
@login_required
@user_passes_test(is_not_superuser)
def cancel_product(request,id):
    order_product = get_object_or_404(CartOrder, id=id, user=request.user)

                  # Retrieve the associated CartOrder

    
    # Check if the product is cancelable (add your own conditions)
    if order_product.product_status == 'processing':
        order_product.product_status = 'canceled'
        order_product.save()
       
        # add amount  to customer wallet
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += order_product.price
        wallet.save()
         
    return redirect('core:dashboard')

#Return Order
@login_required
@user_passes_test(is_not_superuser)
def return_product(request,id):
    order_product = get_object_or_404(CartOrder, id=id, user=request.user)
    
    # Check if the product is returnable (add your own conditions)
    if order_product.product_status == 'delivered':
        order_product.product_status = 'returned'
        order_product.save()
        # Add logic for updating totals or other necessary actions

        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += order_product.price
        wallet.save()
         
        
    return redirect('core:dashboard')

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse

from core.utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict


@staff_member_required
def get_filter_options(request):
    grouped_purchases = CartOrder.objects.annotate(year=ExtractYear("order_date")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })



def get_sales_chart(request, year):
    purchases = CartOrder.objects.filter(order_date__year=year)
    grouped_purchases = purchases.annotate(item_price=F("price")).annotate(month=ExtractMonth("order_date"))\
        .values("month").annotate(average=Sum("price")).values("month", "average").order_by("month")

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Monthly Sales - Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(sales_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_per_customer_chart(request, year):
    purchases = CartOrder.objects.filter(order_date__year=year)
    grouped_purchases = purchases.annotate(item_price=F("price")).annotate(month=ExtractMonth("order_date"))\
        .values("month").annotate(average=Avg("price")).values("month", "average").order_by("month")

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(spend_per_customer_dict.keys()),
            "datasets": [{
                "label": "spend-per-customer -Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(spend_per_customer_dict.values()),
            }]
        },
    })


@staff_member_required
def payment_success_chart(request, year):
    purchases = CartOrder.objects.filter(order_date__year=year)

    return JsonResponse({
        "title": f"Payment success rate in {year}",
        "data": {
            "labels": ["Unsuccessful","Successful"],
            "datasets": [{
                "label": "payment-success-Amount ($)",
                "backgroundColor": [colorDanger,colorSuccess],
                "borderColor": [ colorDanger,colorSuccess],
                "data": [
                    purchases.filter(successful=True).count(),
                    purchases.filter(successful=False).count(),
                ],
            }]
        },
    })


@staff_member_required
def payment_method_chart(request, year):
    purchases = CartOrder.objects.filter(order_date__year=year)
    grouped_purchases = purchases.values("payment_method").annotate(count=Count("id"))\
        .values("payment_method", "count").order_by("payment_method")

    payment_method_dict = dict()

    for payment_method in CartOrder.PAYMENT_METHODS:
        payment_method_dict[payment_method[1]] = 0

    for group in grouped_purchases:
        payment_method_dict[dict(CartOrder.PAYMENT_METHODS)[group["payment_method"]]] = group["count"]

    return JsonResponse({
        "title": f"Payment method rate in {year}",
        "data": {
            "labels": list(payment_method_dict.keys()),
            "datasets": [{
                "label": "payment-method-Amount ($)",
                "backgroundColor": generate_color_palette(len(payment_method_dict)),
                "borderColor": generate_color_palette(len(payment_method_dict)),
                "data": list(payment_method_dict.values()),
            }]
        },
    })

@staff_member_required
def statistics_view(request):

    return render(request, "admin/statistics.html", {})