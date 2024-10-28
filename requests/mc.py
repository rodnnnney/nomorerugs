import requests
from requests.price import get_token_price_in_usdc

def fetch_max_supply(token_mint_address, rpc_url):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenSupply",
        "params": [token_mint_address]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(rpc_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if "result" in data and "value" in data["result"]:
            supply_info = data["result"]["value"]
            max_supply = int(supply_info["amount"]) / (10 ** supply_info["decimals"])
            return max_supply
    except requests.RequestException as e:
        print("Error fetching max supply:", e)
    return None

def calculate_fully_diluted_market_cap(token_mint_address, rpc_url):

    current_price = get_token_price_in_usdc(token_mint_address)
    max_supply = fetch_max_supply(token_mint_address, rpc_url)

    if current_price is not None and max_supply is not None:
        fully_diluted_market_cap = current_price * max_supply
        print(f"Fully Diluted Market Cap: ${fully_diluted_market_cap:,.2f}")
        return fully_diluted_market_cap
    else:
        print("Could not calculate fully diluted market cap.")
        return None


