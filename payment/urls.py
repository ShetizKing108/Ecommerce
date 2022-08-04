from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.BasketView, name='basket'),
    # path('error/', views.Error.as_view(), name='error'),
    # path('orderplaced/', views.order_placed, name='order_placed'),
    # path('webhook/', views.stripe_webhook),
]