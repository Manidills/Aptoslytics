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



    

def home():


    st.markdown("##")
    df = pd.read_csv("nodit_graphql/aptos_vs_rest/All - Average Daily TPS Per chain copy.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])

    # Chart title and description
    st.markdown("## Average Daily TPS Per chain")
    st.markdown("##")

    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('TOTAL_USER:Q', stack=None, title='TOTAL_USER'),
            color=alt.Color('CHAIN:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400
        ),
        use_container_width=True
    )
    


    a,b = st.columns([2,2])
    with a:
         st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('TPS:Q', stack=None, title='TPS'),
            color=alt.Color('CHAIN:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400
        ),
        use_container_width=True
    )
    with b:
        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                x=alt.X('DATE:T', title='DATE'),
                y=alt.Y('TOTAL_TX:Q', stack=None, title='TOTAL_TX'),
                color=alt.Color('CHAIN:N', legend=alt.Legend(title='CHAIN'))
            ).properties(
                width=800,
                height=400
            ),
            use_container_width=True
        )

    generate_summary_p(df)

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/aptos_vs_rest/Average Price Changes.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])

    # Chart title and description
    st.markdown("## Average Price Changes [24h]")
    st.markdown("##")

    a,b = st.columns([2,2])
    with a:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='blueviolet').encode(
            x=alt.X('SYMBOLS', title='SYMBOLS'),
            y=alt.Y('Price Changes', stack=None, title='Price Changes'),
        ).properties(
            width=800,
            height=400
        ),
        use_container_width=True
    )
    with b:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='brown').encode(
            x=alt.X('TYPE', title='TYPE'),
            y=alt.Y('Price Changes', stack=None, title='Price Changes'),
        ).properties(
            width=800,
            height=400
        ),
        use_container_width=True
    )
        
    generate_summary_p(df)

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/aptos_vs_rest/Average Success Rate.csv")

    # Chart title and description
    st.markdown("## Average Success Rate")
    st.markdown("##")

    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_bar(color='green').encode(
            x=alt.X('CHAIN', title='CHAIN'),
            y=alt.Y('TOTAL_TXS', stack=None, title='TOTAL_TXS'),
            color=alt.Color('STATUS:N', legend=alt.Legend(title='STATUS'))
        ).properties(
            width=800,
            height=400
        ),
        use_container_width=True
    )

    generate_summary_p(df)

    st.markdown("##")

    df = pd.read_csv("nodit_graphql/aptos_vs_rest/Block Time.csv")
    # Chart title and description
    st.markdown("## Block Time")
    st.markdown("##")


    a,b = st.columns([2,2])
    with a:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='darkorange').encode(
            x=alt.X('CHAIN', title='CHAIN'),
            y=alt.Y('Average Time', stack=None, title='Price Changes'),
        ).properties(
            width=800,
            height=400
        ),
        use_container_width=True
    )
    with b:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='honeydew').encode(
            x=alt.X('TYPE', title='TYPE'),
            y=alt.Y('Average Time', stack=None, title='Average Time'),
        ).properties(
            width=800,
            height=400
        ),
        use_container_width=True
    )
        
    generate_summary_p(df)

    st.markdown("##")

    df = pd.read_csv("nodit_graphql/aptos_vs_rest/fee.csv")
    # Chart title and description
    st.markdown("## Fee")
    st.markdown("##")



    st.altair_chart(
    alt.Chart(df).mark_bar(color='red').encode(
        x=alt.X('CHAIN', title='CHAIN'),
        y=alt.Y('AVG_FEE', stack=None, title='AVG_FEE'),
    ).properties(
        width=800,
        height=400
    ),
    use_container_width=True
)

    generate_summary(df)    





