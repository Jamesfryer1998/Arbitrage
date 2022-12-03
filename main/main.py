import datetime
import threading
import time
import sys
import os
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from crypto_download.cryptocompare import CryptoCompareAPI
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

cache_path = '/Users/james/Projects/arbitrage/crypto_download/cache'

def worker(cache_path, fsym, tsym, exchange):
    #INSERT try/except function to catch tsym error and PASS
    CryptoCompareAPI(cache_path, fsym, tsym, exchange).run_all()
    return

def main():
    t1 = datetime.datetime.now()
    ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
    fsym_ref = ref_data['fsym']
    tsym_ref = ref_data['tsym']
    exchange_ref = ref_data['exchanges']
    count = 0
    
    for exchange in exchange_ref:
        for fsym in fsym_ref:
            for tsym in tsym_ref:
                try:
                    t = threading.Thread(target=worker, args=[cache_path, fsym, tsym, exchange])
                    t.start()
                    count += 1 
                    time.sleep(0.01)
                except Exception as error:
                    raise Exception(error)

    t2 = datetime.datetime.now()
    delta = t2 - t1
    time.sleep(1)
    print('------------------------------------')
    t2 = datetime.datetime.now()
    crypto_count = len(os.listdir(cache_path))

    print(f'Programme excected in {delta} - {crypto_count} cryptos processed.')

main()
