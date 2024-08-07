import requests
import time
import re
from bs4 import BeautifulSoup, Comment
from dataFrameManipulation import create_ind_stats_df, create_csv
import pandas as pd
from printHelpers import write_to_file, read_from_file
from pathChecking import make_dir, path_exists

class PlayerIndividual:
  def __init__(self, player):
    self.player = player
    self.url = f"https://www.basketball-reference.com//players/{self.player.url_initial}/{self.player.url_name}/gamelog/"
    self.player_path = f"players/{self.player.f_name + self.player.l_name}"

  def get_all_points(self):
    if path_exists(self.get_player_csv_path()):
      return
    year = 2024
    df_list = []
    t_head = []
    make_dir(self.player_path)
    while True: 
      player_year_path = self.get_player_year_path(year)
      if path_exists(player_year_path):
        content = read_from_file(player_year_path) 
        soup = self.soup_process(content)
      else:
        season_url = self.url + str(year)
        soup = self.process_page(season_url)
        if soup == "URL error":
          break
        write_to_file(soup.prettify(), player_year_path)

      table = soup.find("table", class_="stats_table")
      if table == None: 
        break
      
      if t_head == []:
        t_head = [v.get_text(strip=True) for v in table.find("thead").find_all("th")]

      season_stats = table.find_all("tr", id=re.compile(r'^pgl_basic\.\d+$'))

      curr_df = create_ind_stats_df(season_stats, t_head)
      curr_df['Season'] = year
      df_list.append(curr_df)
      year -= 1

    total_stats = pd.concat(df_list, ignore_index=True)
    create_csv(total_stats, self.get_player_csv_path())

  def process_page(self, url):
    r = requests.get(url)
    print(r.status_code)
    if r.status_code != 200:
      return "URL error"
    return self.soup_process(r.content)
  
  def soup_process(self, content):
    soup = BeautifulSoup(content, "html.parser")
    return soup
  
  def get_player_year_path(self, year):
    return self.player_path + "/" + self.player.f_name + self.player.l_name + str(year) + ".html"
  
  def get_player_csv_path(self):
    return self.player_path + "/" + self.player.f_name + self.player.l_name + "PerGame.csv"