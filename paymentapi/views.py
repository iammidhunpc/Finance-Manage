from django.shortcuts import render
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from payment.models import Invoice
from .serializer import InvoiceSerializer
from django.http import JsonResponse
import stripe
import requests
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
import uuid
from django.utils.text import slugify

stripe.api_key = settings.STRIPE_SECRET_KEY

# Invoice creation view with payment link
class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = ( BasicAuthentication, TokenAuthentication)

    def create(self, request, *args, **kwargs):
        context ={
            'request': request
        }
        serializer = self.get_serializer(data=request.data,context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            'code': 200,
            'status': "Invoice Created Successfully",
        }
        data['response'] = serializer.data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class UserDetailView(APIView):
    def get(self, request,*args,**kwargs):
        username =   request.GET.get('username')
        password =  request.GET.get('password')
        if not username:
            return Response({'message': 'Username should not be blank','success':False},status=HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'message': 'Password should not be blank','success':False},status=HTTP_400_BAD_REQUEST)
        if username and password:

            user = authenticate(username=username, password=password)
            try:
                token, created = Token.objects.get_or_create(user=user)
                if user:
                    if user.is_superuser==True:
                        data = {
                                'username': user.username,
                                'token': token.key,
                                'user_type': "SUPERUSER"
                                }
                        return Response({'success': True,'user-details':data}, status=HTTP_200_OK)
            except:
                return Response({'message': 'Invalid credentials','success':False},status=HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)