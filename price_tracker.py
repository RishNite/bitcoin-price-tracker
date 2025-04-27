import requests

# 🔹 Replace with your actual API key
API_KEY = "YOUR_COINMARKETCAP_API_KEY_HERE"

# 🔹 API URL for latest cryptocurrency listings
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# 🔹 Headers to include your API key
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,  # Use API_KEY variable
}

try:
    # 🔹 Make the API request
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()  # Raises an error for bad responses (400, 401, 403, 500, etc.)

    # 🔹 Convert response to JSON
    response_json = response.json()

    # 🔹 Print response type (should be a dictionary)
    print(type(response_json))

    # 🔹 Extract Bitcoin data
    if "data" in response_json:
        bitcoin_data = next((coin for coin in response_json["data"] if coin["symbol"] == "BTC"), None)
        print(bitcoin_data)
    else:
        print("Error fetching Bitcoin data:", response_json)

except requests.exceptions.RequestException as e:
    print("API Request Error:", e)
