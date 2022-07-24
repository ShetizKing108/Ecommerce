from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket': basket})
