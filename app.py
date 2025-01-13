import streamlit as st
import pandas as pd
import numpy as np
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

# Load Lottie animation from the JSON file
def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Load Lottie animation
torch_animation = load_lottie_animation("Animation - 1736265544981.json")
logo_animation = load_lottie_animation("Animation - 1736351628223.json")

st.markdown("""
    <style>
    .main-header {
        background-color: #1e3a8a;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    .main-header h1 {
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1>🏆 Olympics Data Analysis</h1>
        <p>Uncover insights and trends from the Olympics history</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.title('Olympics Analysis 🏅')
with st.sidebar:  # Use the sidebar context
    st_lottie(logo_animation, height=200, key="sidebar-animation")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('🏅 Medal Tally','📊 Overall Analysis','🌍 Country-wise Analysis','🏋️ Athlete wise Analysis')
)

# Header with Lottie animation
st_lottie(torch_animation, height=200, key="torch")

if user_menu == '🏅 Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)

    # Add a Data Download Option
    csv = medal_tally.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Medal Tally as CSV",
        data=csv,
        file_name='medal_tally.csv',
        mime='text/csv',
    )

if user_menu == '📊 Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    st.markdown("---")

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations Over the Year')
    st.plotly_chart(fig)
    st.markdown("---")

    athlete_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name')
    st.title('Athletes Over the Year')
    st.plotly_chart(fig)
    st.markdown("---")

    st.title('Trends in Sports Popularity Over Time')
    sports_popularity = helper.sports_popularity(df)

    # Plotting trends for selected sports using Plotly
    fig = px.line(
        sports_popularity,x='Year',
        y='Number of Athletes',
        color='Sport',
        labels={
            'Year': 'Year',
            'Number of Athletes': 'Number of Athletes',
            'Sport': 'Sport',
        }
    )

    # Adjust layout for better readability
    fig.update_layout(xaxis_title="Year", yaxis_title="Number of Athletes",legend_title="Sport",template="plotly_white",width=1100,height=600)
    st.plotly_chart(fig)
    st.markdown("---")

    st.title('Gender Representation Over Time')
    gender_representation = helper.gender_representation(df)

    # Plotting with Plotly
    fig = px.line(
        gender_representation,
        x='Year',
        y='Percentage',
        color='Sex',
        title='Gender Representation in Summer Olympics Over Time',
        labels={
            "Year": "Year",
            "Percentage": "Percentage of Athletes",
            "Sex": "Gender"
        },
        markers=True
    )

    # Customize layout
    fig.update_layout(xaxis_title="Year",yaxis_title="Percentage",legend_title="Gender",template="plotly_white",title_x=0.5)
    st.plotly_chart(fig)
    st.markdown("---")

    st.title('Evolution of Events and Sports in Summer Olympics')
    events_sports_trend = helper.events_sports_trend(df)

    # Create the Plotly figure
    fig = go.Figure()

    # Add line for Number of Sports
    fig.add_trace(go.Scatter(
        x=events_sports_trend['Year'],
        y=events_sports_trend['Number of Sports'],
        mode='lines+markers',
        name='Sports',
        line=dict(color='blue'),
        marker=dict(size=6)
    ))

    # Add line for Number of Events
    fig.add_trace(go.Scatter(
        x=events_sports_trend['Year'],
        y=events_sports_trend['Number of Events'],
        mode='lines+markers',
        name='Events',
        line=dict(color='green'),
        marker=dict(size=6)
    ))

    # Customize the layout
    fig.update_layout(xaxis_title="Year",yaxis_title="Count",template="plotly_white",legend_title="Category")
    st.plotly_chart(fig)
    st.markdown("---")

    st.title('Top 10 Countries by Total Medals')
    country_medals = helper.top_10_countries_by_medals(df)

    # Plotting
    fig = px.bar(
        country_medals,
        x='region',
        y='Total',
        labels={'region': 'Country', 'Total': 'Total Medals'},
        text='Total',
        color='Total',
        color_continuous_scale='viridis',
    )
    st.plotly_chart(fig)
    st.markdown("---")

    st.title('No. of Events over time(Every Sport)')
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)
    st.markdown("---")

    st.title('Most Frequent Hosts of Summer Olympics')
    host_cities = helper.host_cities(df)
    st.table(host_cities)
    # Add a Data Download Option
    csv = host_cities.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Most Frequent Hosts of Summer Olympics as CSV",
        data=csv,
        file_name='host_cities.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Youngest Medalists')
    x, y = helper.youngest_medalist_and_oldest_medalist(df)
    st.table(x)
    # Add a Data Download Option
    csv = x.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Youngest Medalists as CSV",
        data=csv,
        file_name='Youngest_medalist.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Oldest Medalists')
    st.table(y)
    # Add a Data Download Option
    csv = y.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Oldest Medalists as CSV",
        data=csv,
        file_name='oldest_medalist.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

    # Add a Data Download Option
    csv = x.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Most Successful Athletes as CSV",
        data=csv,
        file_name='most_successful_athletes.csv',
        mime='text/csv',
    )

if user_menu == '🌍 Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medal Tally Over the Years')
    st.plotly_chart(fig)
    st.markdown("---")

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    # Check if the pivot table is empty
    if pt.empty:
        st.warning(f"No medal data available for {selected_country}")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)
    st.markdown("---")

    st.title('Top 10 Athletes of ' + selected_country )
    top10df = helper.most_sucssfull_country_wise(df,selected_country)
    st.table(top10df)

    # Add a Data Download Option
    csv = top10df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Top 10 Athletes of "+ selected_country +" as CSV",
        data=csv,
        file_name='top_10athletes.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Countries Winning Medals Across the Most Sports')
    sports_medal_tally = helper.countries_winning_medals(df)
    st.table(sports_medal_tally)

    # Add a Data Download Option
    csv = sports_medal_tally.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Countries Winning Medals Across the Most Sports as CSV",
        data=csv,
        file_name='countries_winning_most_medals_across_most_sports.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Top Performing Countries by Decade')
    top_countries_per_decade = helper.decade_performance(df)
    st.table(top_countries_per_decade)

    # Add a Data Download Option
    csv = top_countries_per_decade.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Top Performing Countries by Decade as CSV",
        data=csv,
        file_name='top_performing_countries_by_decade.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Countries With Most Gold Medals in a Single Olympics')
    gold_medals_single_year = helper.gold_medals_single_year(df)
    st.table(gold_medals_single_year)

    # Add a Data Download Option
    csv = top_countries_per_decade.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Countries With Most Gold Medals in a Single Olympics as CSV",
        data=csv,
        file_name='most_gold_medals_in_single_olympics.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Countries With Most Silver Medals in a Single Olympics')
    silver_medals_single_year = helper.silver_medals_single_year(df)
    st.table(silver_medals_single_year)

    # Add a Data Download Option
    csv = top_countries_per_decade.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Countries With Most Silver Medals in a Single Olympics as CSV",
        data=csv,
        file_name='most_silver_medals_in_single_olympics.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Countries With Most Bronze Medals in a Single Olympics')
    bronze_medals_single_year = helper.bronze_medals_single_year(df)
    st.table(bronze_medals_single_year)

    # Add a Data Download Option
    csv = top_countries_per_decade.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Countries With Most Bronze Medals in a Single Olympics as CSV",
        data=csv,
        file_name='most_bronze_medals_in_single_olympics.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Countries With No Medals Despite High Participation')
    no_medals = helper.no_medals_despite_high_participation(df)
    st.table(no_medals)

    # Add a Data Download Option
    csv = no_medals.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Countries With No Medals Despite High Participation as CSV",
        data=csv,
        file_name='no_medals.csv',
        mime='text/csv',
    )

if user_menu == '🏋️ Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600, xaxis_title='Age')
    st.title('Distribution of Age')
    st.plotly_chart(fig)
    st.markdown("---")

    x=[]
    name=[]

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
                     'Cricket', 'Ice Hockey', 'Racquets', 'Motorboating', 'Croquet',
                     'Figure Skating', 'Jeu De Paume', 'Roque', 'Basque Pelota',
                     'Alpinism', 'Aeronautics']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_medalists_age = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        # Check if there are at least 2 unique ages and standard deviation is greater than 0:
        if len(np.unique(gold_medalists_age)) >= 2 and np.std(gold_medalists_age) > 0:
            x.append(gold_medalists_age)
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600, xaxis_title='Age')
    st.title('Distribution of Age wrt sports(Gold Medalist)')
    st.plotly_chart(fig)
    st.markdown("---")

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        silver_medalists_age = temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna()
        # Check if there are at least 2 unique ages and standard deviation is greater than 0:
        if len(np.unique(silver_medalists_age)) >= 2 and np.std(silver_medalists_age) > 0:
            x.append(silver_medalists_age)
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600, xaxis_title='Age')
    st.title('Distribution of Age wrt sports(Silver Medalist)')
    st.plotly_chart(fig)
    st.markdown("---")

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        bronze_medalists_age = temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna()
        # Check if there are at least 2 unique ages and standard deviation is greater than 0:
        if len(np.unique(bronze_medalists_age)) >= 2 and np.std(bronze_medalists_age) > 0:
            x.append(bronze_medalists_age)
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600, xaxis_title='Age')
    st.title('Distribution of Age wrt sports(Bronze Medalist)')
    st.plotly_chart(fig)
    st.markdown("---")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)
    st.markdown("---")

    st.title('Men Vs Women Participation Over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male','Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    st.markdown("---")

    st.title('Analysis of Most Consistent Athletes')
    consistent_athletes = helper.most_consistent_athletes(df)
    st.table(consistent_athletes)

    # Add a Data Download Option
    csv = consistent_athletes.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Analysis of Most Consistent Athletes as CSV",
        data=csv,
        file_name='consistent_athletes.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Medal Conversion Rate')
    medal_conversion = helper.medal_conversion(df)
    st.table(medal_conversion)

    # Add a Data Download Option
    csv = medal_conversion.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Medal Conversion Rate as CSV",
        data=csv,
        file_name='medal_conversion.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Most Versatile Athletes')
    versatile_athletes = helper.most_versatile_athletes(df)
    st.table(versatile_athletes)

    # Add a Data Download Option
    csv = versatile_athletes.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Most Versatile Athletes as CSV",
        data=csv,
        file_name='versatile_athletes.csv',
        mime='text/csv',
    )
    st.markdown("---")

    st.title('Medal Winners by Age Groups')
    medals_by_age_group = helper.medals_by_age_group(df)
    st.table(medals_by_age_group)

    # Add a Data Download Option
    csv = medals_by_age_group.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Medal Winners by Age Groups as CSV",
        data=csv,
        file_name='medals_by_age_group.csv',
        mime='text/csv',
    )