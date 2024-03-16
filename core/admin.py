from django.contrib import admin
from django.utils.safestring import mark_safe
from core.models import Category,Subcategory,Product,ProductImages
# Register your models here.



class ProductImagesAdmin(admin.TabularInline):
  model = ProductImages
  
class ProductAdmin(admin.ModelAdmin):
  inlines = [ProductImagesAdmin]
  list_display = ['pid','title','display_image','price','category','sub_category','featured','latest','status','stock',]
  
  
  def display_image(self, obj):
        if obj.image:  # Assuming 'image' is the field storing the image URL
            return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        else:
            return "No Image"
  display_image.allow_tags = True
  display_image.short_description = 'Image'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cid','cname','category_image']
    
    def category_image(self, obj):
        return mark_safe('<img src= "%s" width = "50" height = "50"/>' %(obj.image.url))

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['sid','sub_name','category']



admin.site.register(Subcategory,SubcategoryAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)