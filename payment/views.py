import json
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Invoice
import requests

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        invoice = Invoice.objects.all()

        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "invoice": invoice,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class GenerateUrlView(TemplateView):
    template_name = "generateurl.html"

    def get_context_data(self, **kwargs):
        invoice_id = self.kwargs["pk"]
        invoice = Invoice.objects.get(invoice_id=invoice_id)
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

        context = super(GenerateUrlView, self).get_context_data(**kwargs)
        context.update({
            "invoice": invoice,
            "short_link": short_link
        })
        return context


class ProceedToPayView(TemplateView):
    template_name = "proceedtopay.html"

    def get_context_data(self, **kwargs):
        invoice_id = self.kwargs["pk"]
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        context = super(ProceedToPayView, self).get_context_data(**kwargs)
        context.update({
            "invoice": invoice,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        invoice_id = self.kwargs["pk"]
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        YOUR_DOMAIN = self.request.scheme + "://" + self.request.META['HTTP_HOST']
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': invoice.amount,
                        'product_data': {
                            'name': invoice.invoice_id,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "invoice_id": invoice.invoice_id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        invoice_id = session["metadata"]["invoice_id"]
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        # setting invoice as closed
        invoice.closed = True
        invoice.save()
        send_mail(
            subject="Invoice Paid",
            message=f"Thanks for the payment for invoice {invoice.invoice_id}",
            recipient_list=[invoice.client_email],
            from_email="matt@test.com"
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        invoice_id = intent["metadata"]["invoice_id"]
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        # setting invoice as closed
        invoice.closed = True
        invoice.save()
        send_mail(
            subject="Invoice Paid",
            message=f"Thanks for the payment for invoice {invoice.invoice_id}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )
    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            invoice_id = self.kwargs["pk"]
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            intent = stripe.PaymentIntent.create(
                amount=invoice.amount,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "invoice_id": invoice.invoice_id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
