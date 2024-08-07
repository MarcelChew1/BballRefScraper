import requests
from bs4 import BeautifulSoup, Comment
from dataFrameManipulation import create_stats_df, create_csv
from pathChecking import make_dir, path_exists
from printHelpers import write_to_file, read_from_file
from teamsList import teams

url = "https://www.basketball-reference.com/teams"

for team in teams:
  print(team)
  team_url = f"{url}/{team}/"

  if team == "NJN":
    team = "BKN"

  path =  f"teams/{team}"
  make_dir(path)

  if path_exists(f"{path}/{team}.html"):
    content = read_from_file(f"{path}/{team}.html") 
    soup = BeautifulSoup(content, "html.parser")
  else:
    r = requests.get(team_url)
    if r.status_code != 200:
      print("URL error", r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
    write_to_file(soup.prettify(), f"{path}/{team}.html")

  table = soup.find("table", class_="stats_table")

  df = create_stats_df(table)
  df['Year'] = df['Season'].str[:2] + df['Season'].str[5:7]
  create_csv(df, f"{path}/{team}.csv")