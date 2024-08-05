import pandas as pd
import numpy as np
class CalculateStats:
  def __init__(self, player):
    self.player = player
    self.per_game_df = pd.read_csv(player.player_path + "/" + player.f_name + player.l_name + "PerGame.csv")
  
  def calc_variance(self):
    var_df = self.per_game_df.var(numeric_only=True)

  def calculate_hot(self):
    # split the dataframe into seperate years
    start_of_season_indexes = self.per_game_df[self.per_game_df['G'] == 1]
    start_of_season_indexes = list(start_of_season_indexes.index) + [len(self.per_game_df)]

    total = 0.000001
    up = 0.000001
    per_season_rates = []
    # print(self.per_game_df["PTS"].std() / self.per_game_df["PTS"].mean())
    std_list = []
    for start, end in zip(start_of_season_indexes, start_of_season_indexes[1:]):
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