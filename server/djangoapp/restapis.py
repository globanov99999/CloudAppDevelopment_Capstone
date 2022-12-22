import json

import requests
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

from .models import CarDealer, DealerReview

NLU_URL = 'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/' \
          'instances/04f4f47e-aa82-48d9-90d7-7a99a8cdfd92'




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
    # print(f'With text {text} ')
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
    json_result = get_request(url + '?state=' + str(state_id))
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
                                      purchase=review.get('purchase'), purchase_date=review.get('purchase_date'),
                                      car_make=review.get('car_make'), car_model=review.get('car_model'),
                                      car_year=review.get('car_year'), sentiment=None,
                                      review_id=review.get('id'), name=review.get('name', 'Anonimous'),
                                      review=review['review'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    print(len(results))
    return results


def post_request(url, payload, **kwargs):
    print(f'POST to url={url} payload={payload} kwargs={kwargs}')
    # noinspection PyBroadException
    try:
        response = requests.post(url=url,
                                 json=payload,
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
    authenticator = IAMAuthenticator('K_JdVSTv13Mp0V9N2BznuTkOHByA2sQ4fcPfHQzBVGj1')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(NLU_URL)

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            keywords=KeywordsOptions(emotion=True, sentiment=True)
        )).get_result()
    res = ','.join(r['sentiment']['label'] for r in response.get('keywords', []))
    print(res)
    return res
