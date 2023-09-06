from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Engineer, Manager

admin.site.register(Manager)
admin.site.register(Engineer)