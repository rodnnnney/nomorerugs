import json
from solscan import get_token_holders, get_token_holders, solscan_api_key, calculate_percentage_ownership, get_token_meta, get_metadata_account
from mint import check_mint_authority
from liquidity import is_token_locked
from solana.rpc.async_api import AsyncClient


def calculate_distribution(token_address):
    
    data = json.loads(get_token_meta(token_address))

    token_name = data['data']['name']
    icon = data['data']['icon']
    total_supply = int(data["data"]["supply"])
    
    #daily_trading_volume = data['data']['volume_24h']

    print(f'{token_name}, {total_supply}, {icon}')
    return token_name, total_supply, icon


print(solscan_api_key)
# token_name = '6MQ8D4XgoLTPGgkz7sbJdFzA6F6iuepFXE2BtV9npump'

# name, supply, icon = calculate_distribution(token_name)

# for x in calculate_percentage_ownership(token_name, supply):
#     print(x)

# if is_token_locked(token_name):
#     print("The liquidity is locked.")
# else:
#     print("The liquidity is NOT locked.")

get_metadata_account('BQYPkPWpYY36eUgt2fbPNrQnvE7Qa5vd5JPjqYvmpump')









