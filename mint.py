import asyncio
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from spl.token._layouts import MINT_LAYOUT
import base64

async def check_mint_details(token_address):
    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        mint_pubkey = PublicKey(token_address)
        

        resp = await client.get_account_info(mint_pubkey)
        
        if resp['result']['value'] is None:
            print("Mint account not found")
            return
        

        data_base64 = resp['result']['value']['data'][0]
        data = base64.b64decode(data_base64)
    

        mint_info = MINT_LAYOUT.parse(data)


        if mint_info.mint_authority_option == 0:
            print("Mint authority is disabled (None)")
        else:
            mint_authority = PublicKey(mint_info.mintAuthority)
            print(f"Mint authority is enabled: {mint_authority}")
        

        supply = mint_info.supply
        print(f"Supply: {supply}")


        decimals = mint_info.decimals
        print(f"Decimals: {decimals}")


        if mint_info.freeze_authority_option == 0:
            print("Freeze authority is disabled (None)")
        else:
            freeze_authority = PublicKey(mint_info.freezeAuthority)
            print(f"Freeze authority is enabled: {freeze_authority}")
            

asyncio.run(check_mint_details('BQYPkPWpYY36eUgt2fbPNrQnvE7Qa5vd5JPjqYvmpump'))
