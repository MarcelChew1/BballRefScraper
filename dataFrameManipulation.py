import pandas as pd

def create_stats_df(data):
  header_row = 0
  while len([i.text for i in data[header_row] if (i.text != ' ' and i.text != '\n')]) != len(data[header_row + 1]):
    header_row += 1

  column_names = [name.text for name in data[header_row] if (name.text != ' ' and name.text != '\n')]
  df = pd.DataFrame(columns=column_names)
  
  for season in data[header_row + 1:]:
    info = [v.text for v in season]
    if (len(info) == len(column_names)):
      df.loc[len(df)] = info

  return df

