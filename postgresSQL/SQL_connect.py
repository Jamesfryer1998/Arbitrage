import os
import sys
import pandas as pd
from datetime import datetime
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json
tri_arb_path = '/Users/james/Projects/arbitrage/arbitrage_system/triangular_arbitrage.json'

class PostgresSQL:
    def __init__(self, file_path):
        self.time = datetime.now()
        self.file_path = file_path
        self.df = None
        self.convert_to_df()

    def convert_to_df(self):
        file = load_json(self.file_path)
        data = [x for x in file]
        list_dict = []

        for i in range(0, len(data)):
            data_keys = list(data[i].keys())
            data_values = list(data[i].values())
            dict = {
                'base': data_keys[0],
                'base_price':data_values[0],
                'inter': data_keys[1],
                'inter_price':data_values[1],
                'end': data_keys[2],
                'end_price':data_values[2],
                'final_investment':data[i]['final_investment'],
                'profit': data[i]['profit'],
                'date':data[i]['time']            
            }
            list_dict.append(dict)

        self.df = pd.DataFrame(list_dict)
        # print(self.df)

    # def create_table(self):

SQL = PostgresSQL(tri_arb_path)

