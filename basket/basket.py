# Here we will be modelling the basket, add functionalities and call the same from the views.py

from decimal import Decimal

from store.models import Product

from django.conf import settings


class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):  # __init__ ftn is added so that whatever page the user may visit this ftn will be called and session will be created
        self.session = request.session  # The session info is contained within the http request. Hence we do requet.session to grab that data.
        basket = self.session.get('skey')   # We will use skey(session key) to check in the browser if the user has visited us before
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}  # if there is no session key we will initiate an empty basket. The assignment used here is called 'chained assignment'
        self.basket = basket  # If user already has a key and has some items in the basket, we will set the value to what it was
        """
        Becaue we want this to be available on all the pages, we will go ahead and create a context processor and add it to the settings.        
        """
    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:  # basket contains the session info. So we are checking if the product_id collected from user matches with the product.id in their basket
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}  # Price is got from the model.py file Project class. So if the product id doesn't exist, we will create it and add the price.

        self.save()

    def __iter__(self):  # we are making this class iterable so that we can grab the data from DB
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()  # here product id is the key()
        products = Product.products.filter(id__in=product_ids)  # From DB Product, we are getting products(that which is active) and grab the ones whose product id is equal to session id(collected from browser?)
        basket = self.basket.copy()  # we have made a copy of the basket info

        for product in products:    # We are going to loop through each product added and add some data 'product' into it
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())   # The number of items added will be saved in the basket

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()
    
    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True   # Instead of writting "self.session.modified = True" each time we created a ftn and call it when required.





""" 
Code in this file has been inspried/reworked from other known works. Plese ensure that
the License below is included in any of your work that is directly copied from
this source file.


MIT License

Copyright (c) 2019 Packt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
"""
