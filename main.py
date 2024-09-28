import streamlit as st
from graph import graph
from home import home


# Set page configuration
st.set_page_config(page_title="Aptoslytics", page_icon="🚛", layout="wide")

# Increase font size for better readability
st.markdown("""
<style>
body {
    font-size: 60px;
}
</style>
""", unsafe_allow_html=True)

# Custom CSS to smooth edges of the image and update title color
st.markdown(
    """
    <style>
    .smooth-img {
        border-radius: 50%;
    }
    .golden-title {
        font-family: cursive; 
        color: white; 
        font-size: 70px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 3])

with col1:
    # Apply the smooth-img class for rounded corners
    st.markdown('<img src="https://media1.tenor.com/m/XdmiCYqzZIMAAAAC/aptos-aptoslabs.gif" width="250" class="smooth-img">', unsafe_allow_html=True)

with col2:
    # Apply the golden-title class for golden text
    new_title = '<p class="golden-title">APTOSLYTICS</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    section = st.radio("Navigate to", ["Home", "Platforms", "ETH_Stake", "Fees", "Growth", "Holders", "Explore"], horizontal=True)


if section == 'Home':
    home()
elif section == 'Explore':
    graph()
