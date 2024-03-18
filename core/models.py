from django.db import models
from django.utils.safestring import  mark_safe
from account.models import User,Address

# Create your models here.


# def user_directory_path(instance, filename):
#     if instance.user and instance.user.id:
#         return 'user_{0}/{1}'.format(instance.user.id, filename)
#     else:
#         # Handle the case when user or user.id is None
#         return 'user_unknown/{0}'.format(filename)


def generic_directory_path(instance,filename):
    model_name = instance.__class__.__name__.lower()

    pk = instance.pid if hasattr(instance,'pid') else None

    if pk:
        return f'{model_name}_{pk}/{filename}'
    else:
        return f'{model_name}_unknown/{filename}'
    


class Category(models.Model):
    cid = models.BigAutoField(unique=True,primary_key=True)
    cname = models.CharField(max_length = 50)
    image = models.ImageField(upload_to='category',default='category.jpg')
    is_blocked = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        else:
            return "NO Image Available"

    def __str__(self):
        return self.cname
class Subcategory(models.Model):
    sid = models.BigAutoField(unique=True, primary_key = True)
    sub_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="subcategories",db_column = 'cid')

    def __str__(self):
        return self.sub_name
    


class Product(models.Model):
  pid = models.BigAutoField(unique =True,primary_key = True)
#   user = models.ForeignKey(User, on_delete = models.CASCADE,null =True)
  category = models.ForeignKey(Category, on_delete = models.CASCADE,null = True, related_name ="category")
  sub_category = models.ForeignKey(Subcategory, on_delete = models.CASCADE,null = True, related_name ="sub_category")
  title = models.CharField(max_length = 100,default = "product")
  image = models.ImageField(upload_to= generic_directory_path, default = "product.jpg")
  description = models.TextField(max_length = 400,null =True, blank =True, default = "This is the product")
  
  price = models.DecimalField(max_digits =10, decimal_places =2, default = 1.99 )
  old_price = models.DecimalField(max_digits =10, decimal_places =2, default = 2.99)
  stock = models.IntegerField(default=1)
  specifications = models.TextField(max_length = 400,null =True, blank =True)
  # tags = models.ForeignKey(Tags, on_delete = models.SET_NULL, null =True)
  
  
  
  status = models.BooleanField(default=True)
  in_stock = models.BooleanField(default=True)
  featured = models.BooleanField(default=False)
  latest = models.BooleanField(default=False)  
  related = models.ManyToManyField('self',blank=True)

#   sku = models.BigIntegerField(unique =True)
  date = models.DateTimeField(auto_now_add =True)
  updated = models.DateTimeField(null=True, blank=True)

  class Meta:
    verbose_name_plural = "Products"
    
  def product_image(self):
    return mark_safe('<img src= "%s" width="50" height= "50" />' % (self.image.url))
  
  def __str__(self):
      return self.title
    
  def get_percentage(self):
    new_price = (self.price /self.old_price) * 100
    return new_price


class ProductImages(models.Model):
  image = models.ImageField(upload_to=generic_directory_path, default = "product.jpg")
  product = models.ForeignKey(Product, related_name="p_images", on_delete = models.SET_NULL,null =True)
  date = models.DateField(auto_now_add =True)





class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # total_price = models.PositiveIntegerField()

    def product_image(self):
        # Assuming you want to retrieve the first image of the product
        first_image = self.product.p_images.first()
        if first_image:
            return first_image.Images.url
        return None

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in {self.cart}"
    
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
        unique_together = ['user', 'product']

    def __str__(self):
        return f'{self.user.username} - {self.product.title}'
    

class Order(models.Model):
    CANCELED = 'canceled'
    PROCESSING = 'processing'
    SHIPPED = 'Shipped'
    DELIVERD = 'Delivered'
    
    
    STATUS_CHOICES = [
        (CANCELED, 'Canceled'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERD, 'Delivered'),
        
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Product', through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROCESSING)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"
    
    def cancel_order(self):
        if self.status != self.CANCELED:
            self.status = self.CANCELED
            self.save()
            return True
        return False
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"Order #{self.order.pk} - {self.product.title} - Quantity: {self.quantity}"