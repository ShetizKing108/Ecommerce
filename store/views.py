# Create your views here.
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_all(request):  # This is to display our produts in the DB on the home page.
    products = Product.products.all()  # Product.objects.all() is equivalent to SQL query 'SELECT ALL FROM PRODUCTS'. This will grab the data
    return render(request, 'store/home.html', {'products': products})  # MAking the above data available(render) on home page(template).
    # 'products' will be referring to the data stored in the variable products(ie. Product.objects.all()) 'objects.all()' retreives all the data


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):  # This will display our individual products(Books). The request ia the http request and slug attribute is as requested by user received through url
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    """
    get_object will retrieve data from the DB. 
    when we say slug=slug, it passes on the value received from the url(second slug ie.value) to the first slug(ie.variable). 
    The get_object is used to retrieve that product detail from the dataBase where slug variable (that holds the slugfield) 
    matches the slug received through url(slug recieved from user) and passed on to the slug variable above. 
    Product coz we want Product data whic is stored in the model class called 'Product'.
    This value of the product received through get_object is stored in the product variable and rendered to the template as below.
    """
    return render(request, 'store/products/single.html', {'product': product})