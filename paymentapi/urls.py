from django.urls import include, path
from django.conf.urls import url
from .views import GetUserTokenView,InvoiceViewSet, InvoiceCreateView, InvoiceDetailsView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoices')

urlpatterns = [
    url(r'^', include(router.urls)),
    path('get-user-token/', GetUserTokenView.as_view(),name='get-user-token'),
    path('invoice-create/', InvoiceCreateView.as_view(), name="create"),
    path('invoicelists/<str:invoice_id>/', InvoiceDetailsView.as_view(), name='details')
]


