import logging
from datetime import datetime

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealers_by_state_from_cf, get_dealer_reviews_from_cf, post_request

logger = logging.getLogger(__name__)

DJANGOAPP_INDEX_HTML = 'djangoapp/index.html'
DJANGOAPP__INDEX = 'djangoapp:index'

LOCAL_DEALERS = {}

class BasePageView(TemplateView):
    template_name = 'djangoapp/base.html'


class IndexPageView(TemplateView):
    template_name = DJANGOAPP_INDEX_HTML


class AboutPageView(TemplateView):
    template_name = 'djangoapp/about.html'


class ContactPageView(TemplateView):
    template_name = 'djangoapp/contact.html'


def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(DJANGOAPP__INDEX)
        else:
            return render(request, DJANGOAPP_INDEX_HTML, context)
    else:
        return render(request, DJANGOAPP_INDEX_HTML, context)


def logout_request(request):
    print('Log out the user `%s`', request.user.username)
    logout(request)
    return redirect(DJANGOAPP__INDEX)


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
        # noinspection PyBroadException
        try:
            User.objects.get(username=username)
            user_exist = True
        except Exception:
            logger.debug('%s is new user', username)
        if not user_exist:
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect(DJANGOAPP__INDEX)
        else:
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    if request.method == 'GET':
        url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/' \
              '7d385671-e1f0-4106-b25f-758f2c26052d/dealership-package/get-dealership.json'
        dealerships = get_dealers_from_cf(url)
        for dealer in dealerships:
            LOCAL_DEALERS[dealer.dealer_id]=dealer.full_name
        context = {'dealerships': dealerships}
        return render(request, DJANGOAPP_INDEX_HTML, context)


def get_dealers_by_state(request, state_id):
    if request.method == 'GET':
        url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/' \
              '7d385671-e1f0-4106-b25f-758f2c26052d/dealership-package/get-dealership.json'
        dealerships = get_dealers_by_state_from_cf(url, state_id)
        dealer_names = [str(dealer) for dealer in dealerships]
        return render(request, DJANGOAPP_INDEX_HTML, {'dealer_names': dealer_names})


def get_dealer_details(request, dealer_id):
    if request.method == 'GET':
        url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/' \
              '7d385671-e1f0-4106-b25f-758f2c26052d/dealership-package/get-review.json'
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = {'reviews': reviews,
                   'dealership': LOCAL_DEALERS.get(dealer_id, f'Dealership #{dealer_id}'),
                   'dealer_id': dealer_id}
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        return redirect(DJANGOAPP__INDEX)
    if request.method == 'POST':
        review = {'time': datetime.utcnow().isoformat(),
                  'dealership': dealer_id,
                  'review': 'This is a great car dealer!',
                  'name': 'Driver'}
        json_payload = {'review': review}
        url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/' \
              '7d385671-e1f0-4106-b25f-758f2c26052d/dealership-package/post-review.json'
        result = post_request(url, json_payload)
        print(result)
        return render(request, 'djangoapp/dealer_details.html', {'reviews': result})
    elif request.method == 'GET':
        return render(request, 'djangoapp/add_review.html',
                      {'dealer_id':dealer_id,
                       'dealership': LOCAL_DEALERS.get(dealer_id, f'Dealership #{dealer_id}'),
                       'cars': CarModel.objects.all()})
