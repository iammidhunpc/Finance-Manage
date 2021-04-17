import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from payment.models import Invoice
from .serializer import InvoiceSerializer
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

# initialize the APIClient app
client = Client()


class CreateInvoicetest(TestCase):

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user = User.objects.create_superuser('test', 'admintest@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.client.force_login(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.invoicelist_data = {'invoice_id': 'invoice_1', 'client_name': 'test_client',
                                 'client_email': 'test_email@gmail.com', \
                                 'amount': 123, 'project_name': 'project_test'}
        self.response = self.client.post(
            reverse('create'),
            self.invoicelist_data,
            format="json")

    def test_api_can_create_a_invoice(self):
        """Test the api can create an invoice."""
        print(self.response.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_bucketlist(self):
        """Test the api can get a given bucketlist."""
        bucketlist = Invoice.objects.get()
        response = self.client.get(
            reverse('details', kwargs={'invoice_id': bucketlist.invoice_id}),
            format="json", HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucketlist)

    def test_api_can_update_bucketlist(self):
        """Test the api can update a given bucketlist."""
        bucketlist = Invoice.objects.get()
        change_bucketlist = {'project_name': 'Test Project'}
        res = self.client.patch(
            reverse('details', kwargs={'invoice_id': bucketlist.invoice_id}),
            change_bucketlist, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        """Test the api can delete a bucketlist."""
        bucketlist = Invoice.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'invoice_id': bucketlist.invoice_id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
