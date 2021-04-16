from rest_framework import serializers
from payment.models import Invoice
import uuid
from django.utils.text import slugify


# Creating short link for payment
class InvoiceSerializer(serializers.ModelSerializer):
    closed = serializers.BooleanField(required=False),
    short_link = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Invoice
        fields = ['invoice_id', 'client_name', 'client_email', 'project_name', 'amount', 'closed', 'short_link', 'slug']
        read_only_fields = ('slug',)

    def create(self, validated_data):
        invoice = Invoice(**validated_data)
        slug = slugify(uuid.uuid4())
        invoice.slug = slug
        invoice.save()
        return invoice
