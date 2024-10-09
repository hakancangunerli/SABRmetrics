# The White Sox Suck, But by How Much?


![F45O7ElXcAANgsk](https://github.com/user-attachments/assets/e4019720-f552-493c-86c7-e5721af55ec8)


## Overview

The White Sox have long been considered one of the worst teams in Major League Baseball, but how much do they truly lag behind? In this analysis, we dive deep into the White Sox's performance throughout the 2000s and compare it to their crosstown rivals, the Chicago Cubs.

## Data and Analysis

This project uses the `pybaseball` library to retrieve and analyze data for both the White Sox (CHW) and the Cubs (CHC) from the 2000 season up to the current year. We examine key metrics such as runs scored, home runs, batting averages, on-base percentage (OBP), and slugging percentage (SLG) to quantify the performance of these two teams over the years.

### Data Retrieval

The analysis begins by pulling the relevant pitching and batting statistics for both teams, using the following data:

- **Pitching Statistics**: Data related to pitching performance.
- **Batting Statistics**: Data related to batting performance, filtered for the White Sox and Cubs.

### Key Metrics

#### Team Performance

We calculate the average team stats per season for both the White Sox and Cubs, including:

- **Runs (R)**
- **Home Runs (HR)**
- **Batting Average (AVG)**
- **On-base Percentage (OBP)**
- **Slugging Percentage (SLG)**

These statistics help us understand how the teams performed on average each season.

#### Top Performers

We also identify the top 5 home run hitters for each team:

- **White Sox**: Led by Paul Konerko with 385 home runs.
- **Cubs**: Led by Sammy Sosa with 238 home runs.

#### Pitching Performance

For pitching, we identify the top 5 pitchers for each team based on ERA (minimum 50 innings pitched):

- **White Sox**: Led by Esteban Loaiza with a 2.90 ERA.
- **Cubs**: Led by Jake Arrieta with a 2.80 ERA.

### Visual Analysis

We visualize the data with several plots:

- **Runs Scored by Season**: A line plot showing the runs scored each season by both teams, with a comparison of trends over the years.
- **Home Runs by Season**: A scatter plot with trendlines for home runs by season for both teams.

### Findings

- The average statistics over the 2000s show a slight edge for the White Sox in terms of runs scored and slugging percentage, but the Cubs hold their own in other categories.
- The 2000 season saw the largest difference in runs scored between the two teams, with a significant edge for one of the teams.

## Conclusion

While the White Sox have struggled, especially in recent years, the data shows that both teams have had their ups and downs throughout the 2000s. The Cubs have had some stellar individual performers, while the White Sox have managed to maintain competitive averages in key metrics. This analysis sheds light on how both teams have evolved over the years and how they compare to one another in the same city.

## Requirements

- Python 3.x
- `pybaseball`
- `pandas`
- `matplotlib`
- `numpy`
