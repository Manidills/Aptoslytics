from io import StringIO
import streamlit as st
import pandas as pd
import requests
import json
from pyvis.network import Network
import tempfile
import g4f
from streamlit.components.v1 import html


def chat_bot(prompt):
    response = g4f.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model=g4f.models.default,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    return response


@st.cache_resource
def generate_summary(df):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here ssv network staking related data\n{csv_data_str}\ngive some short summary insights about the data in  points"
    st.write(chat_bot(prompt))


def create_coin_activities_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=10)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query with user input
        query = f"""
        {{
          coin_activities(offset: {offset}, limit: {limit}) {{
            activity_type
            block_height
            coin_type
            entry_function_id_str
            event_account_address
            event_creation_number
            event_index
            event_sequence_number
            is_gas_fee
            is_transaction_success
            owner_address
            storage_refund_amount
            transaction_timestamp
            transaction_version
            coin_info {{
              coin_type
              coin_type_hash
              name
              creator_address
              symbol
            }}
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['coin_activities'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['coin_activities']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for activity in data['coin_activities']:
            transaction_version = activity['transaction_version']
            activity_type = activity['activity_type']
            owner_address = activity['owner_address']
            coin_info = activity['coin_info']

            # Adding main activity node
            activity_node_id = f"Activity: {transaction_version}"
            nodes.append({'id': activity_node_id, 'label': f"{activity_type} ({transaction_version})",
                          'title': f"Owner: {owner_address}"})

            # Adding coin info node
            coin_type_node_id = f"Coin Type: {coin_info['coin_type']}"
            nodes.append({'id': coin_type_node_id, 'label': coin_info['name'],
                          'title': f"Symbol: {coin_info['symbol']}, Creator: {coin_info['creator_address']}"})
            edges.append({'source': activity_node_id, 'target': coin_type_node_id})

            # Adding event account address node
            event_account_node_id = f"Event Account: {activity['event_account_address']}"
            nodes.append({'id': event_account_node_id, 'label': activity['event_account_address'], 'title': ''})
            edges.append({'source': activity_node_id, 'target': event_account_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_collection_datas_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          current_collection_datas(limit: {limit}, offset: {offset}) {{
            collection_data_id_hash
            collection_name
            creator_address
            metadata_uri
            supply
            table_handle
            uri_mutable
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['current_collection_datas'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['current_collection_datas']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for collection in data['current_collection_datas']:
            collection_node_id = f"Collection: {collection['collection_data_id_hash']}"
            nodes.append({'id': collection_node_id, 'label': collection['collection_name'],
                          'title': f"Creator: {collection['creator_address']}"})

            # Adding creator node
            creator_node_id = f"Creator: {collection['creator_address']}"
            nodes.append({'id': creator_node_id, 'label': collection['creator_address'], 'title': "Creator Address"})
            edges.append({'source': collection_node_id, 'target': creator_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_delegator_balances_graph():
    # User input for the query parameters
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = """
        {
          current_delegator_balances {
            delegator_address
            last_transaction_version
            parent_table_handle
            pool_address
            pool_type
            shares
            table_handle
            current_pool_balance {
              active_table_handle
              inactive_table_handle
              last_transaction_version
              staking_pool_address
              total_coins
              total_shares
            }
            staking_pool_metadata {
              last_transaction_version
              operator_address
              staking_pool_address
              voter_address
            }
          }
        }
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['current_delegator_balances'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['current_delegator_balances']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for balance in data['current_delegator_balances']:
            delegator_address = balance['delegator_address']
            pool_address = balance['pool_address']
            current_pool_balance = balance['current_pool_balance']
            staking_pool_metadata = balance['staking_pool_metadata']

            # Adding delegator node
            delegator_node_id = f"Delegator: {delegator_address}"
            nodes.append({'id': delegator_node_id, 'label': delegator_address, 'title': f"Shares: {balance['shares']}"})

            # Adding pool node
            pool_node_id = f"Pool: {pool_address}"
            nodes.append({'id': pool_node_id, 'label': pool_address, 'title': f"Pool Type: {balance['pool_type']}"})
            edges.append({'source': delegator_node_id, 'target': pool_node_id})

            # Adding current pool balance node
            pool_balance_node_id = f"Pool Balance: {current_pool_balance['staking_pool_address']}"
            nodes.append({'id': pool_balance_node_id, 'label': f"Total Coins: {current_pool_balance['total_coins']}",
                          'title': f"Total Shares: {current_pool_balance['total_shares']}"})
            edges.append({'source': pool_node_id, 'target': pool_balance_node_id})

            # Adding staking pool metadata node
            metadata_node_id = f"Metadata: {staking_pool_metadata['staking_pool_address']}"
            nodes.append({'id': metadata_node_id, 'label': staking_pool_metadata['operator_address'],
                          'title': "Voter Address: " + staking_pool_metadata['voter_address']})
            edges.append({'source': pool_node_id, 'target': metadata_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_token_datas_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          current_token_datas(limit: {limit}, offset: {offset}) {{
            collection_data_id_hash
            collection_name
            creator_address
            metadata_uri
            name
            payee_address
            token_data_id_hash
            supply
            uri_mutable
            current_collection_data {{
              collection_data_id_hash
              collection_name
              creator_address
              metadata_uri
              uri_mutable
            }}
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['current_token_datas'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['current_token_datas']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for token in data['current_token_datas']:
            token_node_id = f"Token: {token['token_data_id_hash']}"
            nodes.append(
                {'id': token_node_id, 'label': token['name'], 'title': f"Collection: {token['collection_name']}"})

            # Adding collection node
            collection_node_id = f"Collection: {token['collection_data_id_hash']}"
            nodes.append({'id': collection_node_id, 'label': token['collection_name'],
                          'title': f"Creator: {token['creator_address']}"})
            edges.append({'source': token_node_id, 'target': collection_node_id})

            # Adding creator node
            creator_node_id = f"Creator: {token['creator_address']}"
            nodes.append({'id': creator_node_id, 'label': token['creator_address'], 'title': "Creator Address"})
            edges.append({'source': collection_node_id, 'target': creator_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_token_ownerships_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          current_token_ownerships(limit: {limit}, offset: {offset}) {{
            amount
            collection_data_id_hash
            collection_name
            creator_address
            last_transaction_timestamp
            last_transaction_version
            name
            owner_address
            table_type
            token_properties
            current_collection_data {{
              collection_data_id_hash
              collection_name
              creator_address
              metadata_uri
              uri_mutable
            }}
            current_token_data {{
              collection_data_id_hash
              collection_name
              creator_address
              metadata_uri
              payee_address
              uri_mutable
              token_data_id_hash
              current_collection_data {{
                collection_data_id_hash
                collection_name
                creator_address
                metadata_uri
                uri_mutable
              }}
            }}
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['current_token_ownerships'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['current_token_ownerships']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for ownership in data['current_token_ownerships']:
            ownership_node_id = f"Ownership: {ownership['current_token_data']['token_data_id_hash']}"
            nodes.append(
                {'id': ownership_node_id, 'label': ownership['name'], 'title': f"Owner: {ownership['owner_address']}"})

            # Adding collection node
            collection_node_id = f"Collection: {ownership['collection_data_id_hash']}"
            nodes.append({'id': collection_node_id, 'label': ownership['collection_name'],
                          'title': f"Creator: {ownership['creator_address']}"})
            edges.append({'source': ownership_node_id, 'target': collection_node_id})

            # Adding creator node
            creator_node_id = f"Creator: {ownership['creator_address']}"
            nodes.append({'id': creator_node_id, 'label': ownership['creator_address'], 'title': "Creator Address"})
            edges.append({'source': collection_node_id, 'target': creator_node_id})

            # Adding current token data node
            token_node_id = f"Token: {ownership['current_token_data']['token_data_id_hash']}"
            nodes.append({'id': token_node_id, 'label': ownership['current_token_data']['collection_name'],
                          'title': f"Payee: {ownership['current_token_data']['payee_address']}"})
            edges.append({'source': ownership_node_id, 'target': token_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_delegator_pools_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          delegator_distinct_pool(limit: {limit}, offset: {offset}) {{
            delegator_address
            pool_address
            current_pool_balance {{
              active_table_handle
              inactive_table_handle
              last_transaction_version
              staking_pool_address
              total_coins
              total_shares
              operator_commission_percentage
            }}
            staking_pool_metadata {{
              last_transaction_version
              operator_address
              staking_pool_address
              voter_address
            }}
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['delegator_distinct_pool'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['delegator_distinct_pool']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for pool in data['delegator_distinct_pool']:
            delegator_address = pool['delegator_address']
            pool_address = pool['pool_address']
            current_pool_balance = pool['current_pool_balance']
            staking_pool_metadata = pool['staking_pool_metadata']

            # Adding delegator node
            delegator_node_id = f"Delegator: {delegator_address}"
            nodes.append({'id': delegator_node_id, 'label': delegator_address, 'title': "Delegator"})

            # Adding pool node
            pool_node_id = f"Pool: {pool_address}"
            nodes.append({'id': pool_node_id, 'label': pool_address,
                          'title': f"Total Coins: {current_pool_balance['total_coins']}"})
            edges.append({'source': delegator_node_id, 'target': pool_node_id})

            # Adding current pool balance node
            pool_balance_node_id = f"Pool Balance: {current_pool_balance['staking_pool_address']}"
            nodes.append({'id': pool_balance_node_id, 'label': f"Total Shares: {current_pool_balance['total_shares']}",
                          'title': "Current Pool Balance"})
            edges.append({'source': pool_node_id, 'target': pool_balance_node_id})

            # Adding staking pool metadata node
            metadata_node_id = f"Metadata: {staking_pool_metadata['staking_pool_address']}"
            nodes.append({'id': metadata_node_id, 'label': staking_pool_metadata['operator_address'],
                          'title': "Voter Address: " + staking_pool_metadata['voter_address']})
            edges.append({'source': pool_node_id, 'target': metadata_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_events_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          events(offset: {offset}, limit: {limit}) {{
            account_address
            creation_number
            data
            event_index
            indexed_type
            sequence_number
            transaction_block_height
            transaction_version
            type
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['events'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['events']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for event in data['events']:
            event_node_id = f"Event: {event['transaction_version']}_{event['event_index']}"
            nodes.append({'id': event_node_id, 'label': event['type'],
                          'title': f"Account: {event['account_address']}, Data: {event['data']}"})

            # Adding connections to the account address
            account_node_id = f"Account: {event['account_address']}"
            nodes.append({'id': account_node_id, 'label': event['account_address'], 'title': "Account Address"})
            edges.append({'source': event_node_id, 'target': account_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_fungible_asset_balances_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          fungible_asset_balances(limit: {limit}, offset: {offset}) {{
            amount
            asset_type
            is_frozen
            is_primary
            owner_address
            token_standard
            storage_id
            transaction_timestamp
            transaction_version
            metadata {{
              asset_type
              creator_address
              decimals
              icon_uri
              last_transaction_timestamp
              project_uri
              name
              supply_v2
              symbol
              token_standard
            }}
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['fungible_asset_balances'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['fungible_asset_balances']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for balance in data['fungible_asset_balances']:
            owner_address = balance['owner_address']
            asset_type = balance['asset_type']
            amount = balance['amount']
            metadata = balance['metadata']

            # Adding asset balance node
            balance_node_id = f"Balance: {owner_address}_{asset_type}"
            nodes.append(
                {'id': balance_node_id, 'label': f"{metadata['name']} ({asset_type})", 'title': f"Amount: {amount}"})

            # Adding owner node
            owner_node_id = f"Owner: {owner_address}"
            nodes.append({'id': owner_node_id, 'label': owner_address, 'title': "Owner Address"})
            edges.append({'source': balance_node_id, 'target': owner_node_id})

            # Adding creator node
            creator_node_id = f"Creator: {metadata['creator_address']}"
            nodes.append({'id': creator_node_id, 'label': metadata['creator_address'], 'title': "Creator Address"})
            edges.append({'source': balance_node_id, 'target': creator_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_token_activities_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          token_activities(limit: {limit}, offset: {offset}) {{
            collection_data_id_hash
            collection_name
            creator_address
            event_creation_number
            event_account_address
            event_index
            event_sequence_number
            from_address
            name
            property_version
            to_address
            token_amount
            token_data_id_hash
            transaction_timestamp
            transaction_version
            transfer_type
            current_token_data {{
              collection_data_id_hash
              collection_name
              creator_address
              metadata_uri
              payee_address
              current_collection_data {{
                collection_data_id_hash
                collection_name
                creator_address
                description
                metadata_uri
                supply
                uri_mutable
              }}
              last_transaction_timestamp
              token_data_id_hash
              uri_mutable
            }}
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['token_activities'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['token_activities']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for activity in data['token_activities']:
            activity_node_id = f"Activity: {activity['transaction_version']}_{activity['event_index']}"
            nodes.append({'id': activity_node_id, 'label': activity['name'],
                          'title': f"From: {activity['from_address']}, To: {activity['to_address']}, "})

            # Adding from address node
            from_node_id = f"From: {activity['from_address']}"
            nodes.append({'id': from_node_id, 'label': activity['from_address'], 'title': "Sender Address"})
            edges.append({'source': activity_node_id, 'target': from_node_id})

            # Adding to address node
            to_node_id = f"To: {activity['to_address']}"
            nodes.append({'id': to_node_id, 'label': activity['to_address'], 'title': "Receiver Address"})
            edges.append({'source': activity_node_id, 'target': to_node_id})

            # Adding current token data node
            token_data = activity
            token_data_node_id = f"Token Data: {token_data['token_data_id_hash']}"
            nodes.append({'id': token_data_node_id, 'label': token_data['collection_name'], 'title': "Token Metadata"})
            edges.append({'source': activity_node_id, 'target': token_data_node_id})

            # Adding collection data node
            # collection_data = token_data['current_collection_data']
            collection_node_id = f"Collection: {token_data['collection_data_id_hash']}"
            nodes.append(
                {'id': collection_node_id, 'label': token_data['collection_name'], 'title': "Collection Metadata"})
            edges.append({'source': token_data_node_id, 'target': collection_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_tokens_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          tokens(offset: {offset}, limit: {limit}) {{
            collection_data_id_hash
            collection_name
            name
            creator_address
            property_version
            token_data_id_hash
            token_properties
            transaction_timestamp
            transaction_version
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['tokens'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['tokens']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for token in data['tokens']:
            token_node_id = f"Token: {token['token_data_id_hash']}"
            nodes.append({'id': token_node_id, 'label': token['name'],
                          'title': f"Collection: {token['collection_name']}, Creator: {token['creator_address']}"})

            # Adding collection node
            collection_node_id = f"Collection: {token['collection_data_id_hash']}"
            nodes.append({'id': collection_node_id, 'label': token['collection_name'], 'title': "Collection Metadata"})
            edges.append({'source': token_node_id, 'target': collection_node_id})

            # Adding creator node
            creator_node_id = f"Creator: {token['creator_address']}"
            nodes.append({'id': creator_node_id, 'label': token['creator_address'], 'title': "Creator Address"})
            edges.append({'source': token_node_id, 'target': creator_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_user_transactions_graph():
    # User input for the query parameters
    limit = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    offset = st.number_input("Offset for records", min_value=0, value=0)
    submit_button = st.button('Sumit')

    if submit_button:
        # Constructing the query
        query = f"""
        {{
          user_transactions(limit: {limit}, offset: {offset}) {{
            block_height
            entry_function_id_str
            epoch
            expiration_timestamp_secs
            gas_unit_price
            max_gas_amount
            parent_signature_type
            sender
            sequence_number
            timestamp
            version
          }}
        }}
        """

        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://aptos-mainnet.nodit.io/Skr_t-4IDJOOcT1v9o-TX7KWQurJ~9WU/v1/graphql"  # Replace with your actual endpoint
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['user_transactions'])

            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['user_transactions']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for transaction in data['user_transactions']:
            transaction_node_id = f"Transaction: {transaction['version']}"
            nodes.append({'id': transaction_node_id, 'label': f"Tx: {transaction['version']}",
                          'title': f"Sender: {transaction['sender']}, Block Height: {transaction['block_height']}"})

            # Adding sender node
            sender_node_id = f"Sender: {transaction['sender']}"
            nodes.append({'id': sender_node_id, 'label': transaction['sender'], 'title': "Sender Address"})
            edges.append({'source': transaction_node_id, 'target': sender_node_id})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def graph():
    st.markdown("### Select an Option")
    option = st.radio(
        "Select Choice",
        ("CoinActivities", "CollectionData", "CurrentDelegatorBalances",
         "CurrentTokenDatas", "CurrentTokenOwnership", "DelegatorPools", "Events", "FungibleAssetBalances",
         "TokenActivities", "Tokens", "UserTransactions"),
        index=0,
        horizontal=True
    )

    if option == 'CoinActivities':
        html_content = create_coin_activities_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'CollectionData':
        html_content = create_collection_datas_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'CurrentDelegatorBalances':
        html_content = create_delegator_balances_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'CurrentTokenDatas':
        html_content = create_token_datas_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'CurrentTokenOwnership':
        html_content = create_token_ownerships_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'DelegatorPools':
        html_content = create_delegator_pools_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Events':
        html_content = create_events_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'FungibleAssetBalances':
        html_content = create_fungible_asset_balances_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'TokenActivities':
        html_content = create_token_activities_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Tokens':
        html_content = create_fungible_asset_balances_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'UserTransactions':
        html_content = create_fungible_asset_balances_graph()
        st.components.v1.html(html_content, height=800)
