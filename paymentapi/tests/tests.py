from payment.models import Invoice
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class InvoiceTest(APITestCase):
    def test_invoice_creation(self):
    	import pdb;pdb.set_trace()
        """
        Ensure we can create a new invoice object.
        """
        url = reverse('invoices')
        data = {'invoice_id': 'invoice_test_id'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.get().invoice_id, 'Financial Invoice')