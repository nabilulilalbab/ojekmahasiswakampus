from django.urls import path
from .views import HomeView, OrderCreateView, OrderSuccessView, CheckVoucherView, KalkulatorView, CalculateCostAPI,FeedbackView,FeedbackThanksView

app_name = 'omk'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('order/', OrderCreateView.as_view(), name='order_create'),
    path('order/success/', OrderSuccessView.as_view(), name='order_success'),
    path('check-voucher/', CheckVoucherView.as_view(), name='check_voucher'),
    path('kalkulator/', KalkulatorView.as_view(), name='kalkulator'),
    path('api/calculate-cost/', CalculateCostAPI.as_view(), name='calculate_cost_api'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('feedback/terimakasih/', FeedbackThanksView.as_view(), name='feedback_thanks'),
    ]
