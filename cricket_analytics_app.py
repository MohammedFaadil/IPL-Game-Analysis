import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('ipl_match_results_sample_300.csv')

# Function to calculate win percentage for a team
def calculate_win_percentage(team_name):
    total_matches = len(df[(df['team1'] == team_name) | (df['team2'] == team_name)])
    total_wins = len(df[((df['team1'] == team_name) & (df['winner'] == team_name)) |
                        ((df['team2'] == team_name) & (df['winner'] == team_name))])
    return (total_wins / total_matches) * 100 if total_matches else 0

# Function to calculate toss win percentage for a team
def calculate_toss_win_percentage(team_name):
    total_matches = len(df[(df['team1'] == team_name) | (df['team2'] == team_name)])
    total_toss_wins = len(df[((df['team1'] == team_name) & (df['toss_winner'] == team_name)) |
                             ((df['team2'] == team_name) & (df['toss_winner'] == team_name))])
    return (total_toss_wins / total_matches) * 100 if total_matches else 0

# Team selection and season filtering
st.title("IPL Match Analytics Dashboard")
teams = df['team1'].unique()
selected_team = st.selectbox("Select Team", teams)

# Calculate statistics for the selected team
win_percentage = calculate_win_percentage(selected_team)
toss_win_percentage = calculate_toss_win_percentage(selected_team)

# Display stats for the selected team
st.header(f"{selected_team} Statistics")
st.write(f"Total Matches Played: {len(df[(df['team1'] == selected_team) | (df['team2'] == selected_team)])}")
st.write(f"Total Wins: {len(df[((df['team1'] == selected_team) & (df['winner'] == selected_team)) | ((df['team2'] == selected_team) & (df['winner'] == selected_team))])}")
st.write(f"Win Percentage: {win_percentage:.2f}%")
st.write(f"Toss Win Percentage: {toss_win_percentage:.2f}%")

# Plotting the team-specific performance
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df[(df['team1'] == selected_team) | (df['team2'] == selected_team)], 
              x='season', hue='winner', ax=ax)
ax.set_title(f'{selected_team} Match Wins Over the Seasons')
ax.set_xlabel('Season')
ax.set_ylabel('Number of Matches')
st.pyplot(fig)

# Additional plots for toss decision and win percentage based on toss
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.countplot(data=df[(df['team1'] == selected_team) | (df['team2'] == selected_team)],
              x='toss_decision', hue='winner', ax=ax2)
ax2.set_title(f'{selected_team} Toss Decision Analysis')
ax2.set_xlabel('Toss Decision')
ax2.set_ylabel('Number of Matches')
st.pyplot(fig2)

# Display some of the latest matches played by the selected team
st.subheader(f"Recent Matches of {selected_team}")
recent_matches = df[(df['team1'] == selected_team) | (df['team2'] == selected_team)].sort_values(by='date', ascending=False).head(10)
st.dataframe(recent_matches[['date', 'team1', 'team2', 'venue', 'toss_winner', 'toss_decision', 'winner']])

# Allow the user to select a season for a deeper dive
selected_season = st.slider("Select Season", min_value=df['season'].min(), max_value=df['season'].max(), value=df['season'].max())
season_data = df[df['season'] == selected_season]

# Plot the season's matches for the selected team
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.countplot(data=season_data[(season_data['team1'] == selected_team) | (season_data['team2'] == selected_team)], 
              x='venue', hue='winner', ax=ax3)
ax3.set_title(f'{selected_team} Performance in {selected_season} Season')
ax3.set_xlabel('Venue')
ax3.set_ylabel('Number of Matches')
st.pyplot(fig3)

