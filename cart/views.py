from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product

from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    # Get the cart from the request
    cart = Cart(request)
    # Get the product object from the product_id
    product = get_object_or_404(Product, id=product_id)
    # Create a form to add the product to the cart
    form = CartAddProductForm(request.POST)
    # Check if the form is valid
    if form.is_valid():
        # Get the cleaned data from the form
        cd = form.cleaned_data
        # Add the product to the cart
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        # Redirect to the cart detail page
        return redirect('cart:cart_detail')
    
@require_POST
def cart_remove(request, product_id):
    # Get the cart from the request
    cart = Cart(request)
    # Get the product object from the product_id
    product = get_object_or_404(Product, id=product_id)
    # Remove the product from the cart
    cart.remove(product)
    # Redirect to the cart detail page
    return redirect('cart:cart_detail')

def cart_detail(request):
    # Get the cart from the request
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    # Set the template name
    template_name = 'cart/detail.html'
    # Render the template with the cart as a context variable
    return render(request, template_name, {'cart': cart})