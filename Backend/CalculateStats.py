import pandas as pd
import numpy as np
from teamsList import teams
import matplotlib.pyplot as plt
from scipy.stats import linregress
class CalculateStats:
  def __init__(self, player):
    self.player = player
    self.per_game_df = pd.read_csv(player.player_path + "/" + player.f_name + player.l_name + "PerGame.csv")
    self.team_ratings = {}

    for team in teams:
      if team == "NJN":
        team = "BKN"
      self.team_ratings[team] = pd.read_csv(f"teams/{team}/{team}.csv")

  def calc_variance(self):
    var_df = self.per_game_df.var(numeric_only=True)

  def calculate_hot(self):
    # split the dataframe into seperate years
    season_start_idx = self.per_game_df[self.per_game_df['G'] == 1]
    season_start_idx = list(season_start_idx.index) + [len(self.per_game_df)]

    total = 0.000001
    up = 0.000001
    per_season_rates = []
    # print(self.per_game_df["PTS"].std() / self.per_game_df["PTS"].mean())
    std_list = []
    for start, end in zip(season_start_idx, season_start_idx[1:]):
      curr_scores = self.per_game_df.iloc[start:end]["PTS"]
      average = curr_scores.mean()
      std = curr_scores.std()
      std_list.append(int(std))
      curr_scores = list(curr_scores)

      tmp_total = 0.000001
      tmp_up = 0.000001

      # for i in range(2, len(curr_scores)):
      #   if curr_scores[i - 2] < curr_scores[i - 1]:
      #     total += 1
      #     if (curr_scores[i - 1] < curr_scores[i]):
      #       up += 1
      
      # for i in range(1, len(curr_scores)):
      #   if (curr_scores[i - 1] > average + std):
      #     total += 1
      #     tmp_total += 1
      #     if (curr_scores[i] > average + std):
      #       up += 1
      #       tmp_up += 1

      # for i in range(2, len(curr_scores)):
      #   if (curr_scores[i - 2] > average and curr_scores[i - 1] > average):
      #     total += 1
      #     tmp_total += 1
      #     if (curr_scores[i] > average):
      #       up += 1
      #       tmp_up += 1

      # for i in range(1, len(curr_scores)):
      #   if (curr_scores[i - 1] > average):
      #     total += 1
      #     tmp_total += 1
      #     if (curr_scores[i] > average):
      #       up += 1
      #       tmp_up += 1

      for i in range(len(curr_scores)):
        if (curr_scores[i] > average):
          up += 1
          tmp_up += 1
        total += 1
        tmp_total += 1
      per_season_rates.append(round(tmp_up / tmp_total, 2))


    # print(std_list)
    print(up, total, up / total)
    print(per_season_rates)
    print(np.std(per_season_rates))



  def calculate_def(self):
    team_season_drtg = {
      (team, row['Year']): row['Rel DRtg']
      for team, df in self.team_ratings.items()
      for _, row in df.iterrows()
    }
    season_start_idx = list(self.per_game_df[self.per_game_df['G'] == 1].index) + [len(self.per_game_df)]

    scores = []
    opp_drtg = []

    for start, end in zip(season_start_idx, season_start_idx[1:]):
      curr_scores = self.per_game_df.iloc[start:end]["PTS"]
      opp_team = self.per_game_df.iloc[start:end]["Opp"]
      season = self.per_game_df.iloc[start:end]["Season"].iloc[0]
      print(season)
      
      for opp in opp_team:
        drtg = team_season_drtg.get((opp, season), None)
        if drtg == None:
          print(opp)
        opp_drtg.append(drtg)
    
      scores += curr_scores.to_list()

    print(len(scores), len(opp_drtg))

    # Calculate correlation coefficient
    correlation_coefficient = np.corrcoef(scores, opp_drtg)[0, 1]
    print(f'Correlation Coefficient: {correlation_coefficient}')

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(opp_drtg, scores)
    print(f'Slope: {slope}, Intercept: {intercept}, R-squared: {r_value**2}')

    # Create scatter plot
    plt.scatter(opp_drtg, scores, color='blue', label='Data points')

    # Plot regression line
    regression_line = np.array(opp_drtg) * slope + intercept
    plt.plot(opp_drtg, regression_line, color='red', label='Regression line')

    # Add title and labels
    plt.title("Player's Points vs Opponents' Defensive Rating")
    plt.xlabel("Opponents' Defensive Rating")
    plt.ylabel("Player's Points")
    plt.legend()

    plt.show()
    # print(scores, opp_drtg)



  

