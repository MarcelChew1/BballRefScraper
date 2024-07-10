import requests
from bs4 import BeautifulSoup, Comment
from dataFrameManipulation import create_stats_df

def write_to_file(season_table):    
  with open("poop.txt", "w", encoding="utf-8") as file:
    file.write(season_table.prettify())

class PlayerSeason:
  def __init__(self, player):
    self.player = player
    self.url = self.player.main_profile_url()
    self.soup = self.process_page(self.url)
  
  def process_page(self, url):
    r = requests.get(url)
    if r.status_code != 200:
      return "URL error"
    soup = BeautifulSoup(r.content, "html.parser")
    return soup
  
  def convert_comment(self, input):
    comment = input.find_all(string=lambda text: isinstance(text, Comment))[0]
    comment_soup = BeautifulSoup(comment, 'html.parser')
    season_table = comment_soup.find("table", class_="stats_table")
    return season_table

  def per_game_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="per_game")
    if season_table is None:
      season_table = self.soup.find("div", id="all_per_game-playoffs_per_game")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")  

    return create_stats_df(season_stats)

  def total_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="totals")
    if season_table is None:
      season_table = self.soup.find("div", id="all_totals-playoffs_totals")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")  

    return create_stats_df(season_stats)

  def per_minute_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="per_minute")
    if season_table is None:
      season_table = self.soup.find("div", id="all_per_minute-playoffs_per_minute")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")  

    return create_stats_df(season_stats)

  def per_poss_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="per_poss")
    if season_table is None:
      season_table = self.soup.find("div", id="all_per_poss-playoffs_per_poss")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")  
    return create_stats_df(season_stats)

  def advanced_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="advanced")
    if season_table is None:
      season_table = self.soup.find("div", id="all_advanced-playoffs_advanced")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")  
    return create_stats_df(season_stats)

  def adj_shooting_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="adj_shooting")
    if season_table is None:
      season_table = self.soup.find("div", id="all_adj_shooting")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")  
    return create_stats_df(season_stats)

  def play_by_play_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="pbp")
    if season_table is None:
      season_table = self.soup.find("div", id="all_pbp-playoffs_pbp")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")  
    return create_stats_df(season_stats)
  
  def shooting_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="shooting")
    if season_table is None:
      season_table = self.soup.find("div", id="all_shooting-playoffs_shooting")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")  
    return create_stats_df(season_stats)
  
  def highs_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="highs-reg-season")
    if season_table is None:
      season_table = self.soup.find("div", id="all_highs")
      season_table = self.convert_comment(season_table)

    season_stats = season_table.find_all("tr")  
    return create_stats_df(season_stats)
  
  def playoff_series_info(self):
    season_table = self.soup.find("table", class_="stats_table", id="playoffs-series")
    if season_table is None:
      season_table = self.soup.find("div", id="all_playoffs-series")
      season_table = self.convert_comment(season_table)
    
    season_stats = season_table.find_all("tr")
    return create_stats_df(season_stats)
