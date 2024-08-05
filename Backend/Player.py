import requests
from bs4 import BeautifulSoup
from PlayerOverview import PlayerOverview
from CalculateStats import CalculateStats
from PlayerIndividual import PlayerIndividual
class Player:
  def __init__(self, f_name, l_name):
    self.f_name = f_name.strip().lower()
    self.l_name = l_name.strip().lower()
    self.url_initial = self.get_url_initial()
    self.url_name = self.get_url_name()
    self.player_path = f"players/{self.f_name + self.l_name}"
    self.season = PlayerOverview(self)
    self.per_game = PlayerIndividual(self)
    self.per_game.get_all_points()
    self.stats = CalculateStats(self)
    self.stats.calculate_hot()

  def main_profile_url(self): 
    return f"https://www.basketball-reference.com/players/{self.url_initial}/{self.url_name}.html"
  
  def season_games_url(self):
    return f"https://www.basketball-reference.com/players/{self.url_initial}/{self.url_name}/gamelog"

  def season_url(self, season):
    return f"https://www.basketball-reference.com/players/{self.url_initial}/{self.url_name}/gamelog/{season}"

  def get_url_name(self):
    l_name_mod = self.l_name.replace("'", "")
    f_name_mod = self.f_name.replace("'", "")
    n = l_name_mod[:5] + f_name_mod[:2]
    i = self.url_initial

    idx = 1
    while True:
      str_idx = f"{idx:02}"
      # try this url if the url is broken the player doesn't exist
      url = f"https://www.basketball-reference.com/players/{i}/{n}{str_idx}.html"
      r = requests.get(url)
      if r.status_code != 200:
        break

      if self.correct_player(r):
        return n + str_idx
      
      idx += 1

    return None
    
  # url works check the page for the player name (note: this won't get duplicates out)
  def correct_player(self, r):
    soup = BeautifulSoup(r.content, "html.parser")
    full_name = soup.find("h1").text.split()
    
    return full_name[0].strip().lower() == self.f_name and full_name[1].strip().lower() == self.l_name

  def get_url_initial(self):
    return self.l_name[0]

  def get_f_name(self):
    return self.f_name
  
  def get_l_name(self):
    return self.l_name