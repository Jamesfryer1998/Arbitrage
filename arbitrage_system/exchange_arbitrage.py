import os
import sys
import re
import json
import time
from datetime import datetime
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

class Arbitrage:
    def __init__(self, fsym, tsym, cache_path):
        self.fsym = fsym
        self.tsym = tsym
        self.cache_path = cache_path
        # ADD IN FEES HERE, JUST A LIST OF FEES FROM EXCHANGES
        ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
        self.fees = ref_data['exchange_fees']
        self.exchanges = ref_data['exchanges']
        self.symbol = f'{self.fsym}-{self.tsym}'
        self.arbitrage = None
        self.arbitrage_file = '/Users/james/Projects/arbitrage/arbitrage_system/arbitrage_opportunities.json'
        
    def available_exchanges(self):
        count = 0
        files = os.listdir(self.cache_path)

        for file in files:
            for exchange in self.exchanges:
                if re.search(f'{exchange}-{self.symbol}', file) != None:
                    count += 1

        if count >= 2 or count == len(self.exchanges):
            return True
        else: 
            return False

    def compare_matching_symbols(self):
        files = os.listdir(self.cache_path)
        exchange_files = []

        for file in files:
            search = re.search(f'{self.symbol}', file)
            if search != None:
                exchange_files.append(file)
            else:
                pass

        self.arbitrage = []

        for _ in exchange_files:
            string = _.split('-', 1)
            exchange = string[0]
            json_data = load_json(f'{self.cache_path}/{_}')
            latest_timestamp = json_data['Data'][-1]['time']
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
            diff = selling['close'] - buying['close']

            for key, value in self.fees.items():
                if selling['exchange'] == key:
                    selling_fee = (value / 100) * selling['close']
                if buying['exchange'] == key:
                    buying_fee = (value / 100) * buying['close']
    
            # May need to amend this to encorporate
            # - selling fees
            # - buying fees 
            # - for each exchange
            all_fees = selling_fee + buying_fee
            profit = diff - all_fees

            # Amount to buy (INVESTMENT)

            if profit > 1:
                dict = [{'time':datetime.utcfromtimestamp(buying['time']).strftime('%Y-%m-%d'),
                        'buy_exchange':buying['exchange'],
                        'sell_exchange':selling['exchange'],
                        'symbol':self.symbol,
                        'buying_close':buying['close'],
                        'selling_close':selling['close'],
                        'fees':all_fees,
                        'difference':diff,
                        'profit':diff - all_fees
                        }]

                if os.path.exists(self.arbitrage_file) == False:
                    with open(self.arbitrage_file, "w") as file:
                        json.dump(dict, file, indent=3)
                else:
                    arbitrage_data = load_json(self.arbitrage_file)
                    if dict[0] in arbitrage_data:
                        pass
                    else:
                        print(f'Adding - {self.symbol}')
                        arbitrage_data.append(dict[0])
                        with open(self.arbitrage_file, "w+") as file:
                            json.dump(arbitrage_data, file, indent=2)

        else:
            print(f'Arbitrage time stamps dont match: {buying["time"]} / {selling["time"]}')

    def find_arbitrage(self):
        if self.available_exchanges() == True:
            self.compare_matching_symbols()
            self.profitable_exchanges()

# Arbitrage('BTC', 'USD', '/Users/james/Projects/arbitrage/crypto_download/cache').find_arbitrage()

def main():
    cache_path = '/Users/james/Projects/arbitrage/crypto_download/cache'
    ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
    fsym_ref = ref_data['fsym']
    tsym_ref = ref_data['tsym']
    count = 0
    t1 = datetime.now()
    print('Comparing symbols across exchanges...')

    if len(os.listdir(cache_path)) == 0:
        print('No files present, please download.')
    else:
        for fsym in fsym_ref:
            for tsym in tsym_ref:
                Arbitrage(fsym, tsym, cache_path).find_arbitrage()
                count += 1

        t2 = datetime.now()
        time.sleep(0.5)

        opportunities = len(load_json('/Users/james/Projects/arbitrage/arbitrage_system/arbitrage_opportunities.json'))
        print(f'{opportunities} pottential arbitrages found out of {count}.')
        print(f'{(opportunities/count)*100:.2f}% Success rate.')
        print(f'Runtime: {t2-t1}')

if __name__ == '__main__':
    main()
