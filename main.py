from Player import Player
from PlayerSeason import PlayerSeason
import pandas as pd

def main():
  first_name = input("Enter the player's first name: ").strip().lower()
  last_name = input("Enter the player's last name: ").strip().lower()
  player = Player(first_name, last_name)

  keep_going = 'Y'
  while keep_going == 'Y':
    info = input("""What information do you want (type index)\n0: Season Averages\n""")#1: Game by game\n""")
    
    if int(info) == 0:
      params = [
                "Per Game", 
                "Totals", 
                "Per Minute", 
                "Per Possession", 
                "Advanced", 
                "Adjusted Shooting",
                "Play by Play",
                "Shooting",
                "Career Highs",
                "Playoff Series"
                ]
      print("What stat/s (type index's space seperated)\nMultiple stats will be exported as xlsx, one stat will be exported as csv")
      print("\n".join(f"{i}: {params[i]}" for i in range(len(params))))

      stats = input()
      stats = sorted([int(x) for x in stats.split()])
      
      while len(stats) == 0:
        stats = input("Please Enter a number: ")
        stats = sorted([int(x) for x in stats.split()])
      
      dfs = []

      if 0 in stats:
        dfs.append(player.season.per_game_info())
      if 1 in stats:
        dfs.append(player.season.total_info())
      if 2 in stats:
        dfs.append(player.season.per_minute_info())
      if 3 in stats:
        dfs.append(player.season.per_poss_info())
      if 4 in stats:
        dfs.append(player.season.advanced_info())
      if 5 in stats:
        dfs.append(player.season.adj_shooting_info())
      if 6 in stats:
        dfs.append(player.season.play_by_play_info())
      if 7 in stats:
        dfs.append(player.season.shooting_info())
      if 8 in stats:
        dfs.append(player.season.highs_info())
      if 9 in stats:
        dfs.append(player.season.playoff_series_info())

      name = input("Enter a file name: ")

      if len(dfs) == 1:
        dfs[0].to_csv(f"{name}.csv")
      else:
        with pd.ExcelWriter(f'{name}.xlsx') as writer:
          for idx, df in zip(stats, dfs):
            df.to_excel(writer, sheet_name=params[idx], index = False)
    
    keep_going = input("Keep going? (Y/N) ")

if __name__ == "__main__":
  main()