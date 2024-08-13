import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px

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
        st.title(selected_country + "'s " + "Medal Tally in " + str(selected_year))
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = ae_df['Year'].unique().shape[0] - 1
    cities = ae_df['City'].unique().shape[0]
    sports = ae_df['Sport'].unique().shape[0]
    events = ae_df['Event'].unique().shape[0]
    athletes = ae_df['Name'].unique().shape[0]
    nations = ae_df['region'].unique().shape[0]
    gold = ae_df['Gold'].sum()
    silver = ae_df['Silver'].sum()
    bronze = ae_df['Bronze'].sum()

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Gold")
        st.title(gold)
    with col2:
        st.header("Silver")
        st.title(silver)
    with col3:
        st.header("Bronze")
        st.title(bronze)

    nations_over_time = helper.participating_nations_over_time(ae_df)
    fig = px.line(nations_over_time, x='Edition', y='No of Countries')
    st.title('Participating nations over the years')
    st.plotly_chart(fig)

    no_of_events = helper.no_of_events_over_time(ae_df)
    fig2 = px.line(no_of_events, x='Edition', y='No of Events')
    st.title('No. of events over the years')
    st.plotly_chart(fig2)