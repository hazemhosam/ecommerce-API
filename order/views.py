from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from rest_framework import status
from customer.models import Customer
from rest_framework.filters import OrderingFilter
from order.serializers import OrderCreateSerializer, OrderSerializer, OrderUpdateSerializer
from rest_framework import permissions 

from .models import Order, OrderItem
from django.shortcuts import render

# Create your views here.
class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete',
                         'head','options']
    filter_backends = [OrderingFilter]
    ordering_fields = ['placed_at']
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [permissions.IsAdminUser()] 
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)


    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data,
                                            context={'user_id':
                                                     request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        return OrderSerializer 
