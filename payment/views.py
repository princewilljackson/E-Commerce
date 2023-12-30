from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages

from orders.models import Order
from . models import Payment

def payment_process(request: HttpRequest) -> HttpResponse:
    '''
    Process the payment using paystack
    '''
    # Get the order id from the session
    order_id = request.session.get('order_id', None)
    # Get the order object from the database
    order = get_object_or_404(Order, id=order_id)
    # Get the total cost of the order
    total_cost = order.get_total_cost()
    # Create a new payment object
    payment = Payment()
    # Set the amount of the payment to the total cost of the order
    payment.amount = total_cost
    # Set the email of the payment to the email of the order
    payment.email = order.email
    # Save the payment object to the database
    payment.save()
    # Set the template name for the payment page
    template_name = 'payment/paystack.html'
    # Create a context dictionary for the payment page
    context = {'order':order, 'total_cost': total_cost, 'PAYSTACK_PUBLIC_KEY':settings.PAYSTACK_PUBLIC_KEY}
    # Return the payment page with the context dictionary
    return render(request, template_name, context)

def payment_verify(request: HttpRequest, ref:str) -> HttpResponse:
    '''
    Verify the payment using the reference number.
    '''
    payment = get_object_or_404(Payment, ref=ref)
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verified')
    messages.error(request, 'Verification Failed')
    return redirect('payment:payment_completed')

def payment_completed(request):
    return render(request, 'payment/completed.html')