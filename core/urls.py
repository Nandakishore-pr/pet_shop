from django.urls import path,include
from core import views
# from .views import checkout_view

app_name = "core"
urlpatterns = [
    path('',views.index,name='index'),
    path('product_list_by_category/<int:category_cid>/',views.product_list_by_category,name = 'product_list_by_category'),
    path('product_list_by_subcategory/<int:subcategory_sid>/', views.product_list_by_subcategory, name='product_list_by_subcategory'),
    path('product_list/',views.product_list,name='product_list'),
    path('product_detail/<int:product_pid>/', views.product_detail, name='product_detail'),
    path('all_products/', views.all_products, name='all_products'),
    path('all_products/<int:category_cid>/', views.sort_by_category, name='sort_by_category'),
    path('profile_view/',views.profile_view,name = 'profile_view'),
    path('password_change/',views.password_change,name="password_change"),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('add_address/',views.add_address,name='add_address'),
    path('delete_address/<int:address_id>/',views.delete_address,name='delete_address'),
    path('edit_address/<int:address_id>/',views.edit_address,name='edit_address'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease_quantity/<int:cart_item_id>/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase_quantity/<int:cart_item_id>/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('checkout/',views.checkout,name='checkout'),
    path('add_to_wishlist/<int:product_pid>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_from_wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cash_on_delivery/',views.cash_on_delivery,name='cash_on_delivery'),
    path('orders/',views.orders,name='orders'),
    path('search/', views.search_view, name='search_view'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment_complete/',views.payment_complete,name= 'payment_complete'),
    path('payment_failed',views.payment_failed,name='payment_failed'),


    path('order_checkout/',views.order_checkout,name='order_checkout'),
    path('return_product/<int:order_id>/',views.return_product,name='return_product'),
    path('user_wallet/',views.user_wallet,name='user_wallet'),
    path('user_coupons/',views.user_coupons,name='user_coupons'),

]