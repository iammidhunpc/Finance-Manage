from django.urls import include, path
from django.conf.urls import url

from .views import InvoiceViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoices')
# router.register(r'create-checkout-session', CheckoutViewSet, basename='create-checkout-session')

urlpatterns = [
    url(r'^', include(router.urls)),

]