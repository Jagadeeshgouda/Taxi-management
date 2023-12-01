from django.shortcuts import get_object_or_404, render
import calendar
from datetime import datetime
from .models import *
from datetime import datetime


from django.shortcuts import render, redirect
from .models import CarRental, Car

from django.shortcuts import render, redirect
from .models import CarRental, Car, Cities

def home(request):
    if request.method == 'POST':
        car_id = request.POST.get('car')
        car = Car.objects.get(pk=car_id)  # Fetch the Car instance using the selected car ID

        city_id = request.POST.get('to')
        city = Cities.objects.get(pk=city_id)  # Fetch the Cities instance using the selected city ID
        email = request.user.email
        # Assuming you have a form in your HTML that submits data
        car_rental_data = {
            'car': car,
            'pickup_date': request.POST.get('pickup_date'),
            'delivery_date': request.POST.get('delivery_date'),
            'start': request.POST.get('start'),
            'to': city,  # Assign the Cities instance, not the ID
            'distance_traveled': request.POST.get('distance_traveled'),
            'status': request.POST.get('status'),
            
        }

        # Create a CarRental object and save it to the database
        car_rental = CarRental(**car_rental_data)
        car_rental.save()

        # Redirect to the same or another page after successful form submission
        return redirect('home')  # Adjust the URL name according to your project

    # If it's a GET request, retrieve data from the database and render the template
    object_list = CarRental.objects.all()
    another_model = Car.objects.all()
    cities = Cities.objects.all()

    return render(request, 'Home.html', {'object_list': object_list, 'another_model': another_model, 'cities': cities})

def confimation(email):
    send_mail(
    'One Time Password',
    f'Hello This is a Taxi-Management project created by jagadeeshgouda Y R and Your booking is confimed we will each you soon ',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )



def getcars(request):
    object_list=Car.objects.all()
    return render(request,"cars.html",{'object_list':object_list})

def more_details_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    context = {
        'car': car
    }


    return render(request, 'MoreDetails.html', context)


from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required


def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            usern = form.cleaned_data['username']
            userp = form.cleaned_data['password']
            user = authenticate(username= usern, password=userp)

            if user is not None:
                login(request, user)
                return redirect('/home')

    else:
        form = AuthenticationForm()
    context= {'form':form}
    return render(request, 'login.html', context)



#logout
@login_required(login_url='/')
def logout_form(request):
    logout(request)
    #return redirect('/login')
    return render(request, 'logout.html')

@login_required(login_url='login')
def changepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('login')
            else:
                return HttpResponse("password is not matching")
        else:
            form = PasswordChangeForm(user= request.user)
            context = {'form':form}
            return render(request, 'changepassword.html',context)
    else:
        return redirect('/')
    
    
#email authentication

from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . forms import CreateUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import random
from .models import PreRegistration,Car
from .forms import VerifyForm
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def creatingOTP():
    otp = ""
    for i in range(6):
        otp+= f'{random.randint(0,9)}'
    return otp

def sendEmail(email):
    otp = creatingOTP()
    send_mail(
    'One Time Password',
    f'Hello This is a Taxi-Management project created by jagadeeshgouda Y R and Your registration OTP :- {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )
    return otp


def createUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                otp = sendEmail(email)
                dt = PreRegistration(first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],username= form.cleaned_data['username'],email=email,otp=otp,password1 = form.cleaned_data['password1'],password2 = form.cleaned_data['password2'])
                dt.save()
                return HttpResponseRedirect('/verify/')
                
                
        else:
            form = CreateUser()
        return render(request,"newuser.html",{'form':form})
    else:
        return HttpResponseRedirect('/success/')
# def login_function(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             form = LoginForm(request=request,data=request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data['username']
#                 password = form.cleaned_data['password']
#                 usr = authenticate(username=username,password = password)
#                 if usr is not None:
#                     login(request,usr)
#                     return HttpResponseRedirect('/success/')
#         else:
#             form = LoginForm()
#         return render(request,'html/login.html',{'form':form})
#     else:
#         return HttpResponseRedirect('/success/')

def verifyUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = VerifyForm(request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                data = PreRegistration.objects.filter(otp = otp)
                if data:
                    username = ''
                    first_name = ''
                    last_name = ''
                    email = ''
                    password1 = ''
                    for i in data:
                        print(i.username)
                        username = i.username
                        first_name = i.first_name
                        last_name = i.last_name
                        email = i.email
                        password1 = i.password1

                    user = User.objects.create_user(username, email, password1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    data.delete()
                    messages.success(request,'Account is created successfully!')
                    return HttpResponseRedirect('/')   
                else:
                    messages.success(request,'Entered OTP is wrong')
                    return HttpResponseRedirect('/verify/')
        else:            
            form = VerifyForm()
        return render(request,'verify.html',{'form':form})
    else:
        return HttpResponseRedirect('/success/')

def success(request):
    if request.user.is_authenticated:
        return render(request,'success.html')
    else:
        return HttpResponseRedirect('/')

from django.db.models import Q

#invoice generator

# views.py

# from django.shortcuts import render, redirect
# from .models import Cities
# @login_required
# def book_ticket(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('booking_success')
#     else:
#         form = BookingForm()

#     return render(request, 'book_ticket.html', {'form': form})

# def booking_success(request):
#     return render(request, 'booking_success.html')
# @login_required
from django.shortcuts import render
from .models import CarRental, Car


def info(request):
    object_list=CarRental.objects.all()
    another_model=Car.objects.all()
    
    # You can then pass this total_amount to your template or use it as needed
    return render(request,"invoice.html",{'object_list':object_list,'another_model':another_model})
  
# from django.http import HttpResponse
# from django.shortcuts import render
# from .models import History

# @login_required
# def history(request):
#     if request.method == 'POST':
#         try:
#             city = Cities.objects.get('city')
#             pick_date = request.POST.get('pick_date')
#             delivery_date = request.POST.get('delivery_date')
#             km = request.POST.get('distance_traveled')
            

#             # Create a new History instance and save it to the database
#             new_user = History(city=city, pick_date=pick_date, delivery_date=delivery_date, distance_travelled=km)
#             new_user.save()
            
                

#             return HttpResponse('Taxi added successfully')
#         except Exception as e:
#             return HttpResponse(f"An exception occurred: {e}")
#     elif request.method == 'GET':
#         return render(request, 'home.html')
#     else:
#         return HttpResponse("Invalid request method. Employee has not been added.")

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def accountSettings(request):
#     customer = request.user.customer # logged in user
#     form = CustomerForm(instance=customer)

#     if request.method == 'POST':
#         form = CustomerForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             form.save()

#     context = {'form':form}
#     return render(request, 'accounts/account_settings.html', context)
from django.views.generic import ListView
from django.db.models import Q
class SearchResultsView(ListView):
    model=drivers
    template_name="search.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = drivers.objects.filter(Q(gender__icontains = query)) | drivers.objects.filter(Q(car_no__contains = query))
        return object_list
