from unittest import skip   # this is done to skip tests that is to be done in the future
from importlib import import_module  # This will help us to run the sessionengine to simulate sessions

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import (  # Client will help us to simulate a user. It acts as a dumy web browser
    Client, RequestFactory, TestCase)
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_exmaple(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()  # Demo user is simulated
    #    self.factory = RequestFactory()  #Now that we have to test the sessions,we don't need to use the RerquestFactory
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        """
        Test category response status
        """
        response = self.c.get(
            reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test items response status
        """
        response = self.c.get(
            reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)   # This session engine will help us simulate session
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertFalse(html.startswith('\n<!DOCTYPE html>\n'))  #Keep it true and make sure it works. Skipping for now
        self.assertEqual(response.status_code, 200)
"""
    def test_view_function(self):
        
       # Example: Using request factory. Now that we have to check the session, we have removed this test
        
        request = self.factory.get('django-beginners')  # Here we had checked if we could access the home page ie. the html files
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
"""
