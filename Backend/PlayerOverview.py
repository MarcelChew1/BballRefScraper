import requests
from bs4 import BeautifulSoup, Comment
from dataFrameManipulation import create_stats_df, create_csv
from pathChecking import make_dir, path_exists
from printHelpers import write_to_file, read_from_file
import pandas as pd

class PlayerOverview:
  def __init__(self, player):
    self.player = player
    self.url = self.player.main_profile_url()
    self.soup = self.get_soup()
  
  def get_soup(self):
    make_dir(self.player.player_path)
    overview_path = self.player.player_path + "/" + self.player.f_name + self.player.l_name + ".html"
    if path_exists(overview_path):
      soup = self.soup_process(read_from_file(overview_path))
    else:
      soup = self.process_page(self.url)
      write_to_file(soup.prettify(), overview_path)
  
    return soup

  def process_page(self, url):
    r = requests.get(url)
    if r.status_code != 200:
      return "URL error"
    
    return self.soup_process(r.content)
  
  def soup_process(self, content):
    soup = BeautifulSoup(content, "html.parser")
    return soup
  
  def convert_comment(self, input):
    comment = input.find_all(string=lambda text: isinstance(text, Comment))[0]
    comment_soup = BeautifulSoup(comment, 'html.parser')
    season_table = comment_soup.find("table", class_="stats_table")
    return season_table

  def generate_response(self, url, table_id, div_id):
    if path_exists(url):
      return pd.read_csv(url)
    season_table = self.soup.find("table", class_="stats_table", id=table_id)
    if season_table is None:
      season_table = self.soup.find("div", id=div_id)
      season_table = self.convert_comment(season_table)
    df = create_stats_df(season_table)

    create_csv(df, url)
    return df

  def per_game_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}per_game_info.csv"
    return self.generate_response(curr_url, "per_game", "all_per_game-playoffs_per_game")

  def total_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}total_info.csv"
    return self.generate_response(curr_url, "totals", "all_totals-playoffs_totals")

  def per_minute_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}per_minute_info.csv"
    return self.generate_response(curr_url, "per_minute", "all_per_minute-playoffs_per_minute")

  def per_poss_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}per_poss_info.csv"
    return self.generate_response(curr_url, "per_poss", "all_per_poss-playoffs_per_poss")

  def advanced_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}advanced_info.csv"
    return self.generate_response(curr_url, "advanced", "all_advanced-playoffs_advanced")

  def adj_shooting_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}adj_shooting_info.csv"
    return self.generate_response(curr_url, "adj_shooting", "all_adj_shooting")

  def play_by_play_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}play_by_play_info.csv"
    return self.generate_response(curr_url, "pbp", "all_pbp-playoffs_pbp")

  def shooting_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}shooting_info.csv"
    return self.generate_response(curr_url, "shooting", "all_shooting-playoffs_shooting")

  def highs_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}highs_info.csv"
    return self.generate_response(curr_url, "highs-reg-season", "all_highs")

  def playoff_series_info(self):
    curr_url = f"{self.player.player_path}/{self.player.f_name}{self.player.l_name}playoff_series_info.csv"
    return self.generate_response(curr_url, "playoffs-series", "all_playoffs-series")
