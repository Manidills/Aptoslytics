import requests
import json

def fetch_data(query, endpoint_url):
    # Send the GraphQL request
    try:
        response = requests.post(endpoint_url, json={'query': query})
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}"}
    
    except Exception as e:
        return {"error": f"An exception occurred: {str(e)}"}

# Function to build a query for fungible asset balances
# def build_fungible_asset_balances_query(limit=10, offset=0):
#     query = f"""
#     {{
#       fungible_asset_balances(limit: {limit}, offset: {offset}) {{
#         amount
#         asset_type
#         is_frozen
#         is_primary
#         owner_address
#         token_standard
#         storage_id
#         transaction_timestamp
#         transaction_version
#         metadata {{
#           asset_type
#           creator_address
#           decimals
#           icon_uri
#           last_transaction_timestamp
#           project_uri
#           name
#           supply_v2
#           symbol
#           token_standard
#         }}
#       }}
#     }}
#     """
#     return query

# URL for the GraphQL endpoint
endpoint_url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"

# Example usage
limit = 10  # Customize the limit
offset = 0  # Customize the offset

# Build the query
query = build_fungible_asset_balances_query(limit, offset)

# Fetch the data
result = fetch_data(query, endpoint_url)

# Print the fetched data
print(json.dumps(result, indent=2))
