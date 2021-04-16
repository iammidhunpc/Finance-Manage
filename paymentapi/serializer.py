import uuid
import requests
from django.utils.text import slugify
from rest_framework import serializers
from payment.models import Invoice

# Creating short link for payment
def create_short_link(self,request, slug):
    try:
        domain = request.scheme + "://" + request.META['HTTP_HOST']
    except:
        domain = 'http://127.0.0.1:8000'
    header = {
        "Authorization": "Bearer fb89bf0ea1bee03de72dad0a93469d1c5622511b",
        "Content-Type": "application/json"
    }
    long_url = domain + "/proceed-to-pay/" + slug + "/"
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


# Creating short link for payment
class InvoiceSerializer(serializers.ModelSerializer):
    closed = serializers.BooleanField(required=False),
    short_link = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Invoice
        fields = ['invoice_id', 'client_name', 'client_email', 'project_name', 'amount', 'closed', 'short_link', 'slug']
        read_only_fields = ('slug',)

    def create(self, validated_data):
        request = self.context['request']
        invoice = Invoice(**validated_data)
        slug = slugify(uuid.uuid4())
        invoice.slug = slug
        short_link = create_short_link(self,request,slug)
        invoice.short_link = short_link
        invoice.save()
        return invoice
