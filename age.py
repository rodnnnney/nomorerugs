import asyncio
from solana.rpc.async_api import AsyncClient

async def get_first_transaction(token_address):
    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        # Fetch signatures for the token mint address
        before_signature = None
        earliest_transaction = None

        while True:
            # Get signatures for address (paginated)
            resp = await client.get_signatures_for_address(token_address, before=before_signature, limit=1000)

            if not resp["result"]:
                break  # No more transactions

            # Update earliest transaction (last one in current batch)
            earliest_transaction = resp["result"][-1]["signature"]
            before_signature = resp["result"][-1]["signature"]

            # If there are fewer than 1000 results, we've reached the end
            if len(resp["result"]) < 1000:
                break

        # If no transactions found, return
        if not earliest_transaction:
            print("No transactions found for this token address.")
            return

        # Fetch the details of the earliest transaction
        transaction_details = await client.get_transaction(earliest_transaction)
        print(f"First transaction signature: {earliest_transaction}")
        print(f"Transaction details: {transaction_details['result']}")

# Example usage
token_address = "BQYPkPWpYY36eUgt2fbPNrQnvE7Qa5vd5JPjqYvmpump"
asyncio.run(get_first_transaction(token_address))
