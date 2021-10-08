import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth



# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            # Basic authentication GET
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            print(params)
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
    

# Create a get_dealers_from_cf method to get dealers from cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    #Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        #Get the row list in JSON as dealers
        dealers = json_result["entry"]
        #For each dealer object
        for dealer_doc in dealers:
            #Get its content in `doc` object
            #Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

#get_dealers_by_state  is same as above are function can understand if value is pass with parameter or not

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    #Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        #Get the row list in JSON as dealers
        dealers = json_result["review"]
        #For each dealer object
        for dealer_doc in dealers:
            #Get its content in `doc` object
            #Create a DealerReview object with values in `doc` object
            dealer_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                   review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                                   car_model=dealer_doc["car_model"],
                                   car_year=dealer_doc["car_year"], id=dealer_doc["id"],sentiment=analyze_review_sentiments(dealer_doc["review"]))
            results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
#def analyze_review_sentiments(text):

def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/2e32f983-6289-46d9-82b8-608e601d2005"
    api_key = "tal8ORrsyHjcTie0tt4ooFqeMpEEYDVEGthnJr7w3YK3"
    response = get_request(url, text=text, api_key=api_key, version='2020-08-01', features='sentiment', return_analyzed_text=True)
    print(response)
    return response



# Create a `post_request` to make HTTP POST requests


