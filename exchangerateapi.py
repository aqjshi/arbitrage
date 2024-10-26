import requests
import json

# Define the base currency for exchange rates (e.g., "USD" as the base currency here)
currency = "USD"

# Load the API key from 'exchangeapi.txt' - this file should contain the API key as a single line of text
api_key = ""
with open("exchangeapi.txt", "r") as file:
    api_key = file.read().strip()  # Read and remove any extra whitespace characters like newlines

# Define the main API endpoint, inserting the API key and base currency into the URL
# This URL will provide the latest exchange rates relative to the specified base currency
url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"

# Send a GET request to the API endpoint to retrieve the exchange rate data
response = requests.get(url)

# Check if the response from the server is successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response data from the API
    data = response.json()
    
    # Check if "conversion_rates" exists in the response, as this will contain the exchange rates
    if "conversion_rates" in data:
        print("\nExchange Rates:")
        
        # Loop through each currency and its exchange rate in the conversion_rates dictionary
        for currency, rate in data["conversion_rates"].items():
            print(f"1 {data['base_code']} = {rate} {currency}")  # Print the rate for each currency
            
            # Define the URL to fetch each currency as the new base currency
            swap_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"
            
            # Send a request to the API with the swapped base currency
            swap_response = requests.get(swap_url)
            
            # Check if the swap request was successful
            if swap_response.status_code == 200:
                # Parse the JSON data for the new base currency
                swap_data = swap_response.json()
                
                # Save the JSON response to a file named after the currency
                with open(f"forex/{currency}_exchange_rates.json", "w") as file:
                    json.dump(swap_data, file, indent=4)  # Write JSON data to the file with indentation for readability
            else:
                print(f"Failed to fetch data for {currency}. Status code: {swap_response.status_code}")
    else:
        print("No exchange rates available in the response.")  # Handle case if conversion rates are missing
else:
    # Print an error message if the initial request failed
    print(f"Failed to fetch data. Status code: {response.status_code}")
