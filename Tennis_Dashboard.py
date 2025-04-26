import pymysql
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="centered")
st.title(":tennis: Tennis World Championship :tennis:")
st.image("Bopanna-Sania.png", caption="Icons of Indian Tennis")

st.markdown("""
<style>
.small-font {
    font-size:20px !important;
            color:cyan;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="small-font">!!<b><u>Tournament dashboard</u></b>!!</p>', unsafe_allow_html=True)

def get_data(query):
    connection = pymysql.connect(
       host = "localhost",
        user = "root",
        password = "",
        database="tennis_db"
    )
    
    data = pd.read_sql_query(query, connection)
    connection.close()
    return data

tournament_data = get_data('SELECT COUNT(DISTINCT category_name) AS Tournament FROM categories')
st.write("No. Tournaments: ", tournament_data['Tournament'].values[0])

comp_played_data = get_data('SELECT count(competition_name) AS competitions_conducted FROM competitions')
st.write("No. Competitons counducted: ", comp_played_data['competitions_conducted'].values[0])

country_data = get_data('SELECT COUNT(distinct country) AS Total_countries_participated FROM competitors')
st.write("No. Countries participated: ", country_data['Total_countries_participated'].values[0])

gender_data = get_data('SELECT competitor_rankings.gender, count(competitors.name) AS comp_count FROM competitor_rankings JOIN competitors on competitors.competitor_id=competitor_rankings.competitor_id group by gender')
st.write("No. Male participants: ", gender_data['comp_count'].values[0])
st.write("No. Female participants: ", gender_data['comp_count'].values[1])

st.markdown("""
<style>
.small-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="small-font">!!<b><u>Toppers</u></b>!!</p>', unsafe_allow_html=True)

fetch_rank_data = get_data('select competitors.name,competitors.country,competitor_rankings.rank,competitor_rankings.points from competitors LEFT JOIN competitor_rankings ON competitors.competitor_id = competitor_rankings.competitor_id where competitor_rankings.rank < 6 order by competitor_rankings.points DESC, competitor_rankings.rank ASC LIMIT 5')
st.dataframe(fetch_rank_data, use_container_width=True)

fetch_category_data = get_data('SELECT category_name FROM `categories` ORDER by category_name ASC')
select_category = st.sidebar.selectbox(
    "Category",
    fetch_category_data['category_name'].values.tolist(),
    index=None
)

if select_category != None:
    category_filter_query = "SELECT categories.category_name, competitions.competition_name AS competition_name, competitions.type, competitions.gender from competitions JOIN categories ON categories.category_id = competitions.category_id WHERE categories.category_name = '" + select_category + "'"
    fetch_category_data_with_filter = get_data(category_filter_query)
    st.write(fetch_category_data_with_filter)

fetch_competitors_data = get_data('SELECT name FROM `competitors` ORDER by name ASC')
select_competitor = st.sidebar.selectbox(
    "Competitors",
    fetch_competitors_data['name'].values.tolist(),
    index=None
)

if select_competitor != None:
    rakings_filter_query = "select competitors.name, competitors.country,competitor_rankings.rank,competitor_rankings.movement, competitor_rankings.points, competitor_rankings.competitions_played from competitor_rankings JOIN competitors ON competitors.competitor_id = competitor_rankings.competitor_id where competitors.name = '" + select_competitor + "'"
    fetch_player_data_with_filter = get_data(rakings_filter_query)
    st.write(fetch_player_data_with_filter)

fetch_country_data = get_data('SELECT country FROM `competitors` GROUP by country ASC')
select_country = st.sidebar.selectbox(
    "Country",
    fetch_country_data['country'].values.tolist(),
    index=None
)

if select_country != None:
    contry_filter_query = "SELECT competitors.country, count(competitors.name) AS Headcount, AVG(competitor_rankings.points) AS Point from competitors JOIN competitor_rankings ON competitors.competitor_id = competitor_rankings.competitor_id where competitors.country = '" + select_country + "' group by country order by country ASC"
    fetch_country_data_with_filter = get_data(contry_filter_query)
    st.write(np.round(fetch_country_data_with_filter,0))

fetch_venue_data = get_data('select city_name from venues group by city_name ORDER by city_name ASC')
select_venue = st.sidebar.selectbox(
    "venues",
   fetch_venue_data['city_name'].values.tolist(),
    index=None
)

if select_venue != None:
    venue_filter_query = "SELECT venue_name, city_name, country_name from venues where city_name = '" + select_venue + "'"
    venue_data_with_filter = get_data(venue_filter_query)
    st.write(venue_data_with_filter)

rank_slider = st.sidebar.slider("Rank range", 0, 501, (0, 0))
if rank_slider[0] != 0 or rank_slider[1] != 0:
    rank_query_filter_with_range = "select competitors.name, competitors.country,competitor_rankings.rank, competitor_rankings.points, competitor_rankings.competitions_played from competitor_rankings JOIN competitors ON competitors.competitor_id = competitor_rankings.competitor_id where competitor_rankings.rank BETWEEN " + str(rank_slider[0]) + " AND " + str(rank_slider[1]) + " order by competitor_rankings.rank ASC"
    fetch_rank_range_data = get_data(rank_query_filter_with_range)
    st.dataframe(fetch_rank_range_data)

points_slider = st.sidebar.slider("Points range", 109, 10665, (109, 109))
if points_slider[0] != 109 or points_slider[1] != 109:
    points_query_filter_with_range = "SELECT competitors.name AS comp_name, competitor_rankings.name,competitor_rankings.year,competitor_rankings.gender,competitor_rankings.points from competitor_rankings JOIN competitors ON competitor_rankings.competitor_id = competitors.competitor_id where competitor_rankings.points BETWEEN " + str(points_slider[0]) + " AND " + str(points_slider[1]) + " ORDER BY competitor_rankings.points DESC"
    fetch_points_range_data = get_data(points_query_filter_with_range)
    st.dataframe(fetch_points_range_data)
