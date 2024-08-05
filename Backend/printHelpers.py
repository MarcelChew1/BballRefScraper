def write_to_file(page, name):    
  with open(name, "w", encoding="utf-8") as file:
    file.write(page)

def read_from_file(file_name):
  with open(file_name, "r", encoding="utf-8") as file:
    return file.read()