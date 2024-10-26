import requests


def get_token_supply(token_address):
    url = f"https://api.solana.fm/v1/tokens/{token_address}/supply"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    print(response.text)

    #{
    #   "circulatingSupply": 999983313.490495,
    #   "tokenWithheldAmount": null,
    #   "userTotalWithheldAmount": 0,
    #   "totalWithheldAmount": 0,
    #   "realCirculatingSupply": 999983313.490495,
    #   "decimals": 6
    # }

token_address = "BQYPkPWpYY36eUgt2fbPNrQnvE7Qa5vd5JPjqYvmpump"
# get_token_supply(token_address)


def get_meta_data(token_address):
    url = f'https://solana.fm/account/{token_address}'

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    print(response.text)

get_meta_data(token_address)