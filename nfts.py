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



    

def nfts():


    st.markdown("##")
    df = pd.read_csv("nodit_graphql/nfts/Daily Sales Number.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Volume (USD):Q', stack=None, title='Volume (USD)')
        ).properties(
            width=800,
            height=400,
            title = 'Volume (USD)'
        ),
        use_container_width=True
    )
    


    a,b = st.columns([2,2])
    with a:
         st.altair_chart(
        alt.Chart(df).mark_bar(color='deeppink').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Transactions:Q', stack=None, title='Transactions')
        ).properties(
            width=800,
            height=400,
            title = 'Transactions'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_bar(color='bisque').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Cumulative Transactions:Q', stack=None, title='Transactions')
        ).properties(
            width=800,
            height=400,
            title='Cumulative Transactions'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_bar(color='darkkhaki').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Collections:Q', stack=None, title='Collections')
        ).properties(
            width=800,
            height=400,
            title='Collections'
        ),
        use_container_width=True
    )
         st.altair_chart(
        alt.Chart(df).mark_bar(color='firebrick').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Buyers:Q', stack=None, title='Buyers')
        ).properties(
            width=800,
            height=400,
            title='Buyers'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_bar(color='antiquewhite').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Max Price (APT):Q', stack=None, title='Max Price (APT)')
        ).properties(
            width=800,
            height=400,
            title='Max Price (APT)'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_bar(color='turquoise').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('AVG_14_DAY_MOVING', stack=None, title='AVG_14_DAY_MOVING')
        ).properties(
            width=800,
            height=400,
            title='AVG_14_DAY_MOVING'
        ),
        use_container_width=True
    )
    with b:
        st.altair_chart(
            alt.Chart(df).mark_bar(color='darkorange').encode(
                x=alt.X('DATE:T', title='DATE'),
                y=alt.Y('Sales:Q', stack=None, title='Sales')
            ).properties(
                width=800,
                height=400
            ),
            use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df).mark_bar(color='dodgerblue').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Cumulative Sales:Q', stack=None, title='Cumulative Sales')
        ).properties(
            width=800,
            height=400,
            title='Cumulative Sales'
        ),
        use_container_width=True
    )
        st.altair_chart(
        alt.Chart(df).mark_bar(color='blanchedalmond').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Avg Price (APT):Q', stack=None, title='Avg Price (APT)')
        ).properties(
            width=800,
            height=400,
            title='Avg Price (APT)'
        ),
        use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='cyan').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Sellers:Q', stack=None, title='Sellers')
        ).properties(
            width=800,
            height=400,
            title='Sellers'
        ),
        use_container_width=True
    )

        st.altair_chart(
        alt.Chart(df).mark_bar(color='dimgray').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Min Price (APT):Q', stack=None, title='Min Price (APT)')
        ).properties(
            width=800,
            height=400,
            title='Min Price (APT)'
        ),
        use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='lavender').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('AVG_30_DAY_MOVING', stack=None, title='AVG_30_DAY_MOVING')
        ).properties(
            width=800,
            height=400,
            title='AVG_30_DAY_MOVING'
        ),
        use_container_width=True
    )
    generate_summary_p(df.tail(90))


    st.markdown("##")
    df = pd.read_csv("nodit_graphql/nfts/Daily New Buyers.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_area(color='chocolate').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('New Buyers:Q', stack=None, title='New Buyers')
        ).properties(
            width=800,
            height=400,
            title = 'New Buyers'
        ),
        use_container_width=True
    )


    st.markdown("##")
    st.subheader("Top collections (30D)")
    df= pd.read_csv("nodit_graphql/nfts/Overview of Top Collections (Last 30D).csv")
    st.data_editor(df)

    generate_summary(df)









    st.markdown("##")
    st.subheader("MARKETPLACES")
    df = pd.read_csv("nodit_graphql/nfts/Daily Sales By Marketplaces.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])

    a,b = st.columns([2,2])
    with a:
         st.altair_chart(
        alt.Chart(df).mark_bar(color='deeppink').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Transactions:Q', stack=None, title='Transactions'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title = 'Transactions'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_line(color='bisque').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Cumulative Transactions:Q', stack=None, title='Transactions'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Cumulative Transactions'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_bar(color='darkkhaki').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Collections:Q', stack=None, title='Collections'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Collections'
        ),
        use_container_width=True
    )
         st.altair_chart(
        alt.Chart(df).mark_bar(color='firebrick').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Buyers:Q', stack=None, title='Buyers'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Buyers'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_circle(color='antiquewhite').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Max Price (APT):Q', stack=None, title='Max Price (APT)'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Max Price (APT)'
        ),
        use_container_width=True
    )
         
         st.altair_chart(
        alt.Chart(df).mark_bar(color='turquoise').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('AVG_14_DAY_MOVING', stack=None, title='AVG_14_DAY_MOVING'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='AVG_14_DAY_MOVING'
        ),
        use_container_width=True
    )
    with b:
        st.altair_chart(
            alt.Chart(df).mark_bar(color='darkorange').encode(
                x=alt.X('DATE:T', title='DATE'),
                y=alt.Y('Sales:Q', stack=None, title='Sales'),
                color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
            ).properties(
                width=800,
                height=400
            ),
            use_container_width=True
        )

        st.altair_chart(
        alt.Chart(df).mark_line(color='dodgerblue').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Cumulative Sales:Q', stack=None, title='Cumulative Sales'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Cumulative Sales'
        ),
        use_container_width=True
    )
        st.altair_chart(
        alt.Chart(df).mark_bar(color='blanchedalmond').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Avg Price (APT):Q', stack=None, title='Avg Price (APT)'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Avg Price (APT)'
        ),
        use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='cyan').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Sellers:Q', stack=None, title='Sellers'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Sellers'
        ),
        use_container_width=True
    )

        st.altair_chart(
        alt.Chart(df).mark_circle(color='dimgray').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('Min Price (APT):Q', stack=None, title='Min Price (APT)'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Min Price (APT)'
        ),
        use_container_width=True
    )
        
        st.altair_chart(
        alt.Chart(df).mark_bar(color='lavender').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('AVG_30_DAY_MOVING', stack=None, title='AVG_30_DAY_MOVING'),
            color=alt.Color('PLATFORM_NAME:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='AVG_30_DAY_MOVING'
        ),
        use_container_width=True
    )
    generate_summary_p(df.tail(90))