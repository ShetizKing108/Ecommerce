from .basket import Basket


def basket(request):
    return {'basket': Basket(request)}  # Basket(request) return the default data that gets initialized in the Basket class __init__() method