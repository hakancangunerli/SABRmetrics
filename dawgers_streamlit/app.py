# pitcher_comparison_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pybaseball import pitching_stats, batting_stats
import plotly.express as px

# Set the page configuration
st.set_page_config(
    page_title="Pitcher Risk Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Function to fetch and cache pitching data using Fangraphs
@st.cache_data(ttl=3600)
def get_pitching_data(year):
    try:
        pitchers = pitching_stats(year, qual=0)  # qual=0 includes all pitchers
        return pitchers
    except Exception as e:
        st.error(f"Error fetching pitching data: {e}")
        return pd.DataFrame()


# Function to fetch and cache team batting data by aggregating player stats
@st.cache_data(ttl=3600)
def get_team_batting_data(year, team):
    try:
        # Fetch all player batting stats for the specified year
        batting = batting_stats(year, qual=0)  # qual=0 includes all players

        if batting.empty:
            st.warning(f"No batting data found for the year {year}.")
            return pd.DataFrame()

        # Display batting DataFrame columns for verification
        # Uncomment the line below if you need to debug
        # st.write("Batting DataFrame Columns:", batting.columns.tolist())

        # Verify the correct team abbreviation
        # Common abbreviations: 'LAD' for Los Angeles Dodgers, 'LAA' for Los Angeles Angels, etc.
        # Print unique team IDs to verify
        unique_teams = batting["Team"].unique().tolist()
        # Uncomment the line below to see team abbreviations
        # st.write("Unique Teams in Batting Data:", unique_teams)

        # Filter for the specified team using the correct column name
        team_batting = batting[batting["Team"] == team]

        if team_batting.empty:
            st.warning(f"No batting data found for the team {team} in the year {year}.")
            return pd.DataFrame()

        # Aggregate team-level batting metrics
        total_hits = team_batting["H"].sum()
        total_at_bats = team_batting["AB"].sum()
        total_walks = team_batting["BB"].sum()
        total_hbp = team_batting["HBP"].sum()
        total_sf = team_batting["SF"].sum()
        total_doubles = team_batting["2B"].sum()
        total_triples = team_batting["3B"].sum()
        total_home_runs = team_batting["HR"].sum()

        # Calculate Singles
        total_singles = total_hits - total_doubles - total_triples - total_home_runs

        # Calculate Total Bases (TB)
        total_bases = (
            (total_singles)
            + (2 * total_doubles)
            + (3 * total_triples)
            + (4 * total_home_runs)
        )

        # Calculate BA, OBP, SLG
        team_ba = total_hits / total_at_bats if total_at_bats > 0 else 0
        team_obp_denominator = total_at_bats + total_walks + total_hbp + total_sf
        team_obp = (
            (total_hits + total_walks + total_hbp) / team_obp_denominator
            if team_obp_denominator > 0
            else 0
        )
        team_slg = total_bases / total_at_bats if total_at_bats > 0 else 0

        # Round the metrics to three decimal places
        team_ba = round(team_ba, 3)
        team_obp = round(team_obp, 3)
        team_slg = round(team_slg, 3)

        # Create a DataFrame with the aggregated metrics
        team_offensive = pd.DataFrame(
            {"BA": [team_ba], "OBP": [team_obp], "SLG": [team_slg]}
        )

        return team_offensive

    except Exception as e:
        st.error(f"Error fetching batting data: {e}")
        return pd.DataFrame()


# Title and Description
st.title("Pitcher Risk Analysis Tool")
st.markdown(
    """
This application allows you to compare two pitchers from a selected team and assess their potential risk against a specified opponent based on various pitching metrics.
"""
)

# Sidebar for user inputs
st.sidebar.header("User Input Parameters")

# Year Selection
current_year = pd.Timestamp.now().year
year = st.sidebar.selectbox(
    "Select Season Year", options=list(range(current_year, 2000, -1)), index=0
)

# Fetch pitching data
pitchers_df = get_pitching_data(year)

if pitchers_df.empty:
    st.warning("Pitching data is not available.")
    st.stop()

# Display pitching DataFrame columns for verification (optional)
# st.write("Pitchers DataFrame Columns:", pitchers_df.columns.tolist())

# Team Selection
teams = pitchers_df["Team"].unique().tolist()
selected_team = st.sidebar.selectbox("Select Team", options=teams, index=0)

# Filter for selected team's pitchers
team_pitchers = pitchers_df[pitchers_df["Team"] == selected_team]

if team_pitchers.empty:
    st.warning(f"No pitching data found for {selected_team}.")
    st.stop()

# Get list of pitcher names
pitcher_names = team_pitchers["Name"].unique().tolist()

# Select two pitchers
pitcher_a_name = st.sidebar.selectbox(
    "Select Pitcher A", options=pitcher_names, index=0
)
pitcher_b_name = st.sidebar.selectbox(
    "Select Pitcher B", options=pitcher_names, index=1
)

if pitcher_a_name == pitcher_b_name:
    st.sidebar.error("Please select two different pitchers.")

# Set Dodgers as the default opponent team
# Assuming 'LAD' is the abbreviation for Los Angeles Dodgers
opponent_team_default = "LAD"  # Change this if your data uses a different abbreviation

# Verify if 'LAD' exists in the teams list
if opponent_team_default in teams:
    default_opponent_index = teams.index(opponent_team_default) - 1
else:
    default_opponent_index = 0  # Fallback to the first team if 'LAD' not found

# Select opponent team with Dodgers as default
opponent_team = st.sidebar.selectbox(
    "Select Opponent Team",
    options=[team for team in teams if team != selected_team],
    index=default_opponent_index if opponent_team_default in teams else 0,
)

# Fetch team batting data for opponent
opponent_batting = get_team_batting_data(year, opponent_team)

if opponent_batting.empty:
    st.warning(f"{opponent_team} batting data is not available.")
    st.stop()


# Function to extract pitcher stats
def get_pitcher_stats(pitchers_df, pitcher_name):
    pitcher = pitchers_df[pitchers_df["Name"] == pitcher_name]
    if pitcher.empty:
        st.error(f"No data found for pitcher: {pitcher_name}")
        return None
    metrics = ["ERA", "WHIP", "FIP", "K/9", "BB/9", "HR/9", "GB%", "FB%"]
    return pitcher[metrics].iloc[0]


# Get stats for both pitchers
pitcher_a_stats = get_pitcher_stats(team_pitchers, pitcher_a_name)
pitcher_b_stats = get_pitcher_stats(team_pitchers, pitcher_b_name)

if pitcher_a_stats is None or pitcher_b_stats is None:
    st.stop()

# Display Selected Pitchers
st.header("Selected Pitchers")
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"**Pitcher A: {pitcher_a_name}**")
    st.write(pitcher_a_stats)

