from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Contact
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserForm
from django.contrib.auth import login, logout, authenticate
import csv, io
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.

def home(request):
    data = {'contacts': Contact.objects.order_by('name')}
    return render(request=request, template_name='myapp/dash.html', context=data)

def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as: {username}")
            return redirect('/')

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg} : {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "myapp/register.html",
                          context={"form":form})

    form = CustomUserForm
    return render(request = request,
                  template_name = "myapp/register.html",
                  context={"form":form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as {username}')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
            
    form = AuthenticationForm()
    return render(request=request, template_name='myapp/login.html', context={'form':form})

def logout_request(request):
    logout(request)
    messages.info(request, f'Logged out successfully!')
    return redirect('/')

def add_csv(request):
    csv_file = request.FILES['csv_file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Please upload CSV file only')
        return redirect('/')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    ccount = 0
    ucount = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        updated, created = Contact.objects.update_or_create(
            name=column[1],
            number=column[2],
        )
        if created:
            ccount += 1
        if updated:
            ucount += 1
    messages.success(request, f'{ccount} contacts added, {ucount-ccount} contacts updated')
    return redirect('/')

def add_contact(request):    
    name = request.POST['name']
    number = request.POST['number']
    if name and number:
        new = Contact.objects.update_or_create(name=name, number=number)
    if new:
        messages.success(request, 'Added new contact')
        return redirect('/')

def search_results(request):
    if request.method == 'POST':
        key = request.POST.get('query')
        results = {'contacts': Contact.objects.filter(name__icontains=key).order_by('name')}
        return render(request=request, template_name='myapp/results.html', context=results)
    
def delete(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')

        con = get_object_or_404(Contact, name=name, number=number)
        succ = con.delete()
        return HttpResponse(succ)