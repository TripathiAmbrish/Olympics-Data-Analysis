import streamlit as st
import pandas as pds

st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country wise analysis', 'Athlete wise analysis')
)