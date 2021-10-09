from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
import requests
import os
from io import BytesIO

from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
import tempfile
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from core.models import Payment
from .models import *
from .forms import *
from .filters import *
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account was created for ' + username)

            return redirect('signin')

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')


        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/signIn.html', context)


def logoutUser(request):
    logout(request)
    return redirect('signin')



def gallery(request):
    return render(request, 'gallery/gallery.html')


def handler404(request, exception, template_name="error/404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    return render(request, 'error/500.html', status=500)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['customer'])
def home(request):
    orders = request.user.customer.payment_set.all()
    from django.db.models import Sum
    total_amount= orders.annotate(total=Sum("amount"))

    total_count = orders.count()
    #pending = orders.filter(status='Pending').count()
   
    print('orders:', orders)
   
    print(total_count)
    print('total_amount:' ,total_amount)

    context = {'orders': orders,'total_count': total_count}
    return render(request, 'trisolace/welcome.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':

        form = CustomerForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='signin')
@admin_only
def dashboard(request):
    orders = Payment.objects.all()
    customers = Customer.objects.all()
    
    total_customers = customers.count()

    total_orders = orders.count()
    
    print(orders)
    print(total_orders)
    

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders}

    return render(request, 'trisolace/dashboard.html', context)


def products(request):
    # form = OrderForm(initial={'customer':customer})

    # print('Printing POST:', request.POST)
    form = OrderForm()

    context = {'form': form}
    return render(request, 'trisolace/products.html', context)


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.payment_set.all()
    order_count = orders.count()
    get_user = request.user
    email= get_user.email
    phone= Customer.objects.all().filter(phone='phone')
    print(phone)
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter, 'email': email}
    return render(request, 'trisolace/customer.html', context)


def faq(request):
    return render(request, 'faq/index.html')


def news(request):
    return render(request, "news/index.html")


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF
class ViewPDF(View):

    def get(self, request, *args, **kwargs):
        # data = {"Name": name, "lastName": lastName, "Email": email, "Company": company, "Country": country, "Address": Address, "Visit date": visit, "Visit type":visittype, "Investment Amount": amount, "Investment Period": investframe}
        pdf = render_to_pdf('pdf-output.html', {'context': context})
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('pdf-output.html', {'context': context})

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'trisolace/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    print('ORDER:', order)
    if request.method == 'POST':

        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'trisolace/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'trisolace/delete.html', context)
