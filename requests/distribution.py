import requests

def get_token_supply(url, token_mint_address):
    """Fetches the total supply of a specific token."""
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getTokenSupply",
        "params": [token_mint_address]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data and "result" in data:
            supply_info = data["result"]["value"]
            total_supply = int(supply_info["amount"]) / (10 ** supply_info["decimals"])
            return total_supply
        else:
            print("No supply data found for this token address.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_largest_token_accounts(url, token_mint_address, total_supply):
    """Fetches the largest token accounts and calculates their holding percentage relative to the total supply."""
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getTokenLargestAccounts",
        "params": [token_mint_address]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data and "result" in data:
            accounts_info = []
            accounts = data["result"]["value"]
            for i, account in enumerate(accounts[:10], start=1):  
                balance = float(account["uiAmount"])
                percentage = (balance / total_supply) * 100
                accounts_info.append({
                    "account_index": i,
                    "address": account["address"],
                    "balance": balance,
                    "percentage_of_supply": round(percentage, 2)
                })
            return accounts_info
        else:
            print("No data found for this token address.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_unique_holders_count(token_mint_address, rpc_url):
    """Fetches the number of unique token holders."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getProgramAccounts",
        "params": [
            "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",  # SPL Token program ID
            {
                "encoding": "jsonParsed",
                "filters": [
                    {"dataSize": 165},  # Standard SPL Token account size
                    {"memcmp": {"offset": 0, "bytes": token_mint_address}}  # Filter by token mint address
                ],
                "commitment": "finalized"  # Ensure data is fully confirmed
            }
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(rpc_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        unique_holders = {account["account"]["data"]["parsed"]["info"]["owner"] for account in data["result"]}
        
        return len(unique_holders)
    except requests.RequestException as e:
        print("Error fetching holder count:", e)
        return None

# Usage example
url = "https://nd-326-444-187.p2pify.com/9de47db917d4f69168e3fed02217d15b/"
token_mint_address = "CCwhWaVwJTqrzFahqwsLr9dNKQS1HyBzVWvh3iKcpump"

# Fetch total supply
total_supply = get_token_supply(url, token_mint_address)
if total_supply:
    # Fetch and display the largest accounts
    largest_accounts = get_largest_token_accounts(url, token_mint_address, total_supply)
    print("Largest Token Accounts:", largest_accounts)

# Fetch unique holder count
holder_count = get_unique_holders_count(token_mint_address, url)
print(f"Number of unique holders: {holder_count}")
