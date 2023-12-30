from django.contrib import admin
from . models import Payment


class PaymentAdmin(admin.ModelAdmin):

    list_display = ('email', 'amount',  'verified', 'date_created')
    list_display_links = ('email',)
    search_fields = ('email',)
    list_per_page = 25

admin.site.register(Payment, PaymentAdmin)
