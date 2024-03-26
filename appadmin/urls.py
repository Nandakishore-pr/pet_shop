from django.urls import path
from appadmin import views

app_name = "appadmin"
urlpatterns = [
    path('',views.admin_index,name='admin_index'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('admin_category/',views.admin_category,name='admin_category'),
    path('admin_add_category/',views.admin_add_category,name='admin_add_category'),
    path('admin_delete_category/<int:category_id>/', views.admin_delete_category, name='admin_delete_category'),
    path('admin_edit_category/<int:category_id>/', views.admin_edit_category, name='admin_edit_category'),
    path('admin_subcategory/',views.admin_subcategory,name = 'admin_subcategory'),
    path('admin_add_subcategory/',views.admin_add_subcategory,name='admin_add_subcategory'),
    path('admin_delete_subcategory/<int:subcat_id>/', views.admin_delete_subcategory, name='admin_delete_subcategory'),
    path('admin_edit_subcategory/<int:subcat_id>/',views.admin_edit_subcategory,name = 'admin_edit_subcategory'),
    path('admin_product/',views.admin_product,name='admin_product'),
    path('admin_add_product/',views.admin_add_product,name="admin_add_product"),
    path('admin_edit_product/<int:pid>/',views.admin_edit_product,name="admin_edit_product"),
    path('admin_delete_product/<int:pid>/',views.admin_delete_product,name='admin_delete_product'),
    path("admin_user/",views.admin_user,name='admin_user'),
    path('admin_view_user/<str:username>/',views.admin_view_user,name = 'admin_view_user'),
    path('block_unblock_user/<str:username>/', views.block_unblock_user, name='block_unblock_user'),
    path('admin_order/',views.admin_order,name='admin_order'),
    path('update_order_status/<int:order_id>/',views.update_order_status,name='update_order_status'),
    path('admin_coupon/',views.admin_coupon,name='admin_coupon'),
    path('create_coupon/',views.create_coupon,name='create_coupon'),
    path('delete_coupon/<int:id>/',views.delete_coupon,name='delete_coupon'),
    path('banner/',views.banner,name= 'banner'),
    path('sales_report',views.sales_report,name='sales_report'),
    path('offres',views.offres,name='offres'),
    path('create_product_offer',views.create_product_offer,name='create_product_offer'),
]