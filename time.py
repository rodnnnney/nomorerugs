import requests

url = 'https://solana-mainnet.core.chainstack.com/5ee95cf107c3543c6658a90ad2317aa1'

# Mint address of the token
mint_address = "62GzFSrcha2QupnSM7BiEwPz4VM1fEFki2Ah7k6bpump"

# Step 1: Get the list of signatures (transactions) associated with the mint address
payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "getSignaturesForAddress",
    "params": [mint_address, {"limit": 10}]
}

headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

# Print the response (contains transaction signatures)
print(response.json())
