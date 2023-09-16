from django.contrib import admin
from .models import Regions, EmployeePosition, Objects

# Регистрируем модель Regions
@admin.register(Regions)
class RegionsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    list_per_page = 20  # Количество объектов на странице

    # Дополнительные настройки, если необходимо

# Регистрируем модель EmployeePosition
@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    list_per_page = 20  # Количество объектов на странице

    # Дополнительные настройки, если необходимо
@admin.register(Objects)
class ObjectsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    list_per_page = 20  # Количество объектов на странице