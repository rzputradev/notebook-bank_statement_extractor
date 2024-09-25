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


def load_md(file_path):
   if not os.path.exists(file_path):
      raise FileNotFoundError(f"File not found: {file_path}")
   try:
      return pd.read_csv(file_path, delimiter=';')
   except Exception as e:
      print(f"Error: {e}")
      raise e


def normalize_text(text):
   try:
      return re.sub(r'\W+', ' ', text).lower()
   except Exception as e:
      print(f"Error: {e}")
      raise e
   

def fuzzy_match(text, target_text, threshold=80):
   try:
      return fuzz.partial_ratio(normalize_text(text), normalize_text(target_text)) >= threshold
   except Exception as e:
      raise e


def normalize_master_data(master_df):
   try:
      master_df['OCR_Found_Bank_normalized'] = master_df['OCR_Found_Bank'].apply(normalize_text)
      for i in range(1, 9):
            master_df[f'OCR_Found_Type_{i:02d}_normalized'] = master_df[f'OCR_Found_Type_{i:02d}'].apply(normalize_text)
      return master_df
   except Exception as e:
      print(f"Error: {e}")
      raise e
   

def convert_to_iso_8601(date_string):
   date_formats = [
      "%d-%m-%Y",
      "%Y-%m-%d",
      "%d/%m/%Y %H.%M.%S",
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y",
      "%m/%d/%Y",
      "%d-%b-%Y", 
      "%Y%m%d",
   ]
   try:  
      for date_format in date_formats:
            try:
               datetime_obj = datetime.strptime(date_string, date_format)
               return datetime_obj.strftime("%Y-%m-%dT%H:%M"), False
            except ValueError:
               continue

      return date_string, False
   except Exception as e:
      raise e
   

def clean_and_check_double(value):
   try:
      cleaned_value = re.sub(r'[^\d.,]', '', value)
      cleaned_value = cleaned_value.replace(',', '.')

      if cleaned_value.count('.') > 1:
            parts = cleaned_value.rsplit('.', 1)
            integer_part = parts[0].replace('.', '')
            decimal_part = parts[1]
            cleaned_value = f"{integer_part}.{decimal_part}"
      
      if '.' in cleaned_value:
            integer_part, decimal_part = cleaned_value.split('.', 1)
            decimal_part = decimal_part.ljust(2, '0')[:2]
            cleaned_value = f"{integer_part}.{decimal_part}"
      else:
            cleaned_value += '.00'
            
      number = float(cleaned_value)

      return number, False

   except ValueError as e:
      print(f"Error: {e}")
      return 0.00, True
   

def _concatenate_words(group):
   return ' '.join(group['word_value'])


def _concatenate_and_min(group):
   average_confidence = group['word_confidence'].min()
   return average_confidence
