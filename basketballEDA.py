import streamlit as st
import pandas as pd 
import base64
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np 
from PIL import Image
import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


st.title('NBA Player Statistic Explorer')
st.markdown(''' 
This application performs simple webscraping of NBA players stats data!
* **Python libraries used:** base64, pandas, streamlit, seaborn, PIL, BeautifulSoup, re, requests
* **Data Source:** [Baskerball-reference.com](https://www.basketball-reference.com/)
            ''')

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2024))))

################ 
# Web Scraping of NBA player Stats 
################ 

@st.cache_resource
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

columns_to_convert = ['G', 'GS', 'MP', 'FG', 'FGA','FG%', '3P', '3PA', '3P%','2P', '2PA','2P%', 'FT', 'FTA','FT%', 'ORB', 'DRB', 'TRB','eFG%', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
# Use pd.to_numeric to convert the specified columns to float
playerstats[columns_to_convert] = playerstats[columns_to_convert].apply(pd.to_numeric, errors='coerce')
playerstats = playerstats[playerstats['Tm'] != 'TOT']
################ 
# Sidebar - Team selection with an empty default selection and a placeholder
# Initialize selected_team as an empty list
################ 

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

################ 
# Sidebar - Position selection
# Initialize selected_team as an empty list
################ 

selected_pos = ['C','PF','SF','PG','SG']
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, selected_pos)

################ 
# Filtering data
################ 

df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

show_glossary = st.sidebar.checkbox("Show Glossary")

if show_glossary:
    st.markdown('''
        * Rk -- Rank
        * Pos -- Position
        * Age -- Player's age on February 1 of the season
        * Tm -- Team
        * G -- Games
        * GS -- Games Started
        * MP -- Minutes Played Per Game
        * FG -- Field Goals Per Game
        * FGA -- Field Goal Attempts Per Game
        * FG% -- Field Goal Percentage
        * 3P -- 3-Point Field Goals Per Game
        * 3PA -- 3-Point Field Goal Attempts Per Game
        * 3P% -- 3-Point Field Goal Percentage
        * 2P -- 2-Point Field Goals Per Game
        * 2PA -- 2-Point Field Goal Attempts Per Game
        * 2P% -- 2-Point Field Goal Percentage
        * eFG% -- Effective Field Goal Percentage
        This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal.
        * FT -- Free Throws Per Game
        * FTA -- Free Throw Attempts Per Game
        * FT% -- Free Throw Percentage
        * ORB -- Offensive Rebounds Per Game
        * DRB -- Defensive Rebounds Per Game
        * TRB -- Total Rebounds Per Game
        * AST -- Assists Per Game
        * STL -- Steals Per Game
        * BLK -- Blocks Per Game
        * TOV -- Turnovers Per Game
        * PF -- Personal Fouls Per Game
        * PTS -- Points Per Game''')

################ 
# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
################ 

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
  
################ 
# Sidebar - Player filter (multi-select)
################ 

selected_players = st.sidebar.multiselect('Select Player(s)', df_selected_team['Player'].unique())

# Calculate total points scored by players for each team
team_points = df_selected_team.groupby('Tm')['PTS'].sum().reset_index()
# Sort the teams by total points in descending order
team_points = team_points.sort_values(by='PTS', ascending=False)
# Select the top 10 teams
top_10_teams = team_points.head(10)
# Create a Seaborn bar chart
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=top_10_teams, x='Tm', y='PTS', palette='viridis')
plt.xlabel('Team')
plt.ylabel('Total Points Scored in')
plt.title('Top 10 Teams by Total Points Scored in ' + str(selected_year))
# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')
# Display numerical values on the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')    
# Show the plot in Streamlit
st.pyplot(plt)









# Check if a player is selected
if selected_players:  # Assuming you are using selected_players from your previous code
    ################    
    #player profile section
    st.header('Player Profile')
    ################ 
    for selected_player in selected_players:
        # Remove non-alphabet characters from the player's name
        alphanumeric_name = re.sub(r'[^a-zA-Z]', '', selected_player)
        
        # Display the selected player's statistics
        player_data = df_selected_team[df_selected_team['Player'] == selected_player]
        st.subheader(selected_player)
        st.dataframe(player_data)

        # Generate the photo URL based on the player's name
        lowercase_name = selected_player.lower()
        first_name, last_name = lowercase_name.split()
        unique_identifier = last_name[:5] + first_name[:2] + "01"
        player_photo_url = f"https://www.basketball-reference.com/req/202106291/images/headshots/{unique_identifier}.jpg"
        st.image(player_photo_url)
        
        # Scrape player information from their webpage
        player_info_url = f"https://www.basketball-reference.com/players/{last_name[0].lower()}/{last_name[:5]}{first_name[:2]}01.html"
        player_info_response = requests.get(player_info_url)
        player_info_soup = BeautifulSoup(player_info_response.content, 'html.parser')

        

if selected_players:
    st.subheader('Player Stats for Selected Player(s)')
    df_selected_players = df_selected_team[df_selected_team['Player'].isin(selected_players)]   
    st.dataframe(df_selected_players)  
    if st.checkbox('Show Charts'):
        
        
        ################ 
        # Convert object type to numeric 
        ################ 
        columns_to_convert = ['G', 'GS', 'MP', 'FG', 'FGA','FG%', '3P', '3PA', '3P%','2P', '2PA','2P%', 'FT', 'FTA','FT%', 'ORB', 'DRB', 'TRB','eFG%', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

        # Use pd.to_numeric to convert the specified columns to float
        df_selected_players[columns_to_convert] = df_selected_players[columns_to_convert].apply(pd.to_numeric, errors='coerce')
        
        # Define the order of players for proper grouping
        order = selected_players
        
        ################################# Player Statistics Chart ################################# 
        data = df_selected_players[df_selected_players["Player"].isin(selected_players)]
        data = data.melt(id_vars=["Player"], value_vars=["3P%", "2P%", "FT%", "FG%", 'eFG%'])
        # Create a bar chart with hues
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=data, x="Player", y="value", hue="variable", order=order)
        plt.xlabel(" ")
        plt.ylabel("Performance Metrics")
        plt.title("Player Offence Statistics Comparison")
        plt.xticks(rotation=0, ha="center")
        # Display numerical values on the bars
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')  
        # Show the plot in Streamlit
        st.pyplot(plt)
        
        ################################# Player Defensive Charts #################################
        data = df_selected_players[df_selected_players["Player"].isin(selected_players)]
        data = data.melt(id_vars=["Player"], value_vars=['ORB', 'DRB', 'STL', 'BLK', 'PF'])
        # Create a bar chart with hues
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=data, x="Player", y="value", hue="variable", order=order)
        plt.xlabel(" ")
        plt.ylabel("Performance Metrics")
        plt.title("Player Defence Statistics Comparison")
        plt.xticks(rotation=0, ha="center")
        # Display numerical values on the bars
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')    
        # Show the plot in Streamlit
        st.pyplot(plt)          
else: 
    st.markdown('Select players from the sidebar')
