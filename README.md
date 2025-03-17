# StatsVLR Predictor

## Table of Contents
- [About the Project](#about-the-project)
- [How It Works](#how-it-works)
- [Current Prediction Method](#current-prediction-method)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

## About the Project
StatsVLR Predictor is a simple tool designed to predict the winner of an upcoming Valorant match using past match history and win rates. The project currently relies on basic statistical analysis but aims to improve by incorporating more advanced factors.

## How It Works
1. The predictor retrieves match history data for both teams from an API.
2. It calculates the overall win rate of both teams.
3. The team with the higher win rate is predicted as the winner.
4. The predictor prints logs showing the calculations used in the prediction.

## Current Prediction Method
The predictor makes its decision based on the following:
- It fetches the match history of both teams.
- It counts the number of matches each team has won.
- It calculates the win rate as:
  \[ Win Rate = (Total Wins / Total Matches) \]
- The team with the **higher win rate** is selected as the predicted winner.
- The calculation logs are displayed to show how the decision was made.

## Limitations
While the current predictor provides a basic analysis, it has several limitations:
- **Ignores Recent Performance**: It treats all past matches equally, regardless of how recent they are.
- **No Strength of Opponent Consideration**: It does not account for whether a team won against strong or weak opponents.
- **No Head-to-Head Analysis**: It does not check if one team historically performs well against the other.
- **No Map Data**: It does not consider if a team has a better win rate on certain maps.
- **No Roster Changes Consideration**: It assumes past performance is still relevant despite potential roster changes.

## Future Improvements
To improve accuracy, we plan to implement the following features:
- **Recent Form Weighting**: Give more importance to recent matches over older ones.
- **Head-to-Head Record**: Compare past matches between the two teams directly.
- **Opponent Strength (ELO Rating)**: Adjust win rates based on the strength of opponents.
- **Map Win Rates**: Consider team performances on specific maps.
- **Player Statistics**: Include key player metrics such as K/D ratio, clutch success rate, and first blood percentage.

## License
This project is licensed under the **MIT License**. You are free to use, modify, and distribute it with proper attribution.