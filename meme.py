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



    

def coin():

    st.subheader("SWAPs")
    st.markdown("##")
    df = pd.read_csv("nodit_graphql/meme_coins/meme coin.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])

    #df = df.dropna(subset=['CHAIN_PAIR'])

    a,b = st.columns([2,2])
    with a:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='deeppink').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('N_TXS:Q', stack=None, title='N_TXS'),
            color=alt.Color('TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title = 'N_TXS'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='bisque').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('TOTAL_SWAPS:Q', stack=None, title='TOTAL_SWAPS'),
             color=alt.Color('TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_SWAPS'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_line(color='darkkhaki').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('TOTAL_VOLUME:Q', stack=None, title='TOTAL_VOLUME'),
            color=alt.Color('TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_VOLUME'
        ),
        use_container_width=True
    )
        
    with b:
        
        st.altair_chart(
        alt.Chart(df).mark_line(color='firebrick').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('N_USER:Q', stack=None, title='N_USER'),
            color=alt.Color('TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='N_USER'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_line(color='antiquewhite').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('7D-MA Swaps:Q', stack=None, title='7D-MA Swaps'),
            color=alt.Color('TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='7D-MA Swaps'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_line(color='turquoise').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('7D-MA Swappers', stack=None, title='7D-MA Swappers'),
            color=alt.Color('TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='7D-MA Swappers'
        ),
        use_container_width=True
    )
        
    generate_summary_p(df.tail(150))
















    st.markdown("##")
    df = pd.read_csv("nodit_graphql/meme_coins/meme coin_swaps_assets.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])

    df1= pd.read_csv("nodit_graphql/meme_coins/meme coin_swaps.csv")

    df1['DATE'] = pd.to_datetime(df1['DATE'])


    #df = df.dropna(subset=['CHAIN_PAIR'])

    a,b = st.columns([2,2])
    with a:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='deeppink').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('TOTAL_SWAPS:Q', stack=None, title='TOTAL_SWAPS'),
            color=alt.Color('ASSET:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title = 'TOTAL_SWAPS'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='bisque').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('N_USER:Q', stack=None, title='N_USER'),
             color=alt.Color('ASSET:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='N_USER'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='darkkhaki').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('TOTAL_VOLUME:Q', stack=None, title='TOTAL_VOLUME'),
            color=alt.Color('ASSET:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_VOLUME'
        ),
        use_container_width=True
    )
        
    with b:
        
        st.altair_chart(
        alt.Chart(df1).mark_line(color='firebrick').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('TOTAL_SWAPS:Q', stack=None, title='TOTAL_SWAPS'),
            color=alt.Color('TRADE_TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_SWAPS'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df1).mark_line(color='antiquewhite').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('N_USER:Q', stack=None, title='N_USER'),
            color=alt.Color('TRADE_TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='N_USER'
        ),
        use_container_width=True
    )
         
        st.altair_chart(
        alt.Chart(df1).mark_line(color='turquoise').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('TOTAL_VOLUME', stack=None, title='TOTAL_VOLUME'),
            color=alt.Color('TRADE_TYPE:N', legend=alt.Legend(title='PLATFORM'))
        ).properties(
            width=800,
            height=400,
            title='TOTAL_VOLUME'
        ),
        use_container_width=True
    )
        
    generate_summary(df.tail(150))