import os
import sys
import re
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

class Arbitrage:
    def __init__(self, fsym, tsym, exchanges, cache_path):
        self.fsym = fsym
        self.tsym = tsym
        self.exchanges = exchanges
        self.cache_path = cache_path
        
    def compare_symbols(self):
        print('Comparing symbols across exchanges')
        symbol = f'{self.fsym}-{self.tsym}'

        files = os.listdir(self.cache_path)
        for file in files:
            search = re.search(f'{symbol}', file)
            if search != None:
                print(file)

Arbitrage('BTC', 'USDT', '1', '/Users/james/Projects/arbitrage/crypto_download/cache').compare_symbols()

            
        

        


