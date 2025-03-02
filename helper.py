import numpy as np
import pandas as pd

def fetch_medal_tally(ae_df, year, country):
    flag = 0
    medal_df = ae_df.drop_duplicates(subset=['Team', 'region', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                     ascending=False)
    else:
        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                       ascending=False)

        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                       ascending=False)
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

def medal_tally(ae_df):
    # Drop duplicates and group by region, then sum up the medals
    medal_tally = ae_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year',
                                                'City', 'Sport', 'Event', 'Medal'])

    # Group by region and sum medal counts
    medal_tally = medal_tally.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']]

    # Compute the total medal count
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    # Ensure columns are of integer type
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    # Sort by Gold, then Silver, then Bronze medals in descending order
    medal_tally = medal_tally.sort_values(by=['Gold', 'Silver', 'Bronze'], ascending=False)

    return medal_tally

def year_country_list(ae_df):
    years = ae_df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(ae_df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def participating_nations_over_time(ae_df):
    nations_over_time = ae_df.drop_duplicates(['Year', 'region'])
    nations_over_time = nations_over_time['Year'].value_counts().reset_index()
    nations_over_time.columns = ['Edition', 'No of Countries']
    nations_over_time = nations_over_time.sort_values('Edition')

    return nations_over_time

def no_of_events_over_time(ae_df):
    no_of_events = ae_df.drop_duplicates(['Year', 'Event'])
    no_of_events = no_of_events['Year'].value_counts().reset_index()
    no_of_events.columns = ['Edition', 'No of Events']
    no_of_events = no_of_events.sort_values('Edition')

    return no_of_events

def no_of_athletes_over_time(ae_df):
    no_of_athletes = ae_df.drop_duplicates(['Year', 'Name'])
    no_of_athletes = no_of_athletes['Year'].value_counts().reset_index()
    no_of_athletes.columns = ['Edition', 'No of Athletes']
    no_of_athletes = no_of_athletes.sort_values('Edition')

    return no_of_athletes


def most_successful(ae_df, sport):
    temp_df = ae_df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    medal_count = temp_df['Name'].value_counts().reset_index()
    medal_count.columns = ['Name', 'Medals']

    x = medal_count.head(20).merge(ae_df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Medals', 'Sport', 'region']
    ].drop_duplicates()

    return x


def yearwise_medal_tally(ae_df, country):
    temp_df = ae_df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(ae_df,country):
    temp_df = ae_df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(ae_df, country):
    temp_df = ae_df.dropna(subset=['Medal'])
    
    temp_df = temp_df[temp_df['region'] == country]

    medal_count = temp_df['Name'].value_counts().reset_index()
    medal_count.columns = ['Name', 'Medals']

    x = medal_count.head(20).merge(ae_df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Medals', 'Sport']
    ].drop_duplicates()

    return x

def weight_v_height(ae_df, sport):
    athlete_df = ae_df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    
def male_v_female_partcipation(ae_df):
    athlete_df = ae_df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    m_f = men.merge(women, on = 'Year', how = 'left')
    m_f.rename(columns = {'Name_x':'Male', 'Name_y':'Female'}, inplace = True)
    m_f.fillna(0, inplace=True)

    return m_f

