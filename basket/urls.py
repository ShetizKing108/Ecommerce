from django.urls import path

from . import views


app_name = 'basket'
""" 
 In the base template we have mentioned basket: 'basket_summary' which means to look for the app named 'basket' whose link is 'basket_summary'
 This name='basket_summary' gets its value from views.basket_summary
"""
urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update'),
]