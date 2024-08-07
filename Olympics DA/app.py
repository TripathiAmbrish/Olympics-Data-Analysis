import streamlit as st
import pandas as pd
import preprocessor
import helper

ae_df = pd.read_csv('athlete_events.csv')
reg_df = pd.read_csv('noc_regions.csv')

ae_df = preprocessor.preprocess(ae_df, reg_df)

st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country wise analysis', 'Athlete wise analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.year_country_list(ae_df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(ae_df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s " + "Overall Medal Tally")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s " + "Medal Tally in " + str(selected_year) + " is" )
    st.table(medal_tally)
