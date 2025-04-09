import json;

def read_json_file(path):
  if not path:
    raise Exception("Path cannot be empty !!!");
  
  with open(path, 'r') as file:
    return json.load(file);

def write_json_file(path, data):
  if not path:
    raise Exception("Path cannot be empty !!!");

  with open(path, 'w') as file:
      return json.dump(data, file, indent=4);