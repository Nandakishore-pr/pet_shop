from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import logout,login,get_user_model
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from core.models import Category,Product,ProductImages,Subcategory,Order,OrderItem
# from core.forms import ProductEditForm,ProductImagesForm
from account.models import User
from django.contrib.auth.decorators import login_required




# Create your views here.


@never_cache
def admin_login(request):
    
        if request.method=='POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
       
            user = authenticate(request,username=email,password=password)
            if user is not None and user.is_active and user.is_superadmin:
                login(request,user)

                request.session['logged_in'] = True

                return HttpResponseRedirect(reverse('appadmin:admin_index'))
        return render(request, 'appadmin/admin_login.html')


def admin_index(request):
    if not request.user.is_authenticated:
        return redirect('appadmin:admin_login')
    
    return render(request, 'appadmin/admin_index.html')


def admin_logout(request):
    logout(request)
    messages.success(request,f'You logged out')
    return redirect('appadmin:admin_login') 



def admin_category(request):
     categories = Category.objects.all()
     context = {
          'categories':categories
     }
     return render(request,'appadmin/category/admin_category_list.html',context)

def admin_add_category(request):
    if request.method == 'POST':
        cat_name = request.POST.get('cname')
        
        
        is_blocked = request.POST.get('blocked') == 'on'

        cat_data = Category(cname=cat_name, is_blocked=is_blocked, image=request.FILES.get('image'))
        cat_data.save()

        return redirect('appadmin:admin_category')  

    return render(request, 'appadmin/category/admin_category.html')



def admin_delete_category(request, category_id):
   
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        
        category.delete()
        return redirect('appadmin:admin_category')  

    return render(request, 'appadmin/category/admin_delete_category.html', {'category': category})



def admin_edit_category(request, category_id):
    
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
       
        category.cname = request.POST.get('cname')
        category.is_blocked = request.POST.get('blocked') == 'on'
        
        category.image = request.FILES.get('image') if 'image' in request.FILES else category.image
        category.save()
        return redirect('appadmin:admin_category') 

    return render(request, 'appadmin/category/admin_edit_category.html', {'category': category})


def admin_subcategory(request):
    sub_cat = Subcategory.objects.all()
    context={
        'sub_cat':sub_cat
    }
    return render(request,'appadmin/subcategory/admin_subcategory_list.html',context)

def admin_delete_subcategory(request,subcat_id):
    subcat = get_object_or_404(Subcategory, sid=subcat_id)

    if request.method == 'POST':
        
        subcat.delete()
        return redirect('appadmin:admin_subcategory')  

    return render(request, 'appadmin/subcategory/admin_subcategory_delete.html', {'subcat': subcat})



def admin_edit_subcategory(request, subcat_id):
    # Get the subcategory instance to edit
    subcategory = get_object_or_404(Subcategory, sid=subcat_id)

    if request.method == 'POST':
        # Update subcategory fields based on form data
        subcategory.sub_name = request.POST.get('sub_name')
        subcategory.category = Category.objects.get(pk=request.POST.get('category'))
        subcategory.save()
        return redirect('appadmin:admin_subcategory')  # Redirect to the subcategory list after successful edit

    # Get all categories for the dropdown list
    categories = Category.objects.all()

    return render(request, 'appadmin/subcategory/admin_edit_subcategory.html', {'subcategory': subcategory, 'categories': categories})


def admin_add_subcategory(request):
    if request.method == 'POST':
        sub_name = request.POST.get('sub_name')
        category_id = request.POST.get('category')

        # Assuming you have a ForeignKey relationship between Subcategory and Category
        category = Category.objects.get(cid=category_id)

        # Create the subcategory
        Subcategory.objects.create(sub_name=sub_name, category=category)

        return redirect('appadmin:admin_subcategory')

    # Fetch available categories to display in the dropdown
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'appadmin/subcategory/admin_add_subcategory.html', context)

def admin_product(request):

    products = Product.objects.all()
    context={
        "products":products,
    }

    return render(request,'appadmin/product/admin_product_list.html',context)



