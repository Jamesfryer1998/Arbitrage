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
    t1 = datetime.datetime.now()
    ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
    fsym_ref = ref_data['fsym']
    tsym_ref = ref_data['tsym']
    exchange_ref = ref_data['exchanges']
    crypto_count = len(os.listdir(cache_path))
    count = 0
    
    if ref_data['downloaded'] != crypto_count:
        jobs = []
        for exchange in exchange_ref:
            for fsym in fsym_ref:
                for tsym in tsym_ref:
                    try:
                        thread = threading.Thread(target=worker, args=[cache_path, fsym, tsym, exchange])
                        jobs.append(thread)
                        # available_cryptos.append(symbol_format)
                        count += 1
                    except Exception as error:
                        raise Exception(error)

        for t in jobs:
            t.start()

        for t in jobs:
            t.join()
        
        t2 = datetime.datetime.now()
        delta = t2 - t1
        time.sleep(1)

        # ref_data['downloaded'] = crypto_count
        # print(available_cryptos)

        with open('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json', 'w') as file:
            json.dump(ref_data, file, indent=2)

        print('------------------------------------')
        print(f'Programme excected in {delta} - {crypto_count} cryptos processed.')
    else:
        print('All available cryptos-stable downloaded.')
        pass

def crypto_to_crypto():
    t1 = datetime.datetime.now()
    ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
    fsym_ref = ref_data['fsym']
    # tsym_ref = ref_data['tsym']
    exchange_ref = ref_data['exchanges']
    crypto_count = len(os.listdir(cache_path))
    count = 0

    # if ref_data['downloaded'] != crypto_count:
    for exchange in exchange_ref:
        for fsym_1 in fsym_ref:
            for fsym_2 in fsym_ref:
                try:
                    t = threading.Thread(target=worker, args=[cache_path, fsym_1, fsym_2, exchange])
                    t.start()
                    count += 1 
                    time.sleep(0.01)
                except Exception as error:
                    raise Exception(error)

    t2 = datetime.datetime.now()
    delta = t2 - t1
    time.sleep(1)
    print('------------------------------------')
    ref_data['downloaded'] = crypto_count

    with open('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json', 'w') as file:
        json.dump(ref_data, file, indent=2)

    print(f'Programme excected in {delta} - {crypto_count} cryptos processed.')
    # else:
    #     print('All available cryptos downloaded.')
    #     pass

crypto_to_stable_coin()
# crypto_to_crypto()

# TODO
# If date from first file in cache path is not datetime.now.date() then redownload, if not then check count