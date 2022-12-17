import json
import requests
from .models import CarDealer, DealerReview



def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url} ")
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs, timeout=60)
    except Exception: # pylint: disable=broad-except
        print("Network exception occurred")
        return {}
    status_code = response.status_code
    text = response.text
    print(f"With status {status_code} ")
    print(f"With text {text} ")
    if not text:
        text={}
    json_data = json.loads(text)
    return json_data

def get_dealers_from_cf(url):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["result"]
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    print(len(results))
    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url+'?id='+str(dealer_id))
    if json_result:
        reviews = json_result["result"]
        for review in reviews:
            print(review)
            review_obj = DealerReview(dealership=review['dealership'],
            purchase=review['purchase'],purchase_date=review['purchase_date'],
            car_make=review['car_make'], car_model=review['car_model'],
            car_year=review['car_year'], sentiment=None,
            id=review['id'], name=review['name'], review=review['review'])
            results.append(review_obj)
    print(len(results))
    return results


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)





# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



