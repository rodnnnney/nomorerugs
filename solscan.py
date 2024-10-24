import os
import requests
from dotenv import load_dotenv
import json

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


def calculate_percentage_ownership(json_data, totalSupply):
    data = json.loads(json_data)

    ownership_list = []
    for holder in data["data"]["items"]:
        rank = holder["rank"]
        address = holder["address"]
        amount = int(holder["amount"])
        percentage = (amount / totalSupply) * 100
        ownership_list.append((rank, address, percentage))

    return ownership_list
