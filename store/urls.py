from django.urls import path

from . import views

app_name = 'store' # This is matched to the 'namespace' of the core urls.py...

urlpatterns = [   # Creating some URL patterns
    path('', views.all_products, name='all_products'), # all_products is a name of a ftn in views.py
    path('item/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
]