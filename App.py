import streamlit as st
import pandas as py

st.sidebar.radio(
    'Select an option',
    ('Home','Overall Analysis', 'Team Analysis', 'Season Analysis')
)