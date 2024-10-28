import requests

def get_token_name(token_address: str, rpc_url: str) -> str:
    """
    Get the name of a Solana token using its mint address via RPC.
    
    Args:
        token_address (str): The mint address of the token
        rpc_url (str): The Solana RPC node URL
        
    Returns:
        str: The name/symbol of the token
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [
            token_address,
            {
                "encoding": "jsonParsed",
                "commitment": "finalized"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(rpc_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        print(data)
        
        if "result" in data and data["result"]["value"]:
            mint_info = data["result"]["value"]["data"]["parsed"]["info"]
            # For SPL tokens, we can get the symbol from the mint data
            if "symbol" in mint_info:
                return mint_info["symbol"]
            # If no symbol, try to get the name
            elif "name" in mint_info:
                return mint_info["name"]
            else:
                return "Unknown Token"
        else:
            raise Exception("No data found for this token address")
            
    except Exception as e:
        raise Exception(f"Error fetching token name: {str(e)}")

def get_token_mint_info(url: str, token_mint_address: str) -> dict:
    """
    Get detailed information about a token mint.
    
    Args:
        url (str): The RPC URL
        token_mint_address (str): The token's mint address
        
    Returns:
        dict: Token information including decimals, authorities, and supply
    """
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getAccountInfo",
        "params": [
            token_mint_address,
            {
                "encoding": "jsonParsed",
                "commitment": "finalized"
            }
        ]
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data and "result" in data and data["result"]["value"]:
            mint_info = data["result"]["value"]["data"]["parsed"]["info"]
            decimals = mint_info["decimals"]
            freeze_authority = mint_info.get("freezeAuthority")
            mint_authority = mint_info.get("mintAuthority")
            supply = mint_info["supply"]
            owner = data["result"]["value"]["owner"]
            
            return {
                "decimals": decimals,
                "freeze_authority": freeze_authority,
                "mint_authority": mint_authority,
                "total_supply": int(supply) / (10 ** decimals),
                "owner" : owner
            }
        else:
            print("No data found for this token address.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# token_mint_address = "62GzFSrcha2QupnSM7BiEwPz4VM1fEFki2Ah7k6bpump"


#     # Get token name
# name = get_token_name(token_mint_address, url)


# #print(f"Token Name/Symbol: {name}")
    
# #     # Get detailed mint info
# result = get_token_mint_info(url, token_mint_address)
# if result:
#     print(f"Decimals: {result['decimals']}")
#     print(f"Freeze Authority: {result['freeze_authority']}")
#     print(f"Mint Authority: {result['mint_authority']}")
#     print(f"Total Supply: {result['total_supply']}")
#     print(f"Owner: {result['owner']}")

# except Exception as e:
#     print(f"Error: {e}")