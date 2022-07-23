from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def categories(request):
    return {
        'categories': Category.objects.all() # In the dropdown all the categories will be returned/displayed
    }


def all_products(request): # This is to display our produts in the DB on the home page. 
    products = Product.objects.all()  #It is equivalent to SQL query 'SELECT ALL FROM PRODUCTS'. This will grab the data
    return render(request, 'store/home.html', {'products': products}) # MAking the above data available(render) on home page(template).
    # 'products' will be referring to the data stored in the variable products(ie. Product.objects.all()) 'objects.all()' retreives all the data


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product': product})