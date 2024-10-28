import requests

def get_token_price_in_usdc(token_mint):
    url = f"https://price.jup.ag/v6/price?ids={token_mint}"
    response = requests.get(url)
    data = response.json()
    if "data" in data and token_mint in data["data"]:
        price = round(data["data"][token_mint]["price"], 10)  # Round to 10 decimal places
        print(type(price))
        return price
    else:
        print("Token not supported or price not available.")
        return None

# token_mint = "62GzFSrcha2QupnSM7BiEwPz4VM1fEFki2Ah7k6bpump"  
# price = get_token_price_in_usdc(token_mint)
# if price is not None:
#     # Format with 10 decimal places, forcing a non-scientific display
#     print(f"1 unit of token {token_mint} is worth {price:.10f} USDC")
