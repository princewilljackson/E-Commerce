from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import CartAddProductForm

# Create your views here.
def product_list(request, category_slug=None):
    '''
    Product list page
    :param request:
    :param category_slug:
    :return:
    '''
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    template_name = "shop/products/product_list.html"
    context = { "category": category, "categories": categories, "products": products}
    return render(request, template_name, context)

def product_detail(request, id, slug):
    '''
    Product detail page
    :param request:
    :param id:
    :param slug:
    :return:
    '''
    # Get the product object or return a 404 error if it doesn't exist
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    # Set the template name to the product_detail.html template
    template_name = "shop/products/product_detail.html"
    # Create a context dictionary with the product object
    context = { "product": product, "cart_product_form": cart_product_form}
    # Return the rendered template with the context dictionary
    return render(request, template_name, context)  