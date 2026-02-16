import requests


def fetch_fx_data():
    """Fetch FX data from the mock external API."""
    url = "http://127.0.0.1:5001/mock-fx-api"  # Replace with the actual API URL
    try:
        response = requests.get(url)  # Use GET method to call the API
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json()  # Convert the JSON response to a Python dictionary
    except requests.RequestException as e:
        print(f"Error fetching FX data: {e}")
        return None

def convert_to_usd(amount, currency):

    fx_data = fetch_fx_data()
    if not fx_data:
        raise Exception("Failed to fetch FX data")
    if currency == "USD":
        return amount, 1.0

    rates = fx_data["rates"]
    rate_to_eur = rates.get(f"{currency}EUR")
    usd_to_eur = rates["USDEUR"]

    if not rate_to_eur:
        raise ValueError("Unsupported currency")

    # Calculate USD rate via EUR
    exchange_rate = rate_to_eur / usd_to_eur
    usd_amount = amount / exchange_rate

    return round(usd_amount, 2), exchange_rate