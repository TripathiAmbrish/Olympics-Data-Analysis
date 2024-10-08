import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import  matplotlib.pyplot as plt
import seaborn as sbn
import plotly.figure_factory as pff

ae_df = pd.read_csv('athlete_events.csv')
reg_df = pd.read_csv('noc_regions.csv')

ae_df = preprocessor.preprocess(ae_df, reg_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://img.freepik.com/premium-photo/five-interlocking-olympic-rings-white-background-generative-ai_437323-8460.jpg?w=900', use_column_width = True)
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise analysis', 'Athlete wise analysis')
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
    fig = px.line(no_of_events, x='Edition', y='No of Events')
    st.title('No. of events over the years')
    st.plotly_chart(fig)

    no_of_athletes = helper.no_of_athletes_over_time(ae_df)
    fig = px.line(no_of_athletes, x='Edition', y='No of Athletes')
    st.title('No. of Athletes over the years')
    st.plotly_chart(fig)

    st.title("No. of Events over time (each sport)")
    fig,ax = plt.subplots(figsize = [20, 20])
    heat_m = ae_df.drop_duplicates(['Year', 'Sport', 'Event'])
    sbn.heatmap(heat_m.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)

    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = ae_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a sport', sport_list)
    x = helper.most_successful(ae_df, selected_sport)
    st.table(x)


if user_menu == 'Country-wise analysis':

    st.sidebar.title('Country wise analysis')

    
    country_lst = ae_df['region'].dropna().unique().tolist()
    country_lst.sort()
    selected_country = st.sidebar.selectbox('Select a country', country_lst)
    country_df = helper.yearwise_medal_tally(ae_df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medals over the years')
    
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")

    pt = helper.country_event_heatmap(ae_df, selected_country)

    if pt.empty:
        st.write(f"No data available for {selected_country} in the selected period.")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sbn.heatmap(pt, annot=True)
        st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(ae_df,selected_country)
    st.table(top10_df)

    years = ae_df['Year'].dropna().unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    selected_year = st.sidebar.selectbox("Select Year", years)


    country_lst = ae_df['region'].dropna().unique().tolist()
    country_lst.sort()
    selected_cntry = st.sidebar.selectbox('Select a country', country_lst)
# Fetch medal tally based on the selected filters
    medal_tally = helper.fetch_medal_tally(ae_df, selected_year, selected_cntry)

# Define title based on user selection
    if selected_year == 'Overall' and selected_cntry == 'Overall':
        st.title("Overall Medal Tally")
    elif selected_year != 'Overall' and selected_cntry == 'Overall':
        st.title("Medal Tally in " + str(selected_year))
    elif selected_year == 'Overall' and selected_cntry != 'Overall':
        st.title(selected_cntry + "'s Overall Medal Tally")
    else:
        st.title(selected_cntry + "'s Medal Tally in " + str(selected_year))

# Display table of medal tally
    st.table(medal_tally)

# Fetch map data for the visualization
    map_data = helper.prepare_map_data(medal_tally, selected_year, selected_cntry)

# Custom color scale for the map
    custom_color_scale = [
        (0.0, "rgb(77, 0, 38)"),
        (0.2, "rgb(128, 0, 38)"),
        (0.3, "rgb(189, 0, 38)"),
        (0.4, "rgb(227, 26, 28)"),
        (0.5, "rgb(252, 78, 42)"),
        (0.6, "rgb(253, 141, 60)"),
        (0.7, "rgb(254, 178, 76)"),
        (0.8, "rgb(254, 217, 118)"),
        (0.9, "rgb(255, 237, 160)"),
        (1.0, "rgb(255, 255, 204)")
    ]

# Create the geopolitical map with Plotly
    fig = px.choropleth(map_data,
                    locations="NOC",  # Assuming NOC is the country code column
                    color="total",    # Visualizing the total medal count
                    hover_name="Country",
                    hover_data=["Gold", "Silver", "Bronze", "total"],
                    color_continuous_scale=custom_color_scale,
                    projection="natural earth",
                    title=f"Medal Distribution in {selected_year if selected_year != 'Overall' else 'All Years'}"
    )

# Plot the map in Streamlit
    st.plotly_chart(fig)


if user_menu == 'Athlete wise analysis':

    st.sidebar.title('Athlete wise analysis')

    st.title('Distribution of Age')
    athlete_df = ae_df.drop_duplicates(subset= ['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = pff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'].notna()]['Age'].dropna())
        name.append(sport)

    fig = pff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age wrt Sports")
    st.plotly_chart(fig)

    #medal_lst = ae_df['Medal'].dropna().unique().tolist()
    #medal_lst.sort()
    #medal_country = st.sidebar.selectbox('Select a country', medal_lst)

    st.title('Weigh vs Height Distribution')
    sport_list = ae_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a sport', sport_list)
    temp_df = helper.weight_v_height(ae_df, selected_sport)
    fig, ax = plt.subplots()
    ax = sbn.scatterplot(x = 'Weight', y = 'Height', data = temp_df, hue = 'Medal', style = 'Sex', s = 100)    
    st.plotly_chart(fig)

    st.title('Male vs Fenale participation over the years')
    m_f = helper.male_v_female_partcipation(ae_df)
    fig = px.line(m_f, x = 'Year', y = ['Male', 'Female'])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)

