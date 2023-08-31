import requests
import time
# Replace with your actual Alpha Vantage API key
API_KEY = "JAQLFFUN5NGN9TD5"
while True:
    try:
        # Construct the API request URL
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=JAQLFFUN5NGN9TD5"

        # Fetch data from the API
        response = requests.get(url)
        data_dict = response.json()['Realtime Currency Exchange Rate']
        print("Exchange Rate: {:.4f}".format(float(data_dict["5. Exchange Rate"])))
        print("*" * 100)
        time.sleep(60)

    except Exception as e:
        print("An error occurred:", e)
        time.sleep(10)
