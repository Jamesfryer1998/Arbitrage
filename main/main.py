import datetime
import threading
import time
import json
import sys
import os
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from crypto_download.cryptocompare_2 import CryptoCompareAPI
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

cache_path = '/Users/james/Projects/arbitrage/crypto_download/cache'

def worker(cache_path, fsym, tsym, exchange):
    CryptoCompareAPI(cache_path, fsym, tsym, exchange).run_all()

def crypto_to_stable_coin():
    ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
    count = 0

    CryptoCompareAPI(cache_path).find_available_cryptos_stable_data()
    runs = []

    for i in range(0, 4):
        t1 = datetime.datetime.now()
        jobs = []
        for data in ref_data['available_crypto_stable']:
            symbol_split = data.split('-')
            try:
                thread = threading.Thread(target=worker, args=[cache_path, symbol_split[1], symbol_split[2], symbol_split[0]])
                jobs.append(thread)
                count += 1
            except Exception as error:
                raise Exception(error)

        for t in jobs:
            t.start()

        for t in jobs:
            t.join()
        
        delta = datetime.datetime.now() - t1
        time.sleep(1)

        crypto_count = len(os.listdir(cache_path))
        expected = len(ref_data['available_crypto_stable'])
        with open('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json', 'w') as file:
            json.dump(ref_data, file, indent=2)

        
        run = [f'RUN {i+1}', f'{crypto_count} out of {expected} downloaded.', f'Programme executed in {delta} - {crypto_count} cryptos processed.']
        runs.append(run)
    
    # else:
    #     print('     Cryptos already downloaded.')

    print('CRYPTO-STABLE')
    for run in runs:
        print(run)

    print('------------------------------------')
    
def crypto_to_crypto():
    ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
    count = 0

    CryptoCompareAPI(cache_path).find_available_crypto_crypto_data()
    runs = []
    print('------------------------------------')
    for i in range(0, 4):
        t1 = datetime.datetime.now()
        jobs = []
        for data in ref_data['available_crypto_crypto']:
            symbol_split = data.split('-')
            try:
                thread = threading.Thread(target=worker, args=[cache_path, symbol_split[1], symbol_split[2], symbol_split[0]])
                jobs.append(thread)
                count += 1
            except Exception as error:
                raise Exception(error)

        for t in jobs:
            t.start()

        for t in jobs:
            t.join()
        
        delta = datetime.datetime.now() - t1
        time.sleep(1)

        crypto_count = len(os.listdir(cache_path))
        expected = len(ref_data['available_crypto_crypto'])
        with open('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json', 'w') as file:
            json.dump(ref_data, file, indent=2)

        run = [f'RUN {i+1}', f'{crypto_count} out of {expected} downloaded.', f'Programme executed in {delta} - {crypto_count} cryptos processed.']
        runs.append(run)
    else:
        print('     Cryptos already downloaded.')
        

    print('CRYPTO-CRYPTO')
    for run in runs:
        print(run)

    print('------------------------------------')
    

crypto_to_stable_coin()
crypto_to_crypto()

# TODO
# If date from first file in cache path is not datetime.now.date() then redownload, if not then check count