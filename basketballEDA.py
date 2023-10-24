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


st.markdown("<h1 style='text-align: center;'>NBA Player Statistic Explorer</h1>", unsafe_allow_html=True)
image = 'https://pngimg.com/uploads/nba/nba_PNG8.png'
st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="{image}" width="200" /></div>',
    unsafe_allow_html=True
)
st.markdown("<h4 style='text-align: center;'>Developed by Raihan Rasheed</h4>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(''' 
Welcome to the NBA Player Statistic Explorer, a powerful tool for basketball enthusiasts and data analysts! This application performs web scraping of NBA player statistics from [Basketball-Reference](https://www.basketball-reference.com/), providing you with a wealth of information on player performance.

### Features:
* Explore NBA player statistics from various seasons.
* Compare player statistics across different years.
* Analyze team performance with various metrics.

### Python Libraries Used:
This application is powered by a set of Python libraries:
* `pandas`: Used for data manipulation and analysis.
* `seaborn` and `matplotlib`: Utilized for data visualization, allowing us to create insightful charts and plots.
* `BeautifulSoup`: Enables us to scrape data from the web.
* `requests`: Used to fetch data from web pages.

### Data Source:
We retrieve NBA player statistics from [Basketball-Reference](https://www.basketball-reference.com/), a reputable source for basketball data. The data includes player performance, team statistics, and much more.

### How to Use:
1. Select the year you want to explore using the dropdown menu.
2. Choose your preferred analysis option from the radio buttons.
3. Enjoy in-depth insights into NBA player and team statistics!

Get ready to dive into the world of NBA data and uncover fascinating insights. Explore player stats, track team performance, and gain a deeper understanding of the game. Let's start analyzing the numbers and discovering the true MVPs of the NBA!
         
            ''')

st.markdown('## Select the year you want to explore')
selected_year = st.selectbox('Year', list(reversed(range(1950,2024))))

if st.checkbox('Show Team Stats of the selected Year'):
    # URL of the webpage
    url = "https://www.basketball-reference.com/leagues/NBA_"+str(selected_year)+".html#all_per_game_team-opponent"
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the table based on the id attribute
    table = soup.find("table", {"id": "totals-team"})
    second_table = soup.find("table", {"id": "per_game-team"})
    
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    df_pg_team = pd.read_html(str(second_table))[0]
    df_pg_team.set_index('Rk', inplace=True)
    df_pg_team = df_pg_team[~df_pg_team['Team'].str.contains('League Average')]
    
    if st.radio("Select a table to display", ("Total Team Stats", "Per Game Team Stats")) == "Total Team Stats":
        st.dataframe(df_team)
    else:
        st.dataframe(df_pg_team)
    st.markdown("Use the checkbox below to explore the explaination of columns")
    if st.checkbox("Show Table Glossary"):
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



################# Web Scraping of NBA player Stats ################ 

def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    columns_to_convert = ['G', 'GS', 'MP', 'FG', 'FGA','FG%', '3P', '3PA', '3P%','2P', '2PA','2P%', 'FT', 'FTA','FT%', 'ORB', 'DRB', 'TRB','eFG%', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    # Use pd.to_numeric to convert the specified columns to float
    playerstats[columns_to_convert] = playerstats[columns_to_convert].apply(pd.to_numeric, errors='coerce')
    playerstats = playerstats[playerstats['Tm'] != 'TOT']
    return playerstats
playerstats = load_data(selected_year)



################ 
# Team selection with an empty default selection and a placeholder
# Initialize selected_team as an empty list
################ 

sorted_unique_team = sorted(playerstats.Tm.unique())
st.markdown("## Select one or more Teams of your choice")
selected_team = st.multiselect('Team', sorted_unique_team, sorted_unique_team)
if st.checkbox("Show Team Name Glossary"):
    st.markdown('''
* Atlanta Hawks - ATL
* Boston Celtics - BOS
* Brooklyn Nets - BKN
* Charlotte Hornets - CHA
* Chicago Bulls - CHI
* Cleveland Cavaliers - CLE
* Dallas Mavericks - DAL
* Denver Nuggets - DEN
* Detroit Pistons - DET
* Golden State Warriors - GSW
* Houston Rockets - HOU
* Indiana Pacers - IND
* LA Clippers - LAC
* Los Angeles Lakers - LAL
* Memphis Grizzlies - MEM
* Miami Heat - MIA
* Milwaukee Bucks - MIL
* Minnesota Timberwolves - MIN
* New Orleans Pelicans - NOP
* New York Knicks - NYK
* Oklahoma City Thunder - OKC
* Orlando Magic - ORL
* Philadelphia 76ers - PHI
* Phoenix Suns - PHX
* Portland Trail Blazers - POR
* Sacramento Kings - SAC
* San Antonio Spurs - SAS
* Toronto Raptors - TOR
* Utah Jazz - UTA
* Washington Wizards - WAS \n
Please note that some teams have changed their names or relocated during this period, and the abbreviations have remained consistent with the teams' histories.
''')
    
################# Filtering data #################


df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) ]


################# Team Plots  ################# 
st.markdown("## Compare Team Performances")

selected_option = st.radio("Select Team Performance Statistics", (
    "Top 10 Total Points scored by Team",
    "Top 10 Total and Conversion Rate of 3P per Team",
    "Top 10 Total And Conversion Rate of 2P per Team",
    "Top 10 Total and Conversion Rate of FTA and FT% per Team",
    "Top 10 Total ORB AND DRB per Team",
    "Top 10 Total STL BLK per Team",
    "Top 10 Total TOV AND PF per Team",
    "Bottom 10 Total Points scored by Team"
))

if selected_option == "Top 10 Total Points scored by Team":
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(selected_year) + ".html#all_per_game_team-opponent"
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the table based on the id attribute
    table = soup.find("table", {"id": "totals-team"})
    second_table = soup.find("table", {"id": "per_game-team"})
    
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    # Sort the DataFrame by 3P in descending order and select the top 10 teams
    top_10 = df_team.sort_values(by='PTS', ascending=False).head(10)

    # Create a bar plot for 3P
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10['Team'], top_10['PTS'])
    plt.xlabel('Total Points (PTS)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest Total Points (PTS)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')

    # Display the plot
    plt.tight_layout()
    plt.grid(False)
    st.pyplot(plt)
    
elif selected_option == "Top 10 Total and Conversion Rate of 3P per Team":
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(selected_year) + ".html#all_per_game_team-opponent"
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the table based on the id attribute
    table = soup.find("table", {"id": "totals-team"})
    second_table = soup.find("table", {"id": "per_game-team"})
    
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    # Sort the DataFrame by 3P in descending order and select the top 10 teams
    top_10_3P = df_team.sort_values(by='3P', ascending=False).head(10)

    # Create a bar plot for 3P
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_3P['Team'], top_10_3P['3P'], color='skyblue')
    plt.xlabel('3-Point Field Goals (3P)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Most 3-Point Field Goals (3P)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')

    # Display the plot
    plt.tight_layout()
    plt.grid(False)
    st.pyplot(plt)

    # Sort the DataFrame by 3P% in descending order and select the top 10 teams
    top_10_3P_percent = df_team.sort_values(by='3P%', ascending=False).head(10)

    # Create a bar plot for 3P%
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_3P_percent['Team'], top_10_3P_percent['3P%'], color='lightcoral')
    plt.xlabel('3-Point Field Goal Percentage (3P%)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest 3-Point Field Goal Percentage (3P%)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', va='center')

    # Display the plot
    plt.tight_layout()
    # Remove grid lines
    plt.grid(False)
    st.pyplot(plt)
    
elif selected_option == "Top 10 Total And Conversion Rate of 2P per Team": 
    # Add code to fetch and plot "Top 10 Total And Conversion Rate of 2P per Team"
    # Fetch the data from the website
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(selected_year) + ".html#all_per_game_team-opponent"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "totals-team"})
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    # Sort the DataFrame by 2P in descending order and select the top 10 teams
    top_10_2P = df_team.sort_values(by='2P', ascending=False).head(10)

    # Create a bar plot for 2P
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_2P['Team'], top_10_2P['2P'], color='lightgreen')
    plt.xlabel('2-Point Field Goals (2P)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Most 2-Point Field Goals (2P)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')

    # Display the plot
    plt.tight_layout()
    plt.grid(False)
    st.pyplot(plt)
    
    # Sort the DataFrame by 3P% in descending order and select the top 10 teams
    top_10_2P_percent = df_team.sort_values(by='2P%', ascending=False).head(10)

    # Create a bar plot for 3P%
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_2P_percent['Team'], top_10_2P_percent['2P%'], color='lightcoral')
    plt.xlabel('3-Point Field Goal Percentage (2P%)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest 2-Point Field Goal Percentage (2P%)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', va='center')

    # Display the plot
    plt.tight_layout()
    # Remove grid lines
    plt.grid(False)
    st.pyplot(plt)
    
elif selected_option == "Top 10 Total and Conversion Rate of FTA and FT% per Team":   
    # Add code to fetch and plot "Top 10 Total And Conversion Rate of 2P per Team"
    # Fetch the data from the website
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(selected_year) + ".html#all_per_game_team-opponent"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "totals-team"})
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    # Sort the DataFrame by 2P in descending order and select the top 10 teams
    top_10_FTA = df_team.sort_values(by='FTA', ascending=False).head(10)

    # Create a bar plot for 2P
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_FTA['Team'], top_10_FTA['FTA'], color='lightgreen')
    plt.xlabel('Free Throws Attempt (FTA)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Most Free Throws Attempt (FTA)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')

    # Display the plot
    plt.tight_layout()
    plt.grid(False)
    st.pyplot(plt)
    
    # Sort the DataFrame by 3P% in descending order and select the top 10 teams
    top_10_FTA_percent = df_team.sort_values(by='FT%', ascending=False).head(10)

    # Create a bar plot for 3P%
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_FTA_percent['Team'], top_10_FTA_percent['FT%'], color='lightcoral')
    plt.xlabel('Free Throw Conversion (FT%)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest Free Throw Conversion (FT%)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', va='center')

    # Display the plot
    plt.tight_layout()
    # Remove grid lines
    plt.grid(False)
    st.pyplot(plt)   

elif selected_option == "Top 10 Total ORB AND DRB per Team":
    # Add code to fetch and plot "Top 10 Total And Conversion Rate of 2P per Team"
    # Fetch the data from the website
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(selected_year) + ".html#all_per_game_team-opponent"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "totals-team"})
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    # Sort the DataFrame by 2P in descending order and select the top 10 teams
    top_10_ORB = df_team.sort_values(by='ORB', ascending=False).head(10)

    # Create a bar plot for 2P
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_ORB['Team'], top_10_ORB['ORB'], color='lightgreen')
    plt.xlabel('Offensive Rebound (ORB)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest Offensive Rebounds (ORB)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')

    # Display the plot
    plt.tight_layout()
    plt.grid(False)
    st.pyplot(plt)
    
    # Sort the DataFrame by 3P% in descending order and select the top 10 teams
    top_10_DRB = df_team.sort_values(by='DRB', ascending=False).head(10)

    # Create a bar plot for 3P%
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_DRB['Team'], top_10_DRB['DRB'], color='lightcoral')
    plt.xlabel('Defensive Rebound (DRB)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest Defensive Rebounds (DRB)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')

    # Display the plot
    plt.tight_layout()
    # Remove grid lines
    plt.grid(False)
    st.pyplot(plt)   
    
elif selected_option == "Top 10 Total STL BLK per Team":
    # Fetch the data from the website
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(selected_year) + ".html#all_per_game_team-opponent"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "totals-team"})
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    # Sort the DataFrame by 2P in descending order and select the top 10 teams
    top_10_STL = df_team.sort_values(by='STL', ascending=False).head(10)

    # Create a bar plot for 2P
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_STL['Team'], top_10_STL['STL'], color='lightgreen')
    plt.xlabel('Steal (STL)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest Steals (STL)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')

    # Display the plot
    plt.tight_layout()
    plt.grid(False)
    st.pyplot(plt)
    
    # Sort the DataFrame by 3P% in descending order and select the top 10 teams
    top_10_BLK = df_team.sort_values(by='BLK', ascending=False).head(10)

    # Create a bar plot for 3P%
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_BLK['Team'], top_10_BLK['BLK'], color='lightcoral')
    plt.xlabel('Block (BLK)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest Blocks (BLK)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', va='center')

    # Display the plot
    plt.tight_layout()
    # Remove grid lines
    plt.grid(False)
    st.pyplot(plt)    
    
elif selected_option == "Top 10 Total TOV AND PF per Team":  
     # Fetch the data from the website
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(selected_year) + ".html#all_per_game_team-opponent"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "totals-team"})
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    # Sort the DataFrame by 2P in descending order and select the top 10 teams
    top_10_TOV = df_team.sort_values(by='TOV', ascending=False).head(10)

    # Create a bar plot for 2P
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_TOV['Team'], top_10_TOV['TOV'], color='lightgreen')
    plt.xlabel('Turnover (TOV)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest Turnovers (TOV)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va='center')

    # Display the plot
    plt.tight_layout()
    plt.grid(False)
    st.pyplot(plt)
    
    # Sort the DataFrame by 3P% in descending order and select the top 10 teams
    top_10_PF = df_team.sort_values(by='PF', ascending=False).head(10)

    # Create a bar plot for 3P%
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top_10_PF['Team'], top_10_PF['PF'], color='lightcoral')
    plt.xlabel('Personal Foul (PF)')
    plt.ylabel('Team')
    plt.title('Top 10 Teams with the Highest Personal Fouls (PF)')

    # Annotate the values
    for bar in bars:
        plt.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', va='center')

    # Display the plot
    plt.tight_layout()
    # Remove grid lines
    plt.grid(False)
    st.pyplot(plt)
    
elif selected_option == "Bottom 10 Total Points scored by Team":
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(selected_year) + ".html#all_per_game_team-opponent"
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the table based on the id attribute
    table = soup.find("table", {"id": "totals-team"})
    second_table = soup.find("table", {"id": "per_game-team"})
    
    df_team = pd.read_html(str(table))[0]
    df_team.set_index('Rk', inplace=True)
    df_team = df_team[~df_team['Team'].str.contains('League Average')]
    
    # Sort the DataFrame by 3P in descending order and select the top 10 teams
    bot_10 = df_team.sort_values(by='PTS', ascending=False).tail(10)

    # Create a bar plot for 3P
    plt.figure(figsize=(12, 6))
    bars = plt.barh(bot_10['Team'], bot_10['PTS'])
    plt.xlabel('Total Points (PTS)')
    plt.ylabel('Team')
    plt.title('Bot 10 Teams with the Highest Total Points (PTS)')  
          
################ 
# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
################ 

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href



if st.checkbox("Show Players Statistics of the selected Team(s)"):
    st.header('Player Statistics of Selected Team(s)')
    st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
    st.dataframe(df_selected_team)
    st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

  

################# Position selection #################


selected_pos = ['C','PF','SF','PG','SG']
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.multiselect('Position', unique_pos, selected_pos)
if st.checkbox("Show Position Glossary"):
    st.markdown('''
- **Point Guard (PG):** The point guard, often referred to as the "floor general," is responsible for running the team's offense. They are known for their ball-handling skills, passing, and court vision. Point guards set up plays, distribute the ball to teammates, and often take on a leadership role.

- **Shooting Guard (SG):**  The shooting guard is primarily a scoring position. They are usually one of the team's primary perimeter shooters and are expected to score points from long-range shots (three-pointers) and mid-range jumpers. Shooting guards also play a role in perimeter defense.

- **Small Forward (SF):**  Small forwards are versatile players who can contribute both offensively and defensively. They often play on the wing and are expected to score, rebound, and defend. Small forwards can be a crucial part of a team's transition game and can play a "point forward" role if they have strong playmaking skills.

- **Power Forward (PF):** Power forwards are known for their physicality and strength. They play close to the basket and are responsible for scoring in the post, grabbing rebounds, and providing interior defense. Some power forwards also have the ability to stretch the floor with their shooting.

- **Center (C):** The center is typically the tallest player on the team and plays near the basket. They are essential for shot-blocking, rebounding, and scoring in the paint. Centers are often the anchors of a team's defense, protecting the rim and altering opponents' shots.
''')





################ 
# Sidebar - Player filter (multi-select)
################ 









st.markdown("## Select Players for Individual Comparision")
st.markdown("You may choose more than one player of your choice to compare performances between them.")
st.markdown( "*Note: The data will be shown only for the year selected earlier, selected teams and positions.*")
selected_players = st.multiselect('Select Player(s)', df_selected_team['Player'].unique())


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

