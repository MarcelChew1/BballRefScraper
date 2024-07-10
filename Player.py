import requests
from bs4 import BeautifulSoup
from PlayerSeason import PlayerSeason

class Player:
  def __init__(self, f_name, l_name):
    self.f_name = f_name.strip().lower()
    self.l_name = l_name.strip().lower()
    self.url_initial = self.get_url_initial()
    self.url_name = self.get_url_name()
    if self.url_name is None:
      print(f"Player {self.f_name} {self.l_name} does not exist.")
      exit() 
    self.season = PlayerSeason(self)

  def main_profile_url(self): 
    return f"https://www.basketball-reference.com/players/{self.url_initial}/{self.url_name}.html"

  def season_url(self, season):
    return f"https://www.basketball-reference.com/players/{self.url_initial}/{self.url_name}/gamelog/{season}"

  def get_url_name(self):
    n = self.l_name[:5] + self.f_name[:2]
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
