from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # List the fields to be displayed in the admin page
    list_display = ['id', 'first_name', 'last_name', 'email',
    # List the fields to be filtered in the admin page
    'address', 'postal_code', 'city', 'paid',
    # List the fields to be included in the admin page
    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    # Include the OrderItemInline in the admin page
    inlines = [OrderItemInline]