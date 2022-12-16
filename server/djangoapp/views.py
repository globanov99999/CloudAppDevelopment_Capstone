from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
class BasePageView(TemplateView):
    template_name = "djangoapp/base.html"

class IndexPageView(TemplateView):
    template_name = "djangoapp/index.html"   

class AboutPageView(TemplateView):
    template_name = "djangoapp/about.html"

class ContactPageView(TemplateView):
    template_name = "djangoapp/contact.html"

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    print("Log out the user `%s`", request.user.username)
    logout(request)
    return redirect('djangoapp:index')

def signup_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except Exception: # pylint: disable=broad-except
            logger.debug("%s is new user", username)
        if not user_exist:
            user = User.objects.create_user(username=username, 
                                            first_name=first_name, 
                                            last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/7d385671-e1f0-4106-b25f-758f2c26052d/dealership-package/get-dealership.json"
        dealerships = get_dealers_from_cf(url)
        dealer_names = [dealer.short_name for dealer in dealerships]
        return render(request, 'djangoapp/index.html', {'dealer_names':dealer_names})


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/7d385671-e1f0-4106-b25f-758f2c26052d/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        return render(request, 'djangoapp/dealer_details.html', {'reviews':reviews})


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

