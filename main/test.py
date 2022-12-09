import sys
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

# print(load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')['exchange_fees'])

import os
import requests
import json
from datetime import datetime 
# file_format =  'Binance-ADA-BUSD-2022-12-08.json'
# cache_path = '/Users/james/Projects/arbitrage/crypto_download/cache'

def call_api(exchange, fsym, tsym):
    api_key = 'e217d6cb1e0cb559030318b9e5e71e1ddcf9f7f46e4ea641dc7ed42dba187ad3'
    cache_path = '/Users/james/Projects/arbitrage/tests/test_cache'
    time = datetime.now()
    date = time.date()
    file_format =  f'{exchange}-{fsym}-{tsym}-{date}.json'
    if os.path.isfile(f'{cache_path}/{file_format}') == False:
        url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={fsym}&tsym={tsym}&limit=100&e={exchange}&api_key={api_key}'
        response = requests.get(url)

        if response.status_code != 200:
                raise Exception(f"Failed to load reference data [{response.status_code}/{response.reason}]")
        else:
            data = response.json()

            if data['Response'] == 'Error':
                pass
            
            data = data['Data']

            if len(data) != 0 and data['Data'][0]['volumefrom'] != 0 and data['Data'][0]['volumeto'] != 0:
                with open(f'{cache_path}/{file_format}', 'w') as f:
                    json.dump(data, f, indent=4)
                print(f'    {file_format} downloaded.')
                response.close()
                return 1

            else:
                # Invalid Data
                return 0

good_calls = 0
bad_calls = 0
exchanges = ['Binance']
fsyms = ['BTC', 'ETH']
tsyms = ['USD', 'USDC', 'BTC']
ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')

for exchange in exchanges:
    for tsym in tsyms:
        for fsym in fsyms:
            symbol = f'{exchange}-{fsym}-{tsym}'
            if symbol in ref_data['available_crypto']:
                if call_api(exchange, fsym, tsym) == 1:
                    good_calls += 1
                    ref_data['available_crypto'].append(symbol)
                    with open('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json', 'w') as file:
                        json.dump(ref_data, file, indent=2)
                else:
                    bad_calls += 1

            else:
                print(f'{symbol} not avaible')

print(f'Good: {good_calls}')
print(f'Bad: {bad_calls}')





