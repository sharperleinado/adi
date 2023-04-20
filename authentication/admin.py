from django.contrib import admin 
from .models import User 
from django.contrib.auth.admin import UserAdmin
from .models import Mobile

# Register your models here.



admin.site.register(User, UserAdmin)
admin.site.register(Mobile)