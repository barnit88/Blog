from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class AdminSite(UserAdmin):    
   
    list_display = ('email' , 'name' , 'date_joined' ,'last_login' ,'is_staff' ,'is_admin')
    search_fields = ('name' , 'email')
    ordering = ('name', 'email')
    list_filter = ()
    fieldsets = (
       
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
        ('Personal' , {'fields': ('name' , 'contact')}),
        ('Permissions', {'fields': ('is_staff','is_superuser','is_admin', 'is_active')}),
    )
    filter_horizontal = ()


admin.site.register(Account , AdminSite)

