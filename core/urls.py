from django.urls import path
from core import views

app_name = "core"
urlpatterns = [
    path('',views.index,name='index'),
    path('product_list_by_category/<int:category_cid>/',views.product_list_by_category,name = 'product_list_by_category'),
    path('product_list_by_subcategory/<int:subcategory_sid>/', views.product_list_by_subcategory, name='product_list_by_subcategory'),
    path('product_list/',views.product_list,name='product_list'),
    path('product_detail/<int:product_pid>/', views.product_detail, name='product_detail'),
    path('all_products/', views.all_products, name='all_products'),
    # path('all_products/<int:category_id>/', views.sort_by_category, name='sort_by_category'),
    path('profile_view/',views.profile_view,name = 'profile_view'),
    path('password_change/',views.password_change,name="password_change"),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('add_address/',views.add_address,name='add_address'),
    path('delete_address/<int:address_id>/',views.delete_address,name='delete_address'),
    path('edit_address/<int:address_id>/',views.edit_address,name='edit_address'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase_quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('checkout_view/',views.checkout_view,name='checkout_view'),
    path('add_to_wishlist/<int:product_pid>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_from_wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('order_placed/',views.order_placed,name='order_placed'),
    path('orders/',views.orders,name='orders'),
    path('search/', views.search_view, name='search_view'),

]