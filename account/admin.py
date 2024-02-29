from django.contrib import admin

from account.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']




admin.site.register(User,UserAdmin)

