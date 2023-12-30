from django.shortcuts import render, redirect
from django.urls import reverse

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    # create a cart object to store the items in the user's session
    cart = Cart(request)
    
    # if the request method is POST, the form has been submitted
    if request.method == 'POST':
        # create a form object from the submitted data
        form = OrderCreateForm(request.POST)

        # if the form is valid
        if form.is_valid():
            # save the order object
            order = form.save()
            # loop through the items in the cart
            for item in cart:
                # create an OrderItem object for each item in the cart
                OrderItem.objects.create(order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
        # render the created.html template, passing in the order object
        # return render(request,
        #             'orders/created.html',
        #             {'order': order})
    else:
        # create an empty form object
        form = OrderCreateForm()
    # render the create.html template, passing in the cart object and the form object
    return render(request,
                    'orders/create.html',
                    {'cart': cart, 'form': form})