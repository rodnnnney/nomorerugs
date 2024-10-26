from solana.rpc.api import Client
from solana.publickey import PublicKey
import base64

# Solana RPC client initialization
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
client = Client(SOLANA_RPC_URL)

# List of known programs associated with locking mechanisms
KNOWN_LOCK_PROGRAMS = [
    "AMM1wERo9JcYwn7ju2X7bRYph2pp8yRD9LzeXZJFEud",  # Raydium AMM Program ID
    "9W5ZmZyU44KfY8tYGRiXp1KtE35TbZ3PQk6z8jbcZdkh",  # Orca Program ID


]

def is_token_locked(token_account_address: str) -> bool:
    """Check if the liquidity for the given token account is locked."""
    # Fetch account info
    response = client.get_account_info(PublicKey(token_account_address))
    account_info = response['result']['value']
    
    if account_info is None:
        print("Token account not found.")
        return False

    # Decode the base64 encoded data
    encoded_data = account_info['data'][0]
    decoded_data = base64.b64decode(encoded_data)

    # Check the owner field to see who controls the token account
    owner = account_info['owner']
    
    # Check if the owner is a known locking program or Raydium program
    is_locked = owner in KNOWN_LOCK_PROGRAMS

    return is_locked


