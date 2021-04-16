from django.shortcuts import render
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from payment.models import Invoice
from .serializer import InvoiceSerializer
from django.http import JsonResponse
import stripe
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import uuid
from django.utils.text import slugify

stripe.api_key = settings.STRIPE_SECRET_KEY


# Creating short link for payment
def create_short_link(self, invoice_id):
    domain = self.request.scheme + "://" + self.request.META['HTTP_HOST']
    header = {
        "Authorization": "Bearer fb89bf0ea1bee03de72dad0a93469d1c5622511b",
        "Content-Type": "application/json"
    }
    long_url = domain + "/proceed-to-pay/" + invoice_id + "/"
    params = {
        "long_url": long_url
    }
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", json=params, headers=header)
    data = response.json()
    if 'link' in data.keys():
        short_link = data['link']
    else:
        short_link = None
    return short_link


# Invoice creation view with payment link
class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        try:
            invoice_id = serializer.validated_data.get('invoice_id')
            short_link = create_short_link(self, invoice_id)
            serializer.save(short_link=short_link)
        except:
            short_link = None
            serializer.save(short_link=short_link)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            'code': 200,
            'status': "Invoice Created Successfully",
        }
        data['response'] = serializer.data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

# class CheckoutViewSet(ModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer
#     # permission_classes = [IsAdminUser]

#     def retrieve(self, request, *args, **kwargs):
#         invoice = self.get_object()
#         serializer = self.get_serializer(invoice)
#         invoice = Invoice.objects.get(invoice_id=invoice)
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount': invoice.amount,
#                         'product_data': {
#                             'name': invoice.invoice_id,
#                             # 'images': ['https://i.imgur.com/EHyR2nP.png'],
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             metadata={
#                 "invoice_id": invoice.invoice_id
#             },
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return JsonResponse({
#             'id': checkout_session.id
#         })
# data = {
#     'code': 200,
#     'status': "OK",
# }
# data['response'] = serializer.data
# return Response(data)
