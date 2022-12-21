import json

import requests
from requests.auth import HTTPBasicAuth

from .models import CarDealer, DealerReview


def get_request(url, auth=None, **kwargs):
    print(kwargs)
    print(f'GET from url={url} auth={auth} kwargs={kwargs}')
    # noinspection PyBroadException
    try:
        response = requests.get(url=url,
                                auth=auth,
                                params=kwargs,
                                headers={'Content-Type': 'application/json'},
                                timeout=60)
    except Exception:  # pylint: disable=broad-except
        print('Network exception occurred')
        return {}
    status_code = response.status_code
    text = response.text
    print(f'With status {status_code} ')
    print(f'With text {text} ')
    if not text:
        text = {}
    json_data = json.loads(text)
    return json_data


def create_dealers(json_result):
    results = []
    dealers = json_result['result']
    for dealer in dealers:
        dealer_doc = dealer
        dealer_obj = CarDealer(address=dealer_doc['address'], city=dealer_doc['city'],
                               full_name=dealer_doc['full_name'],
                               dealer_id=dealer_doc['id'], lat=dealer_doc['lat'], long=dealer_doc['long'],
                               short_name=dealer_doc['short_name'],
                               st=dealer_doc['st'], dealer_zip=dealer_doc['zip'])
        results.append(dealer_obj)
    print(len(results))
    return results


def get_dealers_from_cf(url):
    json_result = get_request(url)
    if not json_result:
        return []
    return create_dealers(json_result)


def get_dealers_by_state_from_cf(url, state_id):
    json_result = get_request(url + '?state' + str(state_id))
    if not json_result:
        return []
    return create_dealers(json_result)


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url + '?id=' + str(dealer_id))
    if json_result:
        reviews = json_result['result']
        for review in reviews:
            print(review)
            review_obj = DealerReview(dealership=review['dealership'],
                                      purchase=review['purchase'], purchase_date=review['purchase_date'],
                                      car_make=review['car_make'], car_model=review['car_model'],
                                      car_year=review['car_year'], sentiment=None,
                                      review_id=review['id'], name=review['name'], review=review['review'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    print(len(results))
    return results


def post_request(url, payload, **kwargs):
    print(kwargs)
    print(f'POST to url={url} payload={payload} kwargs={kwargs}')
    # noinspection PyBroadException
    try:
        response = requests.post(url=url,
                                 params=kwargs,
                                 headers={'Content-Type': 'application/json'},
                                 timeout=60)
    except Exception:  # pylint: disable=broad-except
        print('Network exception occurred')
        return {}
    status_code = response.status_code
    text = response.text
    print(f'With status {status_code} ')
    print(f'With text {text} ')
    if not text:
        text = {}
    json_data = json.loads(text)
    return json_data


def analyze_review_sentiments(text):
    kwargs = {'text': text,
              'version': '2019-07-12',
              'features': {'sentiment': {}, 'categories': {}, 'concepts': {}, 'entities': {}, 'keywords': {}},
              'return_analyzed_text': 'True'}
    return kwargs
