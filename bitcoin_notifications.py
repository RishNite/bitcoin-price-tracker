import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 100
BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
API_KEY = "48b68606-46b0-4edf-85a3-60d8702e4dee"
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{}'

# Headers for API request
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,
}

# Get the current Bitcoin price
def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        bitcoin_data = next((coin for coin in response_json["data"] if coin["symbol"] == "BTC"), None)
        price = float(bitcoin_data["quote"]["USD"]["price"])
        return round(price, 2)  # Round the price to two decimal places (nearest cent)
    else:
        print(f"Error fetching Bitcoin data: {response.status_code}")
        return None

# Post the price to IFTTT
def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event, "hwCZf6ihuIOaaJbP4TGyD957snHzmAv1pf-DBkUitho")
    response = requests.post(ifttt_event_url, json=data)
    print(f"Posted to IFTTT, response: {response.status_code}, Data Sent: {data}")

# Main function to fetch the price and send the notification
def main():
    while True:
        price = get_latest_bitcoin_price()  # Get current Bitcoin price
        if price:
            print(f"Bitcoin price: {price} USD")

            # Send an emergency notification if price is below threshold
            if price < BITCOIN_PRICE_THRESHOLD:
                post_ifttt_webhook('bitcoin_price_emergency', price)

            # Send periodic price updates every 5 minutes
            post_ifttt_webhook('bitcoin_price_update', price)

        # Sleep for 5 minutes before checking the price again
        time.sleep(30 * 60)  # 5 minutes in seconds

# Run the script
if __name__ == '__main__':
    main()
