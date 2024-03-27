from django.shortcuts import render,redirect
from core.models import Category,Product,Subcategory,ProductImages,Cart,CartItem,WishlistItem,Order,OrderItem,wallet,Coupon
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from account.forms import  UserProfileForm,AddressForm
from account.models import Profile,Address,User
from django.http import HttpResponseBadRequest,JsonResponse,HttpResponseRedirect,HttpResponse
from core.forms import ProductSearchForm,AddressSelectionForm
import json
from django.views.decorators.http import require_POST

from decimal import Decimal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


#PaymentOptionForm
# Create your views here.

def get_common_context():
    return {
        'categories': Category.objects.all(),
    }

def index(request):
    context = get_common_context()
    context.update({
        'featured_products': Product.objects.filter(featured=True),
        'latest_products': Product.objects.filter(latest=True),
    })
    return render(request, 'core/index.html', context)

def product_list(request, category_cid=None):
    context = get_common_context()
    
    if category_cid:
        category = get_object_or_404(Category, cid=category_cid)
        products = Product.objects.filter(category=category)
        subcategories = Subcategory.objects.filter(products__in=products).distinct()
    else:
        category = None
        products = Product.objects.all()
        subcategories = Subcategory.objects.all()

    context.update({
        'category': category,
        'products': products,
        'subcategories': subcategories,
    })

    return render(request, 'core/product_list.html', context)

def product_list_by_category(request, category_cid):
    category = get_object_or_404(Category, cid=category_cid)
    products = Product.objects.filter(category=category)
    product_count = products.count()
    
    context = get_common_context()
    context.update({
        'category': category,
        'products': products,
        'product_count': product_count,
        
    })
    return render(request, 'core/product_list.html', context)

def product_list_by_subcategory(request, subcategory_sid):
    subcategory = get_object_or_404(Subcategory, sid=subcategory_sid)
    products = Product.objects.filter(sub_category=subcategory)
    product_count = products.count()

    context = get_common_context()
    context.update({
        'subcategory': subcategory,
        'products': products,
        'product_count': product_count,
    })

    return render(request, 'core/product_list.html', context)


def product_detail(request,product_pid):
    product = get_object_or_404(Product, pid=product_pid)
    product_images = ProductImages.objects.filter(product=product)
    print(product_images)

    context = {
        'product': product,
        'product_images': product_images,
   
    }

    return render(request, 'core/product_detail.html',context)


def all_products(request, category_id=None):
    # Fetch all categories
    categories = Category.objects.all()
    print(category_id)
    # Get the selected category if provided
    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)

    # Filter products based on the selected category
    products = Product.objects.all()
    if selected_category:
        products = products.filter(category=selected_category)

    # Get the minimum and maximum price values from the request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on the price range
    if min_price and max_price:
        # Assuming price is a field in the Product model
        products = products.filter(price__gte=min_price, price__lte=max_price)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'core/all_products.html', context)




def sort_by_category(request,category_cid):
    categories = Category.objects.all()  # Fetch all categories
    selected_category = get_object_or_404(Category,cid=category_cid)

    products = Product.objects.filter(category = selected_category)
    

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,  # Pass selected category ID to template
    }

    return render(request,'core/all_products.html',context)

def profile_view(request):
    user = request.user
    # addresses = user.address_set.all()
    context = {
        'user':user,
        # 'address':addresses
    }
    return render(request, "core/profile.html",context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session with new password hash
            messages.success(request, 'Your password was successfully updated!')
            return redirect('core:profile_view')  # Redirect to profile page after successful password change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/change_password.html', {'form': form})


@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None

    # Check if the user has any addresses
    has_address = user.address_set.exists()

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        if profile:
            profile_form = UserProfileForm(request.POST, instance=profile)
        else:
            profile_form = UserProfileForm(request.POST)

        # Handle address form submission
        if not has_address:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, 'Address added successfully!')
                return redirect('core:profile_view')  # Redirect to user's profile page
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            address_form = None

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            if profile:
                profile_form.save()
            else:
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('core:profile_view')  # Redirect to user's profile page
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        user_form = UserProfileForm(instance=user)
        if profile:
            profile_form = UserProfileForm(instance=profile)
        else:
            profile_form = UserProfileForm()

        if not has_address:
            address_form = AddressForm()
        else:
            address_form = None

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
        'form': user_form,
        'form':address_form
    }

    return render(request, 'core/edit_profile.html', context)



def add_address(request):
    source = request.GET.get('source', None)
    
    if request.method == 'POST':
            
            # Extract address data from the form
            street_address = request.POST.get('street_address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            country = request.POST.get('country')
            

            # Assuming 'Address' is the model for storing addresses
            # Create a new address object and save it to the database
            Address.objects.create(
                user=request.user,
                street_address=street_address,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country
            )
            if source == 'profile_address':
                return redirect('core:profile_view')
            elif source == 'checkout_address':
                return redirect('core:checkout')
    return HttpResponse("Invalid request")
        
        


def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    # Check if the user is authorized to delete the address (optional)
    if request.user == address.user:
        address.delete()
    return redirect('core:profile_view')



def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    print(address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('core:profile_view')
        else:  
            print(form.errors) 
    else:
        form = AddressForm(instance=address)

    context = {
        'form':form,
        'address':address,
        'address_id':address_id,
    }
    return render(request, 'core/edit_address.html', context)

def cart_view(request):
    # Retrieve the user's cart if it exists
    user_cart = Cart.objects.filter(user=request.user).first()

    if user_cart:
        cart_items = user_cart.items.all()

        for cart_item in cart_items:
            cart_item.total_price = cart_item.product.price * cart_item.quantity
        total_cart_price = sum(cart_item.total_price for cart_item in cart_items)
    else:
        cart_items = []
        total_cart_price = 0

    context = {
          'cart_items': cart_items, 
          'total_cart_price': total_cart_price 
       }
    

    return render(request, "core/cart_view.html",context)
    
def add_to_cart(request):
    if request.method == 'GET':
        product_pid = request.GET.get('product_pid')
        if product_pid:
            try:
                product = Product.objects.get(pid=product_pid)

                user_cart, created = Cart.objects.get_or_create(user=request.user)
                cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=product)

                if item_created:
                    message = f"{product.title} added to cart"
                else:

                    message = f"{product.title} is already in your cart"

                return JsonResponse({'message': message})
            except Product.DoesNotExist:
                pass


    return HttpResponseBadRequest("Invalid request")


@require_POST
def remove_from_cart(request, cart_item_id):
    
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return JsonResponse({'message': 'Item removed from cart successfully'}, status=200)
    



def decrease_quantity(request, cart_item_id,cart_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        
        print(cart_item.quantity)
        total_price = cart_item.product.price * cart_item.quantity
        cart_item.save()
        print(total_price)

        all_products = CartItem.objects.filter(cart_id=cart_id)

        total_quantity = 0
        total = 0

        for cart_item in all_products:
            total_quantity += cart_item.quantity
            total += cart_item.product.price * cart_item.quantity
            print(total)

        return JsonResponse({'quantity': cart_item.quantity,'total':total_price,'total_sum':total}, status=200)
    else:
        return JsonResponse({'error': 'Quantity cannot be less than 1'}, status=400)
    
    
def increase_quantity(request, cart_item_id,cart_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    print(cart_item)

    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()
        
    

        total_price = cart_item.product.price * cart_item.quantity
        cart_item.save()

        all_products = CartItem.objects.filter(cart_id=cart_id)
       
        total = 0
        
        
        for cart_i in all_products:
            
            total += cart_i.product.price * cart_i.quantity
            
        
        return JsonResponse({'q': cart_item.quantity , 'total':total_price,'total_sum':total}, status=200)
    else:
        return JsonResponse({'msg':'This product is out of stock.'},status = 201),
   

def wishlist(request):
    wishlist_item = WishlistItem.objects.filter(user=request.user)

    return render (request,'core/wishlist.html',{'wishlist_item':wishlist_item})



def add_to_wishlist(request,product_pid):
    if request.method == 'POST':
        # Get the product based on the provided PID
        product = get_object_or_404(Product, pid=product_pid)

        # Check if the product is already in the user's wishlist
        if WishlistItem.objects.filter(user=request.user, product=product).exists():
            # Product already exists in the wishlist, return a message
            return JsonResponse({'message': 'Item already in the wishlist'}, status=400)
        else:
            # Add the product to the user's wishlist
            WishlistItem.objects.create(user=request.user, product=product)
            return JsonResponse({'message': 'Item added to wishlist successfully'}, status=200)
    else:
        # Handle invalid requests
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@require_POST
def remove_from_wishlist(request, item_id):
    # Get the wishlist item
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    
    # Delete the wishlist item
    wishlist_item.delete()
    
    # Return success response
    return JsonResponse({'message': 'Item removed from wishlist successfully'}, status=200)
    



def create_order(user, cart_items, total_cart_price, shipping_address_id):
    # Create a new order instance
    order = Order.objects.create(
        user=user,
        total_amount=total_cart_price,
        shipping_address_id=shipping_address_id
    )
    # Create order items for each cart item
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity
        )
    # Clear the user's cart after placing the order
    for item in user.cart.items.all():
        item.delete()





def payment_complete(request):
    return render(request, 'core/payment_complete.html')


def payment_failed(request):
    return render(request, 'core/payment_failed.html')



def cash_on_delivery(request):
    return render(request, 'core/order_placed.html')


def orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(pk=order_id,user=request.user)
            order.cancel_order()
        except Order.DoesNotExist:
            pass
        return redirect('core:orders')
    
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    
    for order in user_orders:
        
        order_items = OrderItem.objects.filter(order=order)

        order.product_details = []

        
        for order_item in order_items:
            product_detail = {
                'product_title': order_item.product.title,
                'quantity': order_item.quantity,
                # Include more product details if needed
            }
            order.product_details.append(product_detail)

    context = {
        'user_orders': user_orders
    }
    return render(request, 'core/orders.html', context)



def search_view(request):
    form = ProductSearchForm(request.GET)
    products = []

    if form.is_valid():
        query = form.cleaned_data['query']
        
        products = Product.objects.filter(title__icontains=query)

    return render(request, 'core/search_result.html', {'form': form, 'products': products})




def return_product(request,order_id):
    order = Order.objects.get(id=order_id)
    print(order)
    total_price = order.total_amount
    print(total_price)
    user = request.user

    wallet_instance, created = wallet.objects.get_or_create(user=user)

        
    wallet_instance.Amount += total_price
    wallet_instance.save()
    wal = get_object_or_404(wallet,user=request.user)
    return redirect('core:orders')
    

def user_wallet(request):
    # Retrieve the wallet object associated with the user
    wallet_obj = get_object_or_404(wallet, user=request.user)
    
    # Retrieve canceled orders associated with the user
    returned_orders = Order.objects.filter(user=request.user, status='delivered')
    
    
    
    returned_amount = 0
    returned_orders_details = []
    for order in returned_orders:
        order_items = OrderItem.objects.filter(order=order)
        print(order_items)
        for item in order_items:
            
            total_product_price = item.product.price * item.quantity
            
            returned_orders_details.append({
                'product': item.product,
                'quantity': item.quantity,
                'total_product_price':total_product_price
            })
        
            returned_amount += total_product_price
        

    context = {
        'wallet': wallet_obj,
        'return_orders': returned_orders_details,
        'returned_amount': returned_amount,
    }
    
    return render(request, 'core/wallet.html', context)



def user_coupons(request):
    coupons = Coupon.objects.all
    return render(request, 'core/coupons.html',{'coupons':coupons}) 







def checkout(request):
    user = request.user
    user_cart = Cart.objects.filter(user=user).first()
    form = AddressSelectionForm(user)
    total_cart_price = Decimal(0)
    cart_items = []
    order = None
    
    if user_cart:
        cart_items = user_cart.items.all()
        for cart_item in cart_items:
            cart_item.total_price = cart_item.product.price * cart_item.quantity
            total_cart_price += cart_item.total_price
    print(total_cart_price)


    if request.method == 'POST':

        if 'coupon_code' in request.POST:
            coupon_code = request.POST.get('coupon_code')
            coupon = Coupon.objects.filter(code=coupon_code).first()

            if coupon:
                discount_amount = total_cart_price * (coupon.discount / Decimal(100))
                total_cart_price -= discount_amount
                print(total_cart_price)
                message = messages.success(request, f"Coupon '{coupon.code}' applied successfully!")
            else:
                messages.error(request, "Invalid coupon code!")

        
            host = request.get_host()
            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': total_cart_price,
                'item_name': "Order-Item-No-908210002", 
                'invoice': "INVOICE_NO-908210002" ,
                'currency_code': "USD",
                'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
                'return_url': 'http://{}{}'.format(host, reverse("core:payment_complete")),
                'cancel_url': 'http://{}{}'.format(host, reverse("core:payment_failed")),
            }
            paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

            context = {
                'form': form,
                'cart_items': cart_items,
                'total_cart_price': total_cart_price,
                'paypal_payment_button': paypal_payment_button,
                
            }
            
            return render(request, 'core/checkout.html', context)

        elif 'selected_address_id' in request.POST:

            shipping_address_id = request.POST.get('selected_address_id')
            order = Order.objects.create(
                        user=user,
                        total_amount=total_cart_price,
                        shipping_address_id=shipping_address_id
                    )
            
            print(total_cart_price)
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )
            
            for item in user_cart.items.all():
                item.delete()
    # order_no = Order.objects.get(pk=order.pk)
    
    
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_cart_price,
        'item_name': "Order-Item-No-908210002" ,
        'invoice': "INVOICE_NO-908210002" ,
        'currency_code': "USD",
        'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("core:payment_complete")),
        'cancel_url': 'http://{}{}'.format(host, reverse("core:payment_failed")),
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
        'paypal_payment_button': paypal_payment_button,
    }
    
    return render(request, 'core/checkout.html', context)   




