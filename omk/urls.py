from django.urls import path
from .views import HomeView, OrderCreateView, OrderSuccessView, CheckVoucherView

app_name = 'omk'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('order/', OrderCreateView.as_view(), name='order_create'),
    path('order/success/', OrderSuccessView.as_view(), name='order_success'),
    path('check-voucher/', CheckVoucherView.as_view(), name='check_voucher'),
]