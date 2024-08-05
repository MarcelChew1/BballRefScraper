import os
def make_dir(path):
  os.makedirs(path, exist_ok=True)

def make_parent_dir(path):
  os.makedirs(os.path.dirname(path), exist_ok=True)

def path_exists(path):
  return os.path.exists(path)