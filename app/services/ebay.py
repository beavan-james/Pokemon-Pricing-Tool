#FetchSoldListingsService.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

EBAY_APP_ID = os.getenv("EBAY_APP_ID")

# Search ebay for sold listings of a given card name. Get metadata including sold price and dates.


def fetch_sold_listings(card_name, limit=25):
    url = "https://svcs.ebay.com/services/search/FindingService/v1"
    headers = {"X-EBAY-SOA-OPERATION-NAME": "findCompletedItems"}
    params = {
        "OPERATION-NAME": "findCompletedItems",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "keywords": card_name,
        "itemFilter(0).name": "SoldItemsOnly",
        "itemFilter(0).value": "true",
        "paginationInput.entriesPerPage": "50"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    soldlistings = []
    
    # Parse eBay Finding API JSON response
    try:
        # Navigate: findCompletedItemsResponse -> searchResult -> item
        search_result = data.get('findCompletedItemsResponse', [{}])[0].get('searchResult', [{}])[0]
        items = search_result.get('item', [])
        for item in items:
            if len(soldlistings) >= limit:
                break
            # Extract price: sellingStatus -> currentPrice -> __value__
            price_str = item.get('sellingStatus', [{}])[0].get('currentPrice', [{}])[0].get('__value__')
            if price_str:
                soldlistings.append(float(price_str))
    except (IndexError, ValueError, KeyError):
        pass # Return empty list if parsing fails
        
    return soldlistings

# pip install fastapi uvicorn requests
# cd /Users/nativeongfuel/PokemonCompCalculator/
# uvicorn app.main:app --reload
# Testing: curl "http://127.0.0.1:8000/PricingService?card_name=Charizard&limit=10"