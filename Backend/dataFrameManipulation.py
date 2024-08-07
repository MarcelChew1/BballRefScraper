import pandas as pd
from teamsList import old_names_dict
def create_stats_df(data):
  header = data.find("thead").find_all("tr")

  # header = header[len(header) - 1] ## in the cases when there are multiple header rows

  column_names = [v.get_text(strip=True) for v in header[len(header) - 1].find_all("th")]
  if len(header) > 1:
    ptr = 0
    for i in reversed(range(len(header) - 1)):
      for line in header[i].find_all("th"):
        colspan = line.get("colspan", 1)
        colspan = int(colspan)
        for j in range(colspan):
          column_names[j + ptr] = f"{line.get_text(strip=True)} {column_names[j + ptr]}"
        ptr += colspan

  df = pd.DataFrame(columns=column_names)
  body = data.find("tbody").find_all("tr")
  for season in body:
    info = [v.get_text(strip=True) for v in season.find_all(["th", "td"])]
    df.loc[len(df)] = info

  return df

def create_ind_stats_df(data, cols):
  df = pd.DataFrame(columns=cols)
  
  for game in data:
    info = [v.get_text(strip=True) for v in game.find_all(["th", "td"])]
    df.loc[len(df)] = info

  # need to change all old names to some standard value
  for k, v in old_names_dict.items():
    df.replace(k, v, inplace=True)
  return df

def create_csv(data, url):
  pd.set_option('future.no_silent_downcasting', True)
  data.replace("", float("NaN"), inplace=True)
  data.dropna(axis=1, how='all', inplace=True)
  data.dropna(axis=0, how='all', inplace=True)
  data.replace(float("NaN"), "0", inplace=True)
  data.to_csv(url, index=False)

