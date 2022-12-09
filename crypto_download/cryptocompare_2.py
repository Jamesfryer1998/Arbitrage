import os
import re
import sys
import json
import time
import requests
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json
import datetime

class CryptoCompareAPI():
    def __init__(self, cache_path, fsym=None, tsym=None, exchange=None):
        self.cache_path = cache_path
        if not os.path.isdir(self.cache_path):
                raise Exception(f"{self.cache_path} does not exist")
        self.fsym = fsym
        self.tsym = tsym
        self.exchange = exchange
        self.api_key = load_json('/Users/james/Projects/arbitrage/crypto_download/api.json')['API_KEY']
        ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
        self.ref_data = ref_data
        time = datetime.datetime.now()
        self.date = time.date()
        self.file_format = None
        self.symbol_format = None
    
    def update_counts(self):
        # fsym_count = len(self.ref_data['fsym'])
        self.ref_data['fsym_count'] = len(self.ref_data['fsym'])
        self.ref_data['tsym_count'] = len(self.ref_data['tsym'])
        self.ref_data['exchange_count'] = len(self.ref_data['exchanges'])

        with open('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json', 'w') as file:
            json.dump(self.ref_data, file, indent=2)

        # tsym_count = len(self.ref_data['tsym'])

        # exchange_count = len(self.ref_data['exchanges'])


    def find_available_cryptos_stable_data(self):
        num_fsym = len(self.ref_data['fsym'])
        fsym_count = self.ref_data['fsym_count']
        num_tsym = len(self.ref_data['tsym'])
        tsym_count = self.ref_data['tsym_count']
        num_exchange = len(self.ref_data['exchanges'])
        exchange_count = self.ref_data['exchange_count']

        if num_fsym != fsym_count or num_tsym != tsym_count or num_exchange != exchange_count:
            for exchange in self.ref_data['exchanges']:
                for fsym in self.ref_data['fsym']:
                    for tsym in self.ref_data['tsym']:
                        symbol_format = f'{exchange}-{fsym}-{tsym}'

                        url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={fsym}&tsym={tsym}&limit=100&e={exchange}&api_key={self.api_key}'
                        response = requests.get(url)
                        if response.status_code != 200:
                                raise Exception(f"Failed to load reference data [{response.status_code}/{response.reason}]")
                        else:
                            data = response.json()

                            if data['Response'] == 'Error':
                                pass
                            
                            data = data['Data']
                            
                            if len(data) != 0 and data['Data'][0]['volumefrom'] != 0 and data['Data'][0]['volumeto'] != 0:
                                if symbol_format not in self.ref_data['available_crypto_stable']:
                                    self.ref_data['available_crypto_stable'].append(symbol_format)
                                    crypto_count = self.ref_data['crypto_count']
                                    self.ref_data['crypto_count'] = crypto_count + 1
                                    self.update_counts()
                                    print(f'    {symbol_format} added.')
                                    with open('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json', 'w') as file:
                                        json.dump(self.ref_data, file, indent=2)
            
            time.sleep(1)
        else:
            print('     All available crypto-stable pairs found...')

    def find_available_crypto_crypto_data(self):
        num_fsym = len(self.ref_data['fsym'])
        fsym_count = self.ref_data['fsym_count']
        num_exchange = len(self.ref_data['exchanges'])
        exchange_count = self.ref_data['exchange_count']

        if num_fsym != fsym_count or num_exchange != exchange_count:
            for exchange in self.ref_data['exchanges']:
                for fsym_1 in self.ref_data['fsym']:
                    for fsym_2 in self.ref_data['tsym']:
                        symbol_format = f'{exchange}-{fsym_1}-{fsym_2}'

                        url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={fsym_1}&tsym={fsym_2}&limit=100&e={exchange}&api_key={self.api_key}'
                        response = requests.get(url)
                        if response.status_code != 200:
                                raise Exception(f"Failed to load reference data [{response.status_code}/{response.reason}]")
                        else:
                            data = response.json()

                            if data['Response'] == 'Error':
                                pass
                            
                            data = data['Data']
                            
                            if len(data) != 0 and data['Data'][0]['volumefrom'] != 0 and data['Data'][0]['volumeto'] != 0:
                                if symbol_format not in self.ref_data['available_crypto_stable']:
                                    self.ref_data['available_crypto_stable'].append(symbol_format)
                                    crypto_count = self.ref_data['crypto_count']
                                    self.ref_data['crypto_count'] = crypto_count + 1
                                    self.update_counts()
                                    print(f'    {symbol_format} added.')
                                    with open('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json', 'w') as file:
                                        json.dump(self.ref_data, file, indent=2)
            
            time.sleep(1)
        else:
            print('     All available crypto-stable pairs found...')

    def remove_file(self):
        files = os.listdir(self.cache_path)
        for file in files:
            search = re.search(f'{self.date}', file)
            if search == None:
                os.remove(f'{self.cache_path}/{file}')
                print(f'    {file} removed')
    
    def download_data(self):
        self.file_format = f'{self.exchange}-{self.fsym}-{self.tsym}-{self.date}.json'
        symbol_format = f'{self.exchange}-{self.fsym}-{self.tsym}'
        if not os.path.isfile(f'{self.cache_path}/{self.file_format}'):
            self.remove_file()
            url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={self.fsym}&tsym={self.tsym}&limit=100&e={self.exchange}&api_key={self.api_key}'
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to load reference data [{response.status_code}/{response.reason}]")
            else:
                data = response.json()

                if data['Response'] == 'Error':
                    pass
                
                data = data['Data']

                if len(data) != 0 and data['Data'][0]['volumefrom'] != 0 and data['Data'][0]['volumeto'] != 0:
                    with open(f'{self.cache_path}/{self.file_format}', 'w') as f:
                        json.dump(data, f, indent=4)
                    print(f'    {self.file_format} downloaded.')
                else:
                    # Invalid Data
                    pass

        # else:
        #     print(f'{self.file_format} already downloaded.')
            
    def run_all(self):
        self.download_data()