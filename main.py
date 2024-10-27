from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import os
import uvicorn

from distribution import get_unique_holders_count, get_token_supply, get_largest_token_accounts
from mc import calculate_fully_diluted_market_cap
from mint import get_token_mint_info
from price import get_token_price_in_usdc

app = FastAPI()

load_dotenv()
URL = os.getenv("CHAIN_STACK")

@app.get("/token-info")
async def get_token_info(
    token_mint_address: str = Query(..., description="The token mint address")
):
    try:
        # Retrieve token price
        token_price = get_token_price_in_usdc(token_mint_address)
        if token_price is not None:
            token_price = f'{token_price:.10f}'  # Format with 10 decimal places

        # Retrieve unique holder count
        holder_count = get_unique_holders_count(token_mint_address, URL)
        
        # Retrieve fully diluted market cap
        fully_diluted_market_cap = calculate_fully_diluted_market_cap(token_mint_address, URL)
        
        # Retrieve token mint information
        result = get_token_mint_info(URL, token_mint_address)

        # Retrieve total supply
        total_supply = get_token_supply(URL, token_mint_address)

        # Retrieve largest token accounts
        largest_accounts = get_largest_token_accounts(URL, token_mint_address, total_supply)

        if result:
            # Format the total supply with commas
            formatted_total_supply = f"{total_supply:,}"
            
            # Return the results as a JSON response
            return {
                "owner" : result.get('owner'),
                "holder_count": holder_count,
                "total_supply": formatted_total_supply,
                "fully_diluted_market_cap": fully_diluted_market_cap,
                "decimals": result.get("decimals"),
                "freeze_authority": result.get("freeze_authority"),
                "mint_authority": result.get("mint_authority"),
                "token_price": token_price,
                "largest_accounts": largest_accounts
            }
        else:
            raise HTTPException(status_code=404, detail="Token mint info not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, reload=True)
    
