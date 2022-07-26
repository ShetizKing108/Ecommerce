from django.urls import path

from . import views

app_name = 'store'  # This is matched to the 'namespace' of the core urls.py...

urlpatterns = [    # Creating some URL patterns. The URL that comes from the browser is matched with these patterns and redirected to corresponding view function
    path('', views.product_all, name='product_all'),   # product_all is a name of a ftn in views.py. This line calls that particular function
    path('<slug:slug>', views.product_detail, name='product_detail'),   #The first slug refers to the variable which stores the value received when user clicks on a product and second slug is the value recieved from the browser(user)
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),  #we are creating a new area called search(like item in previous case) followed by slug
]
"""
Here it retrieves the value of that slug/url which is generated when the user clicks on a particular item and matches it with the expected 
values (urlpatterns) that we have stored. If matched it passes on the value(of slug) to the views.py
"""