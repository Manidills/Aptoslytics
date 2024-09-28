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


    

def projects():


    st.markdown("##")
    df = pd.read_csv("nodit_graphql/Top_projects/tvl.csv")

    df['csvData__001'] = pd.to_datetime(df['csvData__001'])


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_area().encode(
            x=alt.X('csvData__001:T', title='DATE'),
            y=alt.Y('csvData__002:Q', stack=None, title='TVL')
        ).properties(
            width=800,
            height=400,
            title='TVL'
        ),
        use_container_width=True
    )

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/Top_projects/Weekly Number of Users.csv")

    df['csvData__001'] = pd.to_datetime(df['csvData__001'])

    
    a,b = st.columns([2,2])
    with a:
         st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('csvData__001:T', title='DATE'),
            y=alt.Y('csvData__003:Q', stack=None, title='USERS'),
            color=alt.Color('csvData__002:N', legend=alt.Legend(title='CHAIN'))
        ).properties(
            width=800,
            height=400,
            title='Weekly Users'
        ),
        use_container_width=True
    )
    with b:
        st.altair_chart(
            alt.Chart(df).mark_line().encode(
                x=alt.X('csvData__001:T', title='DATE'),
                y=alt.Y('csvData__004:Q', stack=None, title='TOTAL_TX'),
                color=alt.Color('csvData__002:N', legend=alt.Legend(title='CHAIN'))
            ).properties(
                width=800,
                height=400,
                title='Weekly TXS'
            ),
            use_container_width=True
        )

    generate_summary_p(df)

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/Top_projects/Total Daily Number of New Users (YTD).csv")

    df['date'] = pd.to_datetime(df['date'])


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_area().encode(
            x=alt.X('date:T', title='DATE'),
            y=alt.Y('new users:Q', stack=None, title='New Users')
        ).properties(
            width=800,
            height=400,
            title='New Users'
        ),
        use_container_width=True
    )

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/Top_projects/Top Projects Based on Number of New Users.csv")


    a,b = st.columns([2,2])
    with a:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='blueviolet').encode(
            x=alt.X('PROJECT', title='PROJECT'),
            y=alt.Y('NEW_USERS', stack=None, title='NEW_USERS'),
        ).properties(
            width=800,
            height=400,
            title='New Users Per projects'
        ),
        use_container_width=True
    )
    with b:
        st.altair_chart(
        alt.Chart(df).mark_bar(color='brown').encode(
            x=alt.X('PROJECT', title='PROJECT'),
            y=alt.Y('USERS', stack=None, title='USERS'),
        ).properties(
            width=800,
            height=400,
            title='Users Per Projects'
        ),
        use_container_width=True
    )
        
    generate_summary_p(df)


    st.markdown("##")
    df = pd.read_csv("nodit_graphql/Top_projects/New Vs. Old users per project.csv")


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x=alt.X('PROJECT', title='PROJECT'),
            y=alt.Y('TOTAL_TX', stack=None, title='TOTAL_TX'),
            color=alt.Color('TYPE:N', legend=alt.Legend(title='TYPE'))
        ).properties(
            width=800,
            height=400,
            title='Old vs New'
        ),
        use_container_width=True
    )

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/Top_projects/New Users Breakdown Based on Number of Active Days.csv")
    df_1 = pd.read_csv("nodit_graphql/Top_projects/New Users Breakdown Based on Number of Interacted Projects.csv")


    a,b = st.columns([2,2])
    with a:
        st.subheader("New Users Breakdown Based on Number of Active Days")
        st.data_editor(df, width=700)
    with b:
        st.subheader("New Users Breakdown Based on Number of Interacted Projects")
        st.data_editor(df_1, width=700)

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/Top_projects/Daily Transaction Fees.csv")

    df['DATE'] = pd.to_datetime(df['DATE'])


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_area(color='antiquewhite').encode(
            x=alt.X('DATE:T', title='DATE'),
            y=alt.Y('FEES:Q', stack=None, title='FEES')
        ).properties(
            width=800,
            height=400,
            title='Daily Transaction Fees'
        ),
        use_container_width=True
    )

    st.markdown("##")
    df = pd.read_csv("nodit_graphql/Top_projects/Daily Share of New Users Per project type.csv")
    df['day'] = pd.to_datetime(df['day'])


    # Creating the multi-area graph (stacked area chart)
    st.altair_chart(
        alt.Chart(df).mark_circle().encode(
            x=alt.X('day:T', title='day'),
            y=alt.Y('new', stack=None, title='users'),
            color=alt.Color('type:N', legend=alt.Legend(title='type'))
        ).properties(
            width=800,
            height=400,
            title='Daily Share of New Users Per project type'
        ),
        use_container_width=True
    )

    generate_summary_p(df)


#     st.markdown("##")
#     df = pd.read_csv("nodit_graphql/aptos_vs_rest/Average Success Rate.csv")

#     # Chart title and description
#     st.markdown("## Average Success Rate")
#     st.markdown("##")

#     # Creating the multi-area graph (stacked area chart)
#     st.altair_chart(
#         alt.Chart(df).mark_bar(color='green').encode(
#             x=alt.X('CHAIN', title='CHAIN'),
#             y=alt.Y('TOTAL_TXS', stack=None, title='TOTAL_TXS'),
#             color=alt.Color('STATUS:N', legend=alt.Legend(title='STATUS'))
#         ).properties(
#             width=800,
#             height=400
#         ),
#         use_container_width=True
#     )

#     generate_summary_p(df)

#     st.markdown("##")

#     df = pd.read_csv("nodit_graphql/aptos_vs_rest/Block Time.csv")
#     # Chart title and description
#     st.markdown("## Block Time")
#     st.markdown("##")


#     a,b = st.columns([2,2])
#     with a:
#         st.altair_chart(
#         alt.Chart(df).mark_bar(color='darkorange').encode(
#             x=alt.X('CHAIN', title='CHAIN'),
#             y=alt.Y('Average Time', stack=None, title='Price Changes'),
#         ).properties(
#             width=800,
#             height=400
#         ),
#         use_container_width=True
#     )
#     with b:
#         st.altair_chart(
#         alt.Chart(df).mark_bar(color='honeydew').encode(
#             x=alt.X('TYPE', title='TYPE'),
#             y=alt.Y('Average Time', stack=None, title='Average Time'),
#         ).properties(
#             width=800,
#             height=400
#         ),
#         use_container_width=True
#     )
        
#     generate_summary_p(df)

#     st.markdown("##")

#     df = pd.read_csv("nodit_graphql/aptos_vs_rest/fee.csv")
#     # Chart title and description
#     st.markdown("## Fee")
#     st.markdown("##")



#     st.altair_chart(
#     alt.Chart(df).mark_bar(color='red').encode(
#         x=alt.X('CHAIN', title='CHAIN'),
#         y=alt.Y('AVG_FEE', stack=None, title='AVG_FEE'),
#     ).properties(
#         width=800,
#         height=400
#     ),
#     use_container_width=True
# )

#     generate_summary(df)    





