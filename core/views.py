from django.shortcuts import render,redirect
from core.models import Category,Product,Subcategory,ProductImages,Cart,CartItem,WishlistItem,Order,OrderItem
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from account.forms import  UserProfileForm,AddressForm
from account.models import Profile,Address,User
from django.http import HttpResponseBadRequest,JsonResponse
from core.forms import AddressSelectionForm,PaymentOptionForm


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


    context = {
        'product': product,
        'product_images': product_images,
   
    }

    return render(request, 'core/product_detail.html',context)


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



# @login_required
# def edit_profile(request):
#     user = request.user
#     try:
#         profile_instance = user.profile
#     except Profile.DoesNotExist:
#         # If profile doesn't exist, create one
#         profile_instance = Profile.objects.create(user=user)

#     # Get the address instance for the current user
#     address_instance = None
    
#     try:
#         address_instances = Address.objects.filter(user=user)
#         address_instance = address_instances.first() if address_instances.exists() else None
#     except Address.DoesNotExist:
#         address_instance = None


#     if request.method == 'POST':
#         # Create form instances and populate them with data from the request
#         profile_form = UserProfileForm(request.POST, instance=profile_instance)

#         if address_instance:
#             address_form = AddressForm(request.POST, instance=address_instance)
#         else:
#             address_form = AddressForm(request.POST)

#         # Check if the forms are valid
#         if profile_form.is_valid() and (not address_instance or address_form.is_valid()):
#             # Save the form data to the database
#             profile_form.save()
#             address = address_form.save(commit=False)
#             address.user = user  # Set the user for the address instance
#             address.save()
#             # Redirect to a success page
#             return redirect('core:profile_view')  

#     else:
#         # If it's a GET request, create form instances with initial data
#         profile_form = UserProfileForm(instance=profile_instance)
#         if address_instance:
#             address_form = AddressForm(instance=address_instance)
#         else:
#             address_form = AddressForm()

#     context = {
#         'profile_form': profile_form,
#         'address_form': address_form,
#         'has_address':address_instance is not None,
#     }

#     return render(request, 'core/edit_profile.html', context)



# @login_required
# def edit_profile(request):
#     user = request.user
#     try:
#         profile = user.profile
#     except Profile.DoesNotExist:
#         profile = None

#     if request.method == 'POST':
#         user_form = UserProfileForm(request.POST, instance=user)
#         if profile:
#             profile_form = UserProfileForm(request.POST, instance=profile)
#         else:
#             profile_form = UserProfileForm(request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             if profile:
#                 profile_form.save()
#             else:
#                 profile = profile_form.save(commit=False)
#                 profile.user = user
#                 profile.save()
#             messages.success(request, 'Your profile has been updated successfully!')
#             return redirect('core:profile_view')  # Redirect to user's profile page
#         else:
#             messages.error(request, 'Please correct the errors below.')

#     else:
#         user_form = UserProfileForm(instance=user)
#         if profile:
#             profile_form = UserProfileForm(instance=profile)
#         else:
#             profile_form = UserProfileForm()

#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form
#     }

#     return render(request, 'core/edit_profile.html', context)




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
    if request.method == 'POST':
        
        # Extract address data from the form
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        print(street_address)

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

    return redirect('core:profile_view')


def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    # Check if the user is authorized to delete the address (optional)
    if request.user == address.user:
        address.delete()
    return redirect('core:profile_view')



def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
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
                # Assuming you have a view function to retrieve the product based on product_pid
                product = Product.objects.get(pid=product_pid)

                # Get or create the user's cart
                user_cart, created = Cart.objects.get_or_create(user=request.user)

                # Check if the item is already in the cart
                cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=product)

                if item_created:
                    # Item is added to cart
                    message = f"{product.title} added to cart"
                else:
                    # Item is already in the cart
                    message = f"{product.title} is already in your cart"

                # Redirect to the product detail view with the appropriate product_pid
                return JsonResponse({'message': message})
            except Product.DoesNotExist:
                pass

    # Handle invalid requests or errors
    return HttpResponseBadRequest("Invalid request")


def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed from cart successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        
        # Update total price
        cart_item.total_price = cart_item.product.price * cart_item.quantity
        cart_item.save()

        return JsonResponse({'quantity': cart_item.quantity}, status=200)
    else:
        return JsonResponse({'error': 'Quantity cannot be less than 1'}, status=400)
    
    
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    # Increase the quantity
    cart_item.quantity += 1
    cart_item.save()
    
    # Update total price
    cart_item.total_price = cart_item.product.price * cart_item.quantity
    cart_item.save()

    return JsonResponse({'quantity': cart_item.quantity}, status=200)

def wishlist(request):
    wishlist_item = WishlistItem.objects.filter(user=request.user)
    return render (request,'core/wishlist.html',{'wishlist_item':wishlist_item})



# def add_to_wishlist(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         product_pid = data.get('product_pid')
#         if product_pid is None:
#             return JsonResponse({'error': 'Product PID is required'}, status=400)
        
#         product = get_object_or_404(Product, pid=product_pid)
#         # Check if the product is already in the user's wishlist
#         if WishlistItem.objects.filter(user=request.user, product=product).exists():
#             # Product already exists in the wishlist, return a message
#             return JsonResponse({'message': 'Item already in the wishlist'}, status=400)
#         else:
#             # Add the product to the user's wishlist
#             WishlistItem.objects.create(user=request.user, product=product)
#             return JsonResponse({'message': 'Item added to wishlist successfully'}, status=200)
#     else:
#         # Handle invalid requests
#         return JsonResponse({'error': 'Invalid request method'}, status=400)


# def checkout_view(request):
#     if request.method == 'POST':
        
#         return redirect('core:order_placed')

#     user_addresses = Address.objects.filter(user=request.user)
    
#     # Retrieve the user's cart if it exists
#     user_cart = Cart.objects.filter(user=request.user).first()

#     total_cart_price = 0
#     cart_items = []
#     if user_cart:
#         cart_items = user_cart.items.all()
#         # Calculate the total price of all cart items
#         total_cart_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    
#     context = {
#         'user_addresses': user_addresses,
#         'total_cart_price': total_cart_price,
#         'cart_items':cart_items,
#     }
    
#     return render(request, 'core/checkout.html', context)


@login_required
def checkout_view(request):
    user = request.user
    user_addresses = Address.objects.filter(user=user)
    user_cart = Cart.objects.filter(user=user).first()

    total_cart_price = 0
    cart_items = []
    if user_cart:
        cart_items = user_cart.items.all()
        # Calculate the total price of all cart items
        total_cart_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    address_form = AddressSelectionForm(user=user)
    payment_form = PaymentOptionForm()

    if request.method == 'POST':
        address_form = AddressSelectionForm(user=user, data=request.POST)
        payment_form = PaymentOptionForm(request.POST)
        if address_form.is_valid() and payment_form.is_valid():
            shipping_address_id = address_form.cleaned_data['shipping_address'].id
            payment_option = payment_form.cleaned_data['payment_option']

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
            for item in user_cart.items.all():
                item.delete()

            # Redirect to the order placed page
            return redirect('core:order_placed')
        else:
            messages.error(request, "Please fill in all the required fields.")

    context = {
        'address_form': address_form,
        'payment_form': payment_form,
        'total_cart_price': total_cart_price,
        'cart_items': cart_items,
    }

    return render(request, 'core/checkout.html', context)

def order_placed(request):
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
    # Retrieve the user's orders ordered by creation time
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Iterate through each order and fetch associated order items
    for order in user_orders:
        # Fetch all order items related to the current order
        order_items = OrderItem.objects.filter(order=order)

        # Create a list to store product details and quantities for the current order
        order.product_details = []

        # Iterate through each order item to retrieve product details and quantities
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


