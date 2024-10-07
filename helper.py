import os
import json
import pandas as pd
import re
from rapidfuzz import fuzz
from datetime import datetime

def load_json_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f'Error: {e}')
        return None
    

def save_json_file(filepath, data):
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f'Error: {e}')

def normalize_text(text):
   try:
      return re.sub(r'\W+', ' ', text).lower()
   except Exception as e:
      print(f"Error: {e}")
      raise e
   

def get_setting_by_id(statement_id, key=None):
    try:
        settings = load_json_file("database/extractor_settings.json")
        setting = next((setting for setting in settings if setting["id"] == statement_id), None)
        if not setting:
            return None
        if key is None:
            return setting
        else:
            return setting.get(key)
    except Exception as e:
        print(f"Error: {e}")
        return None

