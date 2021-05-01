from django.db import models
from django.forms import ModelForm
from django import forms
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

class Category(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    )
    category = models.CharField(max_length=100, blank = True)
    status = models.CharField(max_length=30, choices=status)

    def __str__(self):
        return self.category


class Product(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    unit_price = models.IntegerField()
    current_stock= models.IntegerField(default=1)
    status = models.CharField(max_length=30, choices=status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name.__str__()
    def price(self):
        return (self.unit_price * self.current_stock)
   

    

class Order(models.Model):
    customer_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    #total_price = models.IntegerField(default=1)
    def __str__(self):
        return self.customer_name
    #QR code
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.customer_name)
        canvas = Image.new('RGB', (290, 290), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.customer_name}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'email', 'phone']
class SearchForm(forms.Form):
	q = forms.CharField(max_length = 250)