from django.contrib import admin
from django.urls import path, include
from payment.views import (
    CreateCheckoutSessionView,
    SuccessView,
    CancelView,
    stripe_webhook,
    StripeIntentView,
    ProceedToPayView
)
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-payment-intent/<uidb64>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<uidb64>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('proceed-to-pay/<uidb64>/', ProceedToPayView.as_view(), name='proceed-to-pay'),
    path('', include('paymentapi.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('docs', schema_view)


]