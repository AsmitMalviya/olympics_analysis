import numpy as np
import pandas as pd
import openai

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition', 'count':col}, inplace=True)
    return nations_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','City','Year','Sport','Event','Medal'],inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_sucssfull_country_wise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final

def sports_popularity(df):
    # Popularity of sports over time
    sports_popularity = df.groupby(['Year', 'Sport'])['ID'].nunique().reset_index()
    sports_popularity.rename(columns={'ID': 'Number of Athletes'}, inplace=True)
    return sports_popularity

def gender_representation(df):
    # Gender representation
    gender_representation = df.groupby(['Year', 'Sex'])['ID'].nunique().reset_index()
    gender_representation.rename(columns={'ID': 'Number of Athletes'}, inplace=True)

    # Calculate percentages
    total_athletes_per_year = gender_representation.groupby('Year')['Number of Athletes'].sum().reset_index()
    gender_representation = gender_representation.merge(total_athletes_per_year, on='Year', suffixes=('', '_total'))
    gender_representation['Percentage'] = (gender_representation['Number of Athletes'] / gender_representation['Number of Athletes_total']) * 100

    return gender_representation

def events_sports_trend(df):
    # Evolution of events and sports
    events_sports_trend = df.groupby('Year')[['Sport', 'Event']].nunique().reset_index()
    events_sports_trend.rename(columns={'Sport': 'Number of Sports', 'Event': 'Number of Events'}, inplace=True)

    return events_sports_trend

def top_10_countries_by_medals(df):
    # Total medals by country
    temp = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    country_medals = temp.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    country_medals['Total'] = country_medals[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    country_medals = country_medals.sort_values(by='Total', ascending=False).head(10)

    return country_medals

def host_cities(df):
    # Most frequent hosts
    host_cities = df.groupby('City')['Year'].nunique().reset_index()
    host_cities.rename(columns={'Year': 'Number of Times Hosted'}, inplace=True)
    host_cities = host_cities.sort_values(by='Number of Times Hosted', ascending=False).head(10)

    return host_cities

def youngest_medalist_and_oldest_medalist(df):
    # Youngest and oldest medalists
    medalist = df[df['Medal'].notna()]
    youngest_medalist = medalist.loc[medalist['Age'].idxmin()]
    oldest_medalist = medalist.loc[medalist['Age'].idxmax()]
    youngest_medalist = youngest_medalist[['Name', 'Age', 'Sport', 'Year', 'Medal']]
    oldest_medalist = oldest_medalist[['Name', 'Age', 'Sport', 'Year', 'Medal']]

    return youngest_medalist, oldest_medalist

def countries_winning_medals(df):
    temp = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    sports_medal_tally = temp[temp['Medal'].notna()].groupby('region')['Sport'].nunique().reset_index()
    sports_medal_tally.rename(columns={'Sport': 'Unique Sports'}, inplace=True)
    sports_medal_tally = sports_medal_tally.sort_values(by='Unique Sports', ascending=False).head(10)

    return sports_medal_tally

def decade_performance(df):
    # Top Performing Countries by Decade
    # Add a decade column
    df['Decade'] = (df['Year'] // 10) * 10

    # Top-Performing Countries by decade
    temp = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    decade_performance = temp[temp['Medal'].notna()].groupby(['Decade', 'region'])[['Gold', 'Silver', 'Bronze']].sum()
    decade_performance['Total Medals'] = decade_performance.sum(axis=1)
    decade_performance = decade_performance.sort_values(['Decade', 'Total Medals'],ascending=[True, False]).reset_index()
    top_countries_per_decade = decade_performance.groupby('Decade').head(1)

    return top_countries_per_decade

def gold_medals_single_year(df):
    temp = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    gold_medals_single_year = temp.groupby(['Year', 'region'])['Gold'].sum().reset_index()
    gold_medals_single_year = gold_medals_single_year.sort_values(by='Gold', ascending=False).head(10)

    return gold_medals_single_year


def silver_medals_single_year(df):
    # Most silver medals in a single Olympics
    temp = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    silver_medals_single_year = temp.groupby(['Year', 'region'])['Silver'].sum().reset_index()
    silver_medals_single_year = silver_medals_single_year.sort_values(by='Silver', ascending=False).head(10)

    return silver_medals_single_year


def bronze_medals_single_year(df):
    # Most bronze medals in a single Olympics
    temp = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    bronze_medals_single_year = temp.groupby(['Year', 'region'])['Bronze'].sum().reset_index()
    bronze_medals_single_year = bronze_medals_single_year.sort_values(by='Bronze', ascending=False).head(10)

    return bronze_medals_single_year

def no_medals_despite_high_participation(df):
    # Countries with high participation but no medals
    temp = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    participation = temp.groupby('region')['ID'].nunique().reset_index()
    participation.rename(columns={'ID': 'Total Participants'}, inplace=True)

    medals = df[df['Medal'].notna()].groupby('region')['Medal'].count().reset_index()
    medals.rename(columns={'Medal': 'Total Medals'}, inplace=True)

    # Merge participation and medals
    country_performance = participation.merge(medals, on='region', how='left')
    country_performance['Total Medals'] = country_performance['Total Medals'].fillna(0)
    no_medals = country_performance[country_performance['Total Medals'] == 0]
    no_medals = no_medals.sort_values(by='Total Participants', ascending=False).head(10)

    return no_medals

def most_consistent_athletes(df):
    # Most consistent athletes
    consistent_athletes = df.groupby('Name')['Year'].nunique().reset_index()
    consistent_athletes.rename(columns={'Year': 'Olympics Editions'}, inplace=True)
    consistent_athletes = consistent_athletes.sort_values(by='Olympics Editions', ascending=False).head(10)

    return consistent_athletes

def medal_conversion(df):
    # Medal conversion rate
    medal_conversion = df.groupby('Name')[['Gold', 'Silver', 'Bronze']].sum()
    medal_conversion['Total Medals'] = medal_conversion.sum(axis=1)
    medal_conversion['Total Events'] = df.groupby('Name')['Event'].count()
    medal_conversion['Conversion Rate'] = medal_conversion['Total Medals'] / medal_conversion['Total Events']

    # Sort by conversion rate
    medal_conversion = medal_conversion.sort_values(by='Conversion Rate', ascending=False)
    medal_conversion = medal_conversion[['Total Medals', 'Total Events', 'Conversion Rate']].head(10)

    return medal_conversion

def most_versatile_athletes(df):
    # Most versatile athletes
    versatile_athletes = df.groupby('Name')['Sport'].nunique().reset_index()
    versatile_athletes.rename(columns={'Sport': 'Unique Sports'}, inplace=True)
    versatile_athletes = versatile_athletes.sort_values(by='Unique Sports', ascending=False).head(10)

    return versatile_athletes

def medals_by_age_group(df):
    # Medal winners by age groups
    df['Age Group'] = pd.cut(df['Age'], bins=[0, 20, 30, 40, 50, 100], labels=['<20', '20-30', '30-40', '40-50', '>50'])

    # Count medals by age group
    medals_by_age_group = df[df['Medal'].notna()].groupby('Age Group')[['Gold', 'Silver', 'Bronze']].sum()
    medals_by_age_group['Total Medal'] = medals_by_age_group.sum(axis=1)

    return medals_by_age_group
