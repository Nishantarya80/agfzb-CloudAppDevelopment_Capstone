import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    try:
        api_key = None
        if 'api_key' in kwargs:
            params = {
                'text': kwargs['text'],
                'version': '2021-03-25',
                'features': 'sentiment',
                'return_analyzed_text': True
            }
            api_key = kwargs['api_key']
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=params, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            print('get_requestResponse Status Code = ', status_code)
            return None
    except Exception as e:
        print('Error occurred', e)
        return None

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    try:
        headers = {  'Content-Type': 'application/json'}
        response= requests.request("POST", url, headers=headers, data=json_payload)

        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            print('Response Status Code = ', status_code)
            return None
    except Exception as e:
        print('Error occurred', e)
        return None

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers

        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url):
    results=[]
    # call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        reviews = json_result["review"]
        for review in reviews:
            try:
                Sentiment=analyze_review_sentiments(review["review"])
  
            except:
                Sentiment="neutral"
     

            if review["purchase"]==True:
                review_obj = DealerReview(id=review["id"],dealership=review["dealership"],name=review["name"],purchase=review["purchase"],
                review=review["review"],purchase_date=review["purchase_date"],car_make=review["car_make"],car_model=review["car_model"],
                car_year=review["car_year"], sentiment=Sentiment)
            else:
                review_obj = DealerReview(id=review["id"],dealership=review["dealership"],name=review["name"],purchase=review["purchase"],
                review=review["review"],purchase_date=review["review_time"],car_make="NONE",car_model="NONE",
                car_year="NONE", sentiment=Sentiment)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    kwargs = {
        'text': text,
        'api_key': "z43HCKRN1IlZiUWnzyZoo-FNTS3C8OWHCNSnYT7fzhTk"
    }
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/2e32f983-6289-46d9-82b8-608e601d2005"
    result = get_request(url + '/v1/analyze', **kwargs)
    return result['sentiment']['document']['label']

