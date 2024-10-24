import json
from solscan import get_token_holders, get_token_holders, solscan_api_key, calculate_percentage_ownership, get_token_meta


def calculate_distribution(json_data):
    data = json.loads(json_data)

    token_name = data['data']['name']
    icon = data['data']['icon']
    total_supply = int(data["data"]["supply"])
    

    #daily_trading_volume = data['data']['volume_24h']


    print(f'{token_name}, {total_supply}, {icon}')
    return token_name, total_supply, icon




#BQYPkPWpYY36eUgt2fbPNrQnvE7Qa5vd5JPjqYvmpump



print("\nTop Token Holders:")
print(solscan_api_key)

token_name, token_supply, icon = (calculate_distribution(get_token_meta('6yqour7y6hJKRP7Y4xK24ijww8FqGKNCzyTAdjMRpump')))

for x in (calculate_percentage_ownership(get_token_holders('6yqour7y6hJKRP7Y4xK24ijww8FqGKNCzyTAdjMRpump'), token_supply)):
    print(x)