def admin_add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.getlist('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        stock = request.POST.get('stock')
        
        # Checkboxes
        featured = request.POST.get('featured') == 'on'
        latest = request.POST.get('latest') == 'on'
        in_stock = request.POST.get('in_stock') == 'on'
        status = request.POST.get('status') == 'on'

        # Get the category and subcategory objects
        category = get_object_or_404(Category, cid=category_id)
        subcategory = get_object_or_404(Subcategory, sid=subcategory_id)

        # Create the product
        
        product = Product.objects.create(
                title=title,
                image=image[0],
                description=description,
                price=price,
                category=category,
                sub_category=subcategory,
                stock=stock,
                featured=featured,
                latest=latest,
                in_stock=in_stock,
                status=status,
            )
       
        for i in image:
                try:
                    ProductImages.objects.create(product=product, Image=i)
                except Exception as e:
                    print(e)

        messages.success(request, 'Product added successfully!')
        return redirect('appadmin:admin_product')
    
    # Fetch categories and subcategories for dropdowns
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()


    context = {
        'categories': categories,
        'subcategories': subcategories,
        
    }

    return render(request, 'appadmin/product/admin_add_product.html', context)





def admin_edit_product(request, pid):
    product = get_object_or_404(Product, pid=pid)
    product_images = ProductImages.objects.filter(product=product)

    if request.method == 'POST':
        # Update product details
        product.title = request.POST.get('title', product.title)
        product.description = request.POST.get('description', product.description)
        product.price = request.POST.get('price', product.price)
        product.old_price = request.POST.get('old_price', product.old_price)
        product.stock = request.POST.get('stock', product.stock)
        product.specifications = request.POST.get('specifications', product.specifications)
        product.category_id = request.POST.get('category')
        product.sub_category_id = request.POST.get('subcategory')
        # Handle image update
        new_image = request.FILES.get('image')
        print(new_image)
        if new_image:
            product.image = new_image
            
        # Update other fields as needed

        # Save changes
        product.save()

        return redirect('appadmin:admin_product')  # Redirect to product list or any other page after editing

    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    context = {
        'product': product,
        'categories': categories,
        'subcategories': subcategories,
        'product_images': product_images,
    }

    return render(request, 'appadmin/product/admin_edit_product.html', context)


def admin_delete_product(request, pid):
    # Get the product instance based on the pid field
    product = get_object_or_404(Product, pk=pid)

    if request.method == 'POST':
        # If the request method is POST, the user has confirmed the deletion
        product.delete()
        return redirect('appadmin:admin_product')  # Redirect to a product list view after deletion

    # If the request method is GET, display a confirmation page
    return render(request, 'appadmin/product/admin_delete_product.html', {'product': product})


def admin_user(request):
    users = User.objects.all().order_by('id')
    return render(request, 'appadmin/user/admin_user_list.html', {'users': users})



def admin_view_user(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
    }

    return render(request, 'appadmin/user/admin_view_user.html', context)



User = get_user_model()


@login_required
def block_unblock_user(request, username):
    user = get_object_or_404(User, username=username)

    # Toggle the is_active field to block or unblock the user
    user.is_active = not user.is_active
    user.save()

    # Display a success message based on the user's current status
    action = "blocked" if not user.is_active else "unblocked"
    messages.success(request, f'The user "{user.username}" has been {action} successfully.')

    # Redirect to the user details page
    return redirect('appadmin:admin_view_user', username=user.username)


def admin_order(request):
    users = User.objects.all()
    order_details = {}
    
    for user in users:
        orders = Order.objects.filter(user=user)
        user_order_details = []
        
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            order_info = {
                'order_id': order.id,
                'total_amount': order.total_amount,
                'shipping_address': order.shipping_address,
                'order_items': order_items,
                'status': order.status
            }
            user_order_details.append(order_info)
        
        order_details[user.username] = user_order_details
    
    status_choices = dict(Order.STATUS_CHOICES)

    context = {
        'order_details': order_details,
        'status_choices': status_choices 
    }


    return render(request, 'appadmin/orders/admin_orders.html', context)


def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('product_status')
        order = Order.objects.get(id=order_id)
        
        # Check if the order has already been canceled
        if order.status == 'cancelled':
            return HttpResponseBadRequest("Cannot update status for a canceled order.")
        
        # Proceed with updating the status for non-canceled orders
        order.status = new_status
        order.save()
        return redirect('appadmin:admin_order')
    else:
        return HttpResponseBadRequest("Only POST requests are allowed for this view.")




# def update_order_status(request, order_id):
#     if request.method == 'POST':
#         new_status = request.POST.get('product_status')
#         order = Order.objects.get(id=order_id)
#         order.status = new_status
#         order.save()
#     return redirect('appadmin:admin_order')


# def admin_order(request):
#     # Retrieve orders for the current user
#     user_orders = Order.objects.filter(user=request.user)

#     context = {
#         'user_orders': user_orders
#     }

#     return render(request, 'appadmin/orders/admin_orders.html', context)

# @login_required
# def update_order_status(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     if request.method == 'POST':
#         new_status = request.POST.get('new_status')
#         if new_status in dict(Order.STATUS_CHOICES):
#             order.status = new_status
#             order.save()
#             return redirect('appadmin:admin_order')
#     # context = {'order': order}
#     return redirect('appadmin:admin_order')