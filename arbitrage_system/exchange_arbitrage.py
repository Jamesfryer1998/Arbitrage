import os
import sys
import re
import json
from datetime import datetime
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

class Arbitrage:
    def __init__(self, fsym, tsym, exchanges, cache_path):
        self.fsym = fsym
        self.tsym = tsym
        self.exchanges = exchanges
        self.cache_path = cache_path
        # ADD IN FEES HERE, JUST A LIST OF FEES FROM EXCHANGES
        ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
        self.fees = ref_data['exchange_fees']
        self.symbol = None
        self.arbitrage = None
        
    def compare_matching_symbols(self):
        print('Comparing symbols across exchanges')
        self.symbol = f'{self.fsym}-{self.tsym}'

        files = os.listdir(self.cache_path)
        exchange_files = []

        for file in files:
            search = re.search(f'{self.symbol}', file)
            if search != None:
                exchange_files.append(file)

        self.arbitrage = []

        for _ in exchange_files:
            string = _.split('-', 1)
            exchange = string[0]
            json_data = load_json(f'{self.cache_path}/{_}')
            latest_timestamp = json_data['Data'][-1]['time']
            # print(datetime.utcfromtimestamp(latest_timestamp).strftime('%Y-%m-%d %H:%M:%S'))
            latest_close = json_data['Data'][-1]['close']
            dict = {'exchange':exchange,
                    'symbol':self.symbol,
                    'close':latest_close,
                    'time':latest_timestamp}
            self.arbitrage.append(dict)

    def profitable_exchanges(self):
        sorted_arbitrage = sorted(self.arbitrage, key=lambda k: k['close'])

        selling = sorted_arbitrage[-1]
        buying = sorted_arbitrage[0]
        if buying['time'] == selling['time']:
            print(f'Buy: {buying}')
            print(f'Sell: {selling}')

            diff = selling['close'] - buying['close']

            for key, value in self.fees.items():
                if selling['exchange'] == key:
                    selling_fee = value
                elif buying['exchange'] == key:
                    buying_fee = value
    
            all_fees = selling_fee + buying_fee
            print(f'diff: {diff}')
            print(f'fees: {all_fees}')

            if diff > all_fees:
                if os.path.exists("/Users/james/Projects/arbitrage/arbitrage_system/arbitrage_opportunities.json") == False:
                    ########################### HERERERERE
                    with open("sample.json", "w") as outfile: 
                        json.dump(dictionary, outfile) 

                print(diff-all_fees)
        else:
            print(f'Arbitrage time stamps dont match: {buying["time"]} / {selling["time"]}')

    def arbitrage_opportunities(self):
        return

arb = Arbitrage('ETH', 'USD', '1', '/Users/james/Projects/arbitrage/crypto_download/cache')
arb.compare_matching_symbols()
arb.profitable_exchanges()

            
        

        


