from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render

from store.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)   # here we are instanciating the object of the class Basket
    return render(request, 'basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)  # We are creating an Object and here we are grabing the session data from the class Basket and savig it in a the variable basket. 
    if request.POST.get('action') == 'post':    # We are ensuring that the request received from AJAX is POST
        product_id = int(request.POST.get('productid'))   # Here we are grabbing the productid from the single.html
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)  # Using the product ID we are retrieving the data from DB
        basket.add(product=product, qty=product_qty)  # We are sending some data to the add function of view.py so that it performs necessary action.

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})   # 
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':    # Getting details from ajax request data
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)    # We just need the product id unlike previous case where we needed the qty as well

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        # print(product_id)  # Whenever we update our basket, we can check if it working right as the values are printed on the terminal
        # print(product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
