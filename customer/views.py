from rest_framework.viewsets import GenericViewSet 
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin,UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response 
from django.shortcuts import render

from customer.models import Customer
from customer.serializers import CustomerSerializer

# Create your views here.
class CustomerVeiwSet(ListModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      GenericViewSet):
    serializer_class = CustomerSerializer 
    queryset = Customer.objects.all()

    @action(detail=False, methods=['get','put'])
    def me(self,request):
        customer = Customer.objects.get(user_id=request.user.id) 
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        else:
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


