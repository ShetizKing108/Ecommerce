from django.contrib import admin

from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # we are extending from Admin to ModelAdmin
    list_display = ['name', 'slug']  # these are the two things that we want to be displayed for the admin
    prepopulated_fields = {'slug': ('name',)}  # Slug will be populated with what we have typed into the name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'price',
                    'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}
