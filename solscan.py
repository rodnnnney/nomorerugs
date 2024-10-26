import os
import requests
from dotenv import load_dotenv
import json
import base64
import struct
import base58

load_dotenv()

solscan_api_key = os.getenv('SOLSCAN_API_KEY')

API_BASE_URL = "https://pro-api.solscan.io/v2.0/"

def get_token_holders(token_address):
    # Correct URL to get token holders
    url = f"{API_BASE_URL}token/holders?address={token_address}&page=1&page_size=10"
    headers = {"token": solscan_api_key}
    response = requests.get(url, headers=headers)
    return response.text


def get_token_meta(token_address):
    url = f"{API_BASE_URL}token/meta?address={token_address}"    
    headers = {"token": solscan_api_key}
    response = requests.get(url, headers=headers)
    return response.text


def calculate_percentage_ownership(token_address ,totalSupply):

    data = json.loads(get_token_holders(token_address))

    ownership_list = []
    for holder in data["data"]["items"]:
        rank = holder["rank"]
        address = holder["address"]
        amount = int(holder["amount"])
        percentage = (amount / totalSupply) * 100
        ownership_list.append((rank, address, percentage))

    return ownership_list

def check_mint_authority(token_address):
    """Check if a mint address has a mint authority turned on or off."""
    try:
        url = "https://api.mainnet-beta.solana.com"
        
        # Prepare payload to get account info
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [
                token_address,
                {"encoding": "base64"}
            ]
        }
        
        # Send the request
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        print(data)

        # Check for the presence of result and data
        if 'result' not in data or not data['result'] or 'value' not in data['result']:
            print("No account information found for the given mint address.")
            return None

        # Get the encoded account data
        value = data['result']['value']
        if not value or 'data' not in value or len(value['data']) == 0:
            print("No account data found.")
            return None

        encoded_data = value['data'][0]
        


        # Decode the base64 account data
        account_data = base64.b64decode(encoded_data)

        print(account_data)

        # Extract the mint authority (first 32 bytes)
        mint_authority = account_data[:32]

        mint_authority_address = base58.b58encode(mint_authority).decode('utf-8')

        print(mint_authority_address)


        # Check if the mint authority is set
        if mint_authority == b'\x00' * 32:
            print("Mint authority is turned off (no minting allowed).")
            return "No Mint Authority"
        else:
            print("Mint authority is turned on (minting allowed).")
            return mint_authority.hex()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


token_account_address = "BQYPkPWpYY36eUgt2fbPNrQnvE7Qa5vd5JPjqYvmpump"

check_mint_authority(token_account_address)
