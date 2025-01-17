from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from dateutil.parser import parse
from django.urls import reverse
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/aboutus.html', context)
# ...

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contactus.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('psw')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context ={}
    if request.method == "GET":
        url = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/7eed226c81af75dae086a851aa8986b232fbb65a5f0a0483731fc5046f29267e/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context["dealership_list"]=dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    if request.method == "GET":
            # LOCAL url = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/7eed226c81af75dae086a851aa8986b232fbb65a5f0a0483731fc5046f29267e/api/review"
            # LOCAL url_dealer = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/7eed226c81af75dae086a851aa8986b232fbb65a5f0a0483731fc5046f29267e/api/dealership"
            url = "https://1da01ea5.eu-gb.apigw.appdomain.cloud/api/review"
            url_dealer = "https://1da01ea5.eu-gb.apigw.appdomain.cloud/api/dealership"

            # Get dealers from the URL
            dealerships = get_dealer_reviews_from_cf(str(url)+'?dealerId='+str(dealer_id))
            dealer_name = get_dealers_from_cf(url_dealer)
            # Concat all dealer's short name
            context['review_list']=dealerships
            context['dealer_id']=dealer_id
            context['dealer']=dealer_name[dealer_id-1]

            #review = ' '.join([dealer.review for dealer in dealerships])
            # Return a list of dealer short name
            return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review

def add_review(request, dealer_id):
    context = {}
    print("thanks"+str(dealer_id))
    if request.method == 'GET':
        # LOCAL url = 'https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/7eed226c81af75dae086a851aa8986b232fbb65a5f0a0483731fc5046f29267e/api/dealership'
        url = "https://1da01ea5.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url, **({'id':dealer_id}))
        context['dealer'] = dealerships[dealer_id-1]
        context['cars'] = CarModel.objects.filter(dealerid=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        # LOCAL url = 'https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/7eed226c81af75dae086a851aa8986b232fbb65a5f0a0483731fc5046f29267e/api/review'
        url = "https://1da01ea5.eu-gb.apigw.appdomain.cloud/api/review"
        dealer_reviews = get_dealer_reviews_from_cf(url)
        max_id = max([review.id for review in dealer_reviews], default=100)
        new_id = max_id + 1 if max_id >= 100 else max_id + 100
        date = datetime.now()
        date = date.strftime('%Y-%m-%d')
        print(request.POST)
        if 'purchasecheck' in request.POST:
            car=request.POST['car_details']
            car = car.split("-")
            car_make = car[0]
            car_model = car[1]
            car_year = parse(car[2])
            car_year=car_year.year
            print("purchase_date")
            print(request.POST.get('purchase_date'))

            json_payload = {
                'doc': {
                    'id': new_id,
                    'name': request.user.first_name+" "+request.user.last_name,
                    'review': request.POST['review_content'],
                    'purchase': True,
                    'purchase_date': request.POST.get('purchase_date'),
                    'dealership': dealer_id,
                    'car_make': car_make,
                    'car_model': car_model,
                    'car_year': car_year,
                    'review_time': date
                }
            }
        else:
            json_payload = {
                'doc': {
                    'id': new_id,
                    'name': request.user.get_full_name(),
                    'review': request.POST['review_content'],
                    'purchase': False,
                    'dealership': dealer_id,
                    'review_time': date
                   }
            }
        
        json_payload=json.dumps(json_payload)
        print("sending")
        print(json_payload)
        post_request(url, json_payload)
        
        return HttpResponseRedirect(reverse(viewname='djangoapp:dealer_details', args=(str(dealer_id),)))