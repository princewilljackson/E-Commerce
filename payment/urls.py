from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('verify-payment/<slug:ref>/', views.payment_verify, name='verify-payment'),
    path('completed/', views.payment_completed, name='payment-completed'),
    ]