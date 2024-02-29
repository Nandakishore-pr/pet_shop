from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
  def create_user(self,first_name,last_name,username,email,password=None):
    if not email:
      raise ValueError('User must an email address')
    
    if not username:
      raise ValueError('User must have a username')

    user = self.model(
      email = self.normalize_email(email),
      username = username,
      first_name = first_name,
      last_name = last_name     
    )
    user.set_password(password)
    user.save(using =self.db)
    return user
  
  def create_superuser(self,first_name,last_name,username,email,password=None):
    user = self.create_user(
      email = self.normalize_email(email),
      username=username, 
      password=password,
      first_name=first_name,
      last_name=last_name,
    )
    user.is_admin = True
    user.is_active = True
    user.is_staff = True
    user.is_superadmin = True
    user.save(using = self.db)
    return user


class User(AbstractBaseUser,PermissionsMixin):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=100, unique=True)
  email = models.EmailField(max_length=100, unique=True)
  phone_number = models.CharField(max_length=12,blank=True)
  



  #required field

  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now_add=True)
  is_admin = models.BooleanField(default =False)
  is_staff = models.BooleanField(default =True)
  is_active = models.BooleanField(default =True)
  is_superadmin = models.BooleanField(default =False)


  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name','last_name']
  objects = UserManager()

  groups = models.ManyToManyField(Group, blank=True, related_name='account_user_groups')
    
    # update the related_name for user_permissions
  user_permissions = models.ManyToManyField(Permission,blank=True, related_name='account_user_permissions')

  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None):
        return self.is_admin

  
  def has_module_perms(self,app_label):
    return True




class Userform(models.Model):
  # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  username = models.CharField(null=True, max_length=100)
  email = models.EmailField(null=True)
  password = models.CharField(null=True, max_length=255)

  def __str__(self):
    return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} - {self.postal_code}"
