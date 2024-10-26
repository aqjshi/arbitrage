import requests
import json
# FreeCryptoAPI base URL (from the documentation)
url = "https://api.freecryptoapi.com/v1/getCryptoList"  # Endpoint to get the list of supported cryptocurrencies

# Extract the API key from 'api.txt'
api_key = ""
with open("api.txt", "r") as file:
    api_key = file.read().strip()

# Set up the headers with the correct Bearer token authentication format
headers = {
    "Authorization": f"Bearer {api_key}"  # Use Bearer token as per the documentation
}

# Send a GET request to retrieve cryptocurrency data
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parse the JSON response data
    data = response.json()
    
        # Check if 'symbols' exists and has at least one coin
    if "symbols" in data and len(data["symbols"]) > 0:
        # Pretty-print the structure of the first coin in the list
        first_coin = data["symbols"][0]
        print(json.dumps(first_coin, indent=4))
    else:
        print("No coins available in the 'symbols' list.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")