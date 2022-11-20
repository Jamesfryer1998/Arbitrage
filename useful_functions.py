import json
import datetime
import os
import re
import pandas as pd

def load_json(path):
    with open(path) as f:
        data = json.load(f)
        return data

def remove_date_files(file_path):
    time = datetime.datetime.now()
    files = os.listdir(file_path)
    for file in files:
        search = re.search(f'{time.date()}', file)
        if search == None:
            os.remove(f'{file_path}/{file}')
            print(f'{file} removed')

def time_convert(unix):
     return datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d') 

