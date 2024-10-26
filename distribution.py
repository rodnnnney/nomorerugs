import requests

# Function to get top 10 holders of a token
def get_top_holders(token_address, rpc_url="https://api.mainnet-beta.solana.com", top_n=10):
    headers = {
        "Content-Type": "application/json"
    }

    payload_largest_accounts = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenLargestAccounts",
        "params": [
            token_address
        ]
    }
    response_largest_accounts = requests.post(rpc_url, headers=headers, json=payload_largest_accounts).json()
    
    if "result" not in response_largest_accounts or "value" not in response_largest_accounts["result"]:
        raise Exception("Failed to get largest token accounts.")
    
    largest_accounts = response_largest_accounts["result"]["value"]

    payload_total_supply = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenSupply",
        "params": [
            token_address
        ]
    }
    response_total_supply = requests.post(rpc_url, headers=headers, json=payload_total_supply).json()
    
    if "result" not in response_total_supply or "value" not in response_total_supply["result"]:
        raise Exception("Failed to get token supply.")
    
    total_supply = int(response_total_supply["result"]["value"]["amount"])

    top_holders = []
    for account_info in largest_accounts[:top_n]:
        account_address = account_info["address"]
        balance = int(account_info["amount"])
        percentage = (balance / total_supply) * 100
        top_holders.append({
            "account": account_address,
            "balance": balance,
            "percentage": percentage
        })
    
    return top_holders

token_address = "BQYPkPWpYY36eUgt2fbPNrQnvE7Qa5vd5JPjqYvmpump"
top_holders = get_top_holders(token_address)
for holder in top_holders:
    print(f"Account: {holder['account']}, Balance: {holder['balance']}, Percentage: {holder['percentage']:.2f}%")

# Get total token supply
def get_token_supply(token_address, rpc_url="https://api.mainnet-beta.solana.com"):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenSupply",
        "params": [
            token_address
        ]
    }
    response = requests.post(rpc_url, headers=headers, json=payload).json()
    
    if "result" not in response or "value" not in response["result"]:
        raise Exception("Failed to get token supply.")
    
    supply_info = response["result"]["value"]
    total_supply = int(supply_info["amount"]) / (10 ** supply_info["decimals"])
    
    return total_supply

token_address = "BQYPkPWpYY36eUgt2fbPNrQnvE7Qa5vd5JPjqYvmpump"
total_supply = get_token_supply(token_address)
print(f"Total Supply: {total_supply:,.2f}")


