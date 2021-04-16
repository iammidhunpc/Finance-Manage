from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializer import InvoiceSerializer
from payment.models import Invoice

class InvoiceViewSet(ModelViewSet):
    """list all invoices"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (BasicAuthentication, TokenAuthentication)

class GetUserTokenView(APIView):
    """Returns user token"""

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


class InvoiceCreateView(generics.ListCreateAPIView):
    """This class handles the http POST requests."""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = ( BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save()

class InvoiceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Invoice.objects.all()
    lookup_field = 'invoice_id'
    serializer_class = InvoiceSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = ( BasicAuthentication, TokenAuthentication)