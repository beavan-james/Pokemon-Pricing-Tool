#Pricing Service
#Fee is a multiplier for how much the user wants to pay based on the comp e.g. 70% of avg comps
def calculate_market_price(soldlistings, fee = 1):
   if not soldlistings:
         return 0.0
   prices = [item["price"] for item in soldlistings]
   prices.sort()
   min = prices[0]
   max = prices[-1]
   avg = sum(prices) / len(prices)
   median = prices[len(prices)//2]
   price=0
   trend = "Stable" # Default value
   if median > avg:
         trend = "Stable"
   elif median < avg:
         trend = "Falling"
   price = pricecalc(avg, trend, fee)
   return price

def pricecalc(avg, trend, fee):
   if trend == "Stable":
        pass
   elif trend == "Falling":
        avg = avg * 0.95
   price = avg * fee
   return price