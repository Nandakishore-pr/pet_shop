from django.contrib import admin
from django.utils.html import mark_safe
from django.conf import settings
from django.contrib.auth import get_user_model


from core.models import Category,Subcategory,Product,ProductImages
# Register your models here.



class ProductImagesAdmin(admin.TabularInline):
  model = ProductImages
  
class ProductAdmin(admin.ModelAdmin):
  inlines = [ProductImagesAdmin]
  list_display = ['pid','title','product_image','price','category','sub_category','featured','latest','status','stock',]



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cid','cname','category_image']
    
    def category_image(self, obj):
        return mark_safe('<img src= "%s" width = "50" height = "50"/>' %(obj.image.url))

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['sid','sub_name','category']



admin.site.register(Subcategory,SubcategoryAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)