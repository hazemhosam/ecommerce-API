from django.http import HttpResponse
import stripe
from django.conf import settings 
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import  Response
from rest_framework import status
from django.shortcuts import render

from order.models import Order
from payment.serializers import PaymentSerializer
from rest_framework import status

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'process_payment':
            return PaymentSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['post'])
    def process_payment(self, request):
        seriailizer = PaymentSerializer(data=request.data) 
        seriailizer.is_valid(raise_exception=True)
        order_id = seriailizer.validated_data['order_id'] 
        order = Order.objects.prefetch_related('items__product')\
                .get(id=order_id) 
        total_price = sum(item.product.price * item.quantity
                           for item in order.items.all())
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Order #{order.id}',
                    },
                    'unit_amount': int(total_price * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success_payment/'),  # Redirect after successful payment
            cancel_url=request.build_absolute_uri('/faild_payment/'),    # Redirect if payment is canceled
            metadata={'order_id': order.id},
        )

        return Response({'session_id': session.id, 'url': session.url}, status=status.HTTP_201_CREATED) 
    
        
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    event = None
    print(payload)
    print(sig_header)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)  # Invalid signature


    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.metadata.get('order_id')    

        # Update the order status to 'confirmed'
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'C'  # Confirmed
            order.save()
        except Order.DoesNotExist:
            return HttpResponse(status=404)  # Order not found

    return HttpResponse(status=200)