with col2:
    st.subheader(f"**Pitcher B: {pitcher_b_name}**")
    st.write(pitcher_b_stats)

# Comparison Table
st.header("Pitching Metrics Comparison")

comparison_df = pd.DataFrame(
    {
        "Metric": pitcher_a_stats.index,
        pitcher_a_name: pitcher_a_stats.values,
        pitcher_b_name: pitcher_b_stats.values,
    }
)

st.table(comparison_df.set_index("Metric"))

# Visualization: Bar Chart Comparison
st.header("Visual Comparison of Metrics")

melted_df = comparison_df.melt(id_vars="Metric", var_name="Pitcher", value_name="Value")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=melted_df, x="Metric", y="Value", hue="Pitcher", ax=ax)
ax.set_title("Pitching Metrics Comparison")
ax.set_ylabel("Metric Values")
ax.set_xlabel("Metrics")
plt.xticks(rotation=45)
plt.legend(title="Pitcher")

st.pyplot(fig)

# Risk Assessment Against Opponent
st.header(f"Risk Assessment Against {opponent_team}")

# Display opponent's offensive metrics
st.subheader(f"{opponent_team} Offensive Metrics")
opponent_metrics = ["BA", "OBP", "SLG"]
opponent_offensive = opponent_batting[opponent_metrics].drop_duplicates()
st.table(opponent_offensive.reset_index(drop=True))

# Improved Risk Indicator
st.subheader("Risk Indicator Based on Multiple Factors")


def normalize(series):
    min_val, max_val = series.min(), series.max()
    if min_val == max_val:
        return pd.Series(
            [0.5] * len(series)
        )  # Return mid-point if all values are the same
    return (series - min_val) / (max_val - min_val)


# Normalize relevant metrics
metrics_to_normalize = ["ERA", "WHIP", "HR/9"]
normalized_metrics = team_pitchers[["Name"] + metrics_to_normalize].set_index("Name")
for metric in metrics_to_normalize:
    normalized_metrics[f"Normalized_{metric}"] = normalize(normalized_metrics[metric])

# Calculate risk score (higher is riskier for these metrics)
risk_factors = ["Normalized_ERA", "Normalized_WHIP", "Normalized_HR/9"]
normalized_metrics["Risk_Score"] = normalized_metrics[risk_factors].mean(axis=1)

# Get risk scores for selected pitchers
risk_a = normalized_metrics.loc[pitcher_a_name, "Risk_Score"]
risk_b = normalized_metrics.loc[pitcher_b_name, "Risk_Score"]

risk_df = pd.DataFrame(
    {"Pitcher": [pitcher_a_name, pitcher_b_name], "Risk Score": [risk_a, risk_b]}
)

st.table(risk_df.set_index("Pitcher"))

# Visualization: Risk Score
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(data=risk_df, x="Pitcher", y="Risk Score", palette="Reds", ax=ax2)
ax2.set_title("Risk Score Comparison")
ax2.set_ylabel("Risk Score")
ax2.set_xlabel("Pitcher")

st.pyplot(fig2)


# Conclusion
st.header("Conclusion")
st.markdown(
    f"""
Based on the selected metrics, this analysis provides an indication of which pitcher might pose a higher risk against {opponent_team}. 
A higher risk score is generally more unfavorable for pitchers. However, this analysis is a simplification and doesn't account for all 
factors that could influence a pitcher's performance against a specific team.

For a more comprehensive analysis, consider:
- Historical performance against {opponent_team}
- Current form and recent performances
- Specific matchups against key batters
- Ballpark factors
- Weather conditions
"""
)

# Additional Features (Optional)
st.header("Additional Analysis (Coming Soon)")
st.markdown(
    """
- **Advanced Metrics:** Incorporate more advanced statistics like xFIP, SIERA, etc.
- **Pitch Type Analysis:** Breakdown of pitch types and their effectiveness.
- **Historical Performance:** How pitchers have performed in past matchups against the opponent.
- **Interactive Filters:** Allow users to filter by date ranges, specific games, or situational metrics.
- **Machine Learning Models:** Predictive models for pitcher performance based on historical data.
"""
)
