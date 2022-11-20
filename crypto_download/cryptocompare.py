import os
import re
import sys
import json
import requests
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json
import datetime

class CryptoCompareAPI():
    def __init__(self, cache_path, fsym, tsym, exchange, period):
        self.cache_path = cache_path
        if not os.path.isdir(self.cache_path):
                raise Exception(f"{self.cache_path} does not exist")

        self.fsym = fsym
        self.tsym = tsym
        self.exchange = exchange
        self.period = period
        self.api_key = load_json('/Users/james/Projects/arbitrage/crypto_download/api.json')['API_KEY']
        time = datetime.datetime.now()
        self.date = time.date()
        self.file_format = None

    def check_crypto_save(self):
        self.file_format = f'{self.exchange}-{self.fsym}-{self.tsym}-{self.date}.json'
        if os.path.isfile(f'{self.cache_path}/{self.file_format}') != True:
            return False
        else:
            return True

    def remove_file(self):
        time = datetime.datetime.now()
        files = os.listdir(self.cache_path)
        for file in files:
            search = re.search(f'{time.date()}', file)
            if search == None:
                os.remove(f'{self.cache_path}/{file}')
                print(f'    {file} removed')

    def download_data(self):
        if self.check_crypto_save() == False:
            url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={self.fsym}&tsym={self.tsym}&limit=100&e={self.exchange}&api_key={self.api_key}'
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to load reference data [{response.status_code}/{response.reason}]")
            else:
                data = response.json()

                if data['Response'] == 'Error':
                    raise Exception(data['Message'])

                data = data['Data']

                with open(f'{self.cache_path}/{self.file_format}', 'w') as f:
                    json.dump(data, f, indent=4)

                print(f'    {self.file_format} downloaded.')
        else:
            print(f'    {self.file_format} already downloaded.')

    def run_all(self):
        self.remove_file()
        self.download_data()
        return

CryptoCompareAPI('/Users/james/Projects/arbitrage/crypto_download/cache','BTC','USDT', 'Binance',5).run_all()


