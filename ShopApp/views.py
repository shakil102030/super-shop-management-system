from django.shortcuts import render,get_object_or_404
from .models import Order
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Order, OrderForm, Product, SearchForm
from django.contrib import messages
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q

#customer info form
def Home(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            dat = Order()
            dat.customer_name = merchant_nm = form.cleaned_data['customer_name']
            dat.email = form.cleaned_data['email']
            dat.phone = form.cleaned_data['phone']
            dat.save()
            messages.warning(request, "Successfully created")
            return redirect('Home')
    form = OrderForm()

    context = {
        'form': form,
    }
    return render(request, "base.html", context)

#product search
def Search(request): 
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['q']
            if query == None or query == '':
                object_list = Product.objects.filter(status="True").order_by('-created_at')
                
            else:
                print('query = ', query)  
                object_list = []
                for que in query.split():

                    pos_list = Product.objects.filter(
                        Q(product_name__icontains=que) | Q(current_stock__icontains=que)
                        ).order_by('-created_at')
                    object_list.extend(pos_list)
                    print(object_list)
            object_list = list(set(object_list))
            global val
            def val():
                return object_list

            order_obj = Order.objects.get(id=2)
            total=0
            for p in object_list:
                total += p.unit_price * p.current_stock
            context = {
                'order_obj': order_obj,
                'object_list': object_list, 
                'total': total,
            }
            return render(request, 'order_table.html', context)   
            
    return HttpResponseRedirect('/')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return result.getvalue()
    
    return None
#PDF invoice
def OrderPdfView(request, pk):
    object_list = val()
    order_obj = get_object_or_404(Order, pk=pk)
    total=0
    for p in object_list:
        total += p.unit_price * p.current_stock
    context = {
        'order_obj': order_obj,
        'object_list': object_list,
        'total': total,
    }
    pdf = render_to_pdf('order_table.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=%s.pdf" % pk 
        response['Content-Disposition'] = content

        return response
       









    


    
