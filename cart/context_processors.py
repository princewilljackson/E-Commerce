from .cart import Cart

#@cache_page((60 * 15))
def cart(request):
    '''
    View function for the cart page, which returns the cart object
    '''
    return {'cart': Cart(request)}