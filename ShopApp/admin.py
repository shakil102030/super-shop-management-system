from django.contrib import admin
from .models import Category, Product, Order
from django.utils.safestring import mark_safe
from django.urls import reverse

def customer_name(obj):
    return '%s' % (obj.customer_name)
customer_name.short_description = 'Name'

def pdfFile(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('OrderPdfView', args=[obj.id])))
pdfFile.short_description = 'PDF'

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'current_stock']
    search_fields = ['product_name', 'current_stock']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', customer_name, pdfFile]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

