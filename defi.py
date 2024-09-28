from io import StringIO
import requests
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import time
import os
import g4f

def get_response(prompt):
    url = f"https://api.kastg.xyz/api/ai/chatgptV4?prompt={prompt}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("status") == "true" and json_response.get("result"):
                return json_response["result"][0]["response"]
            else:
                return "Error in API response"
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
    

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
    prompt = f"Here aptos blockchain data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and suggest us a good time for the investments in points"
    st.write(chat_bot(prompt))

@st.cache_resource
def generate_summary_p(df):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here aptos blockchain data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and in points"
    st.write(chat_bot(prompt))



    

def defi():

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/defi/APTOS Daily Bridge Volume and Activity Analysis.csv")

    df['ACTIVITY_DATE'] = pd.to_datetime(df['ACTIVITY_DATE'])

    df = df.dropna(subset=['CHAIN_PAIR'])

    a,b = st.columns([2,2])
    with a:
         st.altair_chart(
        alt.Chart(df).mark_circle(color='deeppink').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('TOTAL_TRANSACTIONS:Q', stack=None, title='TOTAL_TRANSACTIONS'),
            color=alt.Color('CHAIN_PAIR:N', legend=alt.Legend(title='CHAIN_PAIR'))
        ).properties(
            width=800,
            height=400,
            title = 'Transactions'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_circle(color='bisque').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('UNIQUE_USERS:Q', stack=None, title='UNIQUE_USERS'),
             color=alt.Color('CHAIN_PAIR:N', legend=alt.Legend(title='CHAIN_PAIR'))
        ).properties(
            width=800,
            height=400,
            title='UNIQUE_USERS'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_circle(color='darkkhaki').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('TOTAL_RAW_AMOUNT:Q', stack=None, title='TOTAL_RAW_AMOUNT'),
            color=alt.Color('CHAIN_PAIR:N', legend=alt.Legend(title='CHAIN_PAIR'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_RAW_AMOUNT'
        ),
        use_container_width=True
    )
         st.altair_chart(
        alt.Chart(df).mark_circle(color='firebrick').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('AVG_RAW_AMOUNT_PER_TX:Q', stack=None, title='AVG_RAW_AMOUNT_PER_TX'),
            color=alt.Color('CHAIN_PAIR:N', legend=alt.Legend(title='CHAIN_PAIR'))
        ).properties(
            width=800,
            height=400,
            title='AVG_RAW_AMOUNT_PER_TX'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_circle(color='antiquewhite').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('AVG_RAW_AMOUNT_PER_TX_CALCULATED:Q', stack=None, title='AVG_RAW_AMOUNT_PER_TX_CALCULATED'),
            color=alt.Color('CHAIN_PAIR:N', legend=alt.Legend(title='CHAIN_PAIR'))
        ).properties(
            width=800,
            height=400,
            title='AVG_RAW_AMOUNT_PER_TX_CALCULATED'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_circle(color='turquoise').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('USERS_PER_TRANSACTION_RATIO', stack=None, title='USERS_PER_TRANSACTION_RATIO'),
            color=alt.Color('CHAIN_PAIR:N', legend=alt.Legend(title='CHAIN_PAIR'))
        ).properties(
            width=800,
            height=400,
            title='USERS_PER_TRANSACTION_RATIO'
        ),
        use_container_width=True
    )
    with b:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='deeppink').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('TOTAL_TRANSACTIONS:Q', stack=None, title='TOTAL_TRANSACTIONS'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title = 'Transactions'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='bisque').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('UNIQUE_USERS:Q', stack=None, title='UNIQUE_USERS'),
             color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='UNIQUE_USERS'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='darkkhaki').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('TOTAL_RAW_AMOUNT:Q', stack=None, title='TOTAL_RAW_AMOUNT'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_RAW_AMOUNT'
        ),
        use_container_width=True
    )
        st.altair_chart(
        alt.Chart(df).mark_bar(color='firebrick').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('AVG_RAW_AMOUNT_PER_TX:Q', stack=None, title='AVG_RAW_AMOUNT_PER_TX'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='AVG_RAW_AMOUNT_PER_TX'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='antiquewhite').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('AVG_RAW_AMOUNT_PER_TX_CALCULATED:Q', stack=None, title='AVG_RAW_AMOUNT_PER_TX_CALCULATED'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='AVG_RAW_AMOUNT_PER_TX_CALCULATED'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_square(color='turquoise').encode(
            x=alt.X('ACTIVITY_DATE:T', title='DATE'),
            y=alt.Y('USERS_PER_TRANSACTION_RATIO', stack=None, title='USERS_PER_TRANSACTION_RATIO'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='USERS_PER_TRANSACTION_RATIO'
        ),
        use_container_width=True
    )
        
    generate_summary(df.tail(90))







    st.markdown("##")
    df = pd.read_csv("nodit_graphql/defi/APTOS Daily DEX Swap Volume and Activity by Platform.csv")

    df['SWAP_DATE'] = pd.to_datetime(df['SWAP_DATE'])

    st.subheader("SWAPs")
    st.markdown("##")

    #df = df.dropna(subset=['CHAIN_PAIR'])

    a,b = st.columns([2,2])
    with a:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='deeppink').encode(
            x=alt.X('SWAP_DATE:T', title='DATE'),
            y=alt.Y('TOTAL_SWAPS:Q', stack=None, title='TOTAL_SWAPS'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title = 'TOTAL_SWAPS'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='bisque').encode(
            x=alt.X('SWAP_DATE:T', title='DATE'),
            y=alt.Y('UNIQUE_SWAPPERS:Q', stack=None, title='UNIQUE_SWAPPERS'),
             color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='UNIQUE_SWAPPERS'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='darkkhaki').encode(
            x=alt.X('SWAP_DATE:T', title='DATE'),
            y=alt.Y('TOTAL_AMOUNT_IN:Q', stack=None, title='TOTAL_AMOUNT_IN'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_AMOUNT_IN'
        ),
        use_container_width=True
    )
        
    with b:
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='firebrick').encode(
            x=alt.X('SWAP_DATE:T', title='DATE'),
            y=alt.Y('TOTAL_AMOUNT_OUT:Q', stack=None, title='TOTAL_AMOUNT_OUT'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_AMOUNT_OUT'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='antiquewhite').encode(
            x=alt.X('SWAP_DATE:T', title='DATE'),
            y=alt.Y('UNIQUE_TOKENS_IN:Q', stack=None, title='UNIQUE_TOKENS_IN'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='UNIQUE_TOKENS_IN'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_square(color='turquoise').encode(
            x=alt.X('SWAP_DATE:T', title='DATE'),
            y=alt.Y('UNIQUE_TOKENS_OUT', stack=None, title='UNIQUE_TOKENS_OUT'),
            color=alt.Color('PLATFORM:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='UNIQUE_TOKENS_OUT'
        ),
        use_container_width=True
    )
        
    generate_summary(df.tail(150))



    st.markdown("##")

    st.data_editor(pd.read_csv("nodit_graphql/defi/Aptos Defi Bridge Platforms.csv"))



