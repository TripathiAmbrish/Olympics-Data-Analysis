import numpy as np

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
