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



    

def dex():


    st.markdown("##")
    df = pd.read_csv("nodit_graphql/dex/Aptos DEXs Volume by Platform.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('VOLUME_USD:Q', stack=None, title='Volume (USD)'),
            color=alt.Color('PROTOCOL:N', legend=alt.Legend(title='PROTOCOL'))
        ).properties(
            width=800,
            height=400,
            title = 'Volume (USD)'
        ),
        use_container_width=True
    )

    generate_summary(df)

    st.markdown("##")

    df = pd.read_csv("nodit_graphql/dex/Dexes on Aptos Over time.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])

    


    a,b = st.columns([2,2])
    with a:
         st.altair_chart(
        alt.Chart(df).mark_bar(color='deeppink').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('# Tx:Q', stack=None, title='Transactions')
        ).properties(
            width=800,
            height=400,
            title = 'Transactions'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_bar(color='firebrick').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Avg Fee per Tx:Q', stack=None, title='Avg Fee per Tx')
        ).properties(
            width=800,
            height=400,
            title='Avg Fee per Tx'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_bar(color='antiquewhite').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Avg Fee per User', stack=None, title='Avg Fee per User')
        ).properties(
            width=800,
            height=400,
            title='Avg Fee per User'
        ),
        use_container_width=True
    )
         
    with b:
         
        st.altair_chart(
        alt.Chart(df).mark_bar(color='turquoise').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('7d-MA # Tx', stack=None, title='7d-MA # Tx')
        ).properties(
            width=800,
            height=400,
            title='7d-MA # Tx'
        ),
        use_container_width=True
    )
        st.altair_chart(
            alt.Chart(df).mark_bar(color='darkorange').encode(
                x=alt.X('DATE:T', title='DATE'),
                y=alt.Y('# Users', stack=None, title='# Users')
            ).properties(
                width=800,
                height=400,
                title='# Users'
            ),
            use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df).mark_bar(color='dodgerblue').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('7d-MA # Users', stack=None, title='7d-MA # Users')
        ).properties(
            width=800,
            height=400,
            title='7d-MA # Users'
        ),
        use_container_width=True
    )
        
       
    generate_summary_p(df.tail(90))

    st.markdown("##")

    st.data_editor(pd.read_csv("nodit_graphql/dex/Aptos DEXs - Time based Cohort Wide.csv"))


    st.markdown("##")

    df = pd.read_csv("nodit_graphql/dex/Volume Ratio.csv")

    df['Date'] = pd.to_datetime(df['Date'])

    


    a,b = st.columns([2,2])
    with a:
         st.altair_chart(
        alt.Chart(df).mark_line(color='deeppink').encode(
            x=alt.X('Date:T', title='DATE'),
            y=alt.Y('Daily volume:Q', stack=None, title='Daily volume')
        ).properties(
            width=800,
            height=400,
            title = 'Daily volume'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_line(color='firebrick').encode(
            x=alt.X('Date:T', title='DATE'),
            y=alt.Y('Avg Vol per User:Q', stack=None, title='Avg Vol per User')
        ).properties(
            width=800,
            height=400,
            title='Avg Vol per User'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_line(color='antiquewhite').encode(
            x=alt.X('Date:T', title='DATE'),
            y=alt.Y('Total users', stack=None, title='Total users')
        ).properties(
            width=800,
            height=400,
            title='Total users'
        ),
        use_container_width=True
    )
         
    with b:
         
        st.altair_chart(
        alt.Chart(df).mark_line(color='turquoise').encode(
            x=alt.X('Date:T', title='DATE'),
            y=alt.Y('volume/Fee ratio', stack=None, title='volume/Fee ratio')
        ).properties(
            width=800,
            height=400,
            title='volume/Fee ratio'
        ),
        use_container_width=True
    )
        st.altair_chart(
            alt.Chart(df).mark_line(color='darkorange').encode(
                x=alt.X('Date:T', title='DATE'),
                y=alt.Y('Avg Vol per Txs', stack=None, title='Avg Vol per Txs')
            ).properties(
                width=800,
                height=400,
                title='Avg Vol per Txs'
            ),
            use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df).mark_line(color='dodgerblue').encode(
            x=alt.X('Date:T', title='DATE'),
            y=alt.Y('Avg Fee/Txs', stack=None, title='Avg Fee/Txs')
        ).properties(
            width=800,
            height=400,
            title='Avg Fee/Txs'
        ),
        use_container_width=True
    )
        
    generate_summary_p(df)

    st.markdown("##")

    a,b = st.columns([2,2])

    with a:
        st.subheader("Whales")
        st.data_editor(pd.read_csv('nodit_graphql/dex/Aptos Whales Per Platform.csv'),width=800)
    with b:
        st.subheader("Dexs Totals")
        st.data_editor(pd.read_csv('nodit_graphql/dex/In total by dexes.csv'), width=800)


    st.markdown("##")

    df = pd.read_csv("nodit_graphql/dex/New Users' Engagement.csv")
    st.subheader("Engagements")

    st.data_editor(df,width=1200)


