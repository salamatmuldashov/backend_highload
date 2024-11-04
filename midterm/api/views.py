from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Product, Order
from rest_framework.response import Response
from django.core.cache import cache
from .tasks import process_order

from .serializers import ProductSerializer, OrderSerializer, UserRegistrationSerializer
from django.contrib.auth.models import User


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category') 
    serializer_class = ProductSerializer


    def get_queryset(self):
        cached_products = cache.get('product_list')
        if cached_products:
            return cached_products

        products = Product.objects.all()
        cache.set('product_list', products, timeout=60) 
        return products

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('product')
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        process_order.delay(order.id) 
        
        return Response(serializer.data, status=201)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

