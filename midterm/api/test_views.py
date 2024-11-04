from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Product, Category, Order
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ProductViewSetTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.00,
            stock=50,
            category=self.category
        )
        self.url = reverse('product-list')

    def test_create_product(self):
        data = {
            'name': 'New Product',
            'description': 'New Product Description',
            'price': 200.00,
            'stock': 20,
            'category': self.category.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_product(self):
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 150.00,
            'stock': 30,
            'category': self.category.id,
        }
        response = self.client.put(reverse('product-detail', args=[self.product.id]), data, format='json',  content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_product(self):
        response = self.client.delete(reverse('product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class OrderViewSetTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.00,
            stock=50,
            category=self.category
        )
        self.user = User.objects.create_user(username='testuser', password='password')
        self.url = reverse('order-list') 

    def test_create_order(self):
        data = {
            'user': self.user.id,
            'product': self.product.id,
            'quantity': 2,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_orders(self):
        Order.objects.create(user=self.user, product=self.product, quantity=2) 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_order(self):
        order = Order.objects.create(user=self.user, product=self.product, quantity=2)  
        data = {
            'user': self.user.id,
            'product': self.product.id,
            'quantity': 3,
        }
        response = self.client.put(reverse('order-detail', args=[order.id]), data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_order(self):
        order = Order.objects.create(user=self.user, product=self.product, quantity=2) 
        response = self.client.delete(reverse('order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

