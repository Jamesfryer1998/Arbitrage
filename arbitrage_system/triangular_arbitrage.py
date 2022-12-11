import os
import re
import sys
import json
import pandas as pd
from datetime import datetime
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

class TriangularArbitrage:
    def __init__(self, investment):
        self.investment = investment
        self.cache_path = '/Users/james/Projects/arbitrage/crypto_download/cache'
        ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
        self.fsym = ref_data['fsym']
        self.tsym = ref_data['tsym']
        self.exchanges = ref_data['exchanges']
        self.fees = ref_data['exchange_fees']
        self.combinations = []
        self.time = datetime.now()
        self.file_path = '/Users/james/Projects/arbitrage/arbitrage_system/triangular_arbitrage.json'

    def get_stable_crypto_combinations(self):
        t1 = datetime.now()
        combinations = []
        count = 0

        for base in self.tsym:
            for inter in self.fsym:
                if inter != base:
                    for end in self.fsym:
                        if end != inter:
                            combination = [f'{base}-{inter}', f'{inter}-{end}', f'{end}-{base}']
                            self.combinations.append(combination)
                            count += 1
        t2 = datetime.now()
        # self.combinations = combinations
        print(f'{count} Triangual Arbitrations Combinations found.')
        print(f'TTR: {t2-t1}')

    def get_crypto_crypto_combinations(self):
        t1 = datetime.now()
        all_symbols = []
        [all_symbols.append(fsym) for fsym in self.fsym]
        [all_symbols.append(tsym) for tsym in self.tsym]
        
        count = 0

        for base in all_symbols:
            for inter in all_symbols:
                if inter != base:
                    for end in all_symbols:
                        if end != inter:
                            combination = [f'{base}-{inter}', f'{inter}-{end}', f'{end}-{base}']
                            self.combinations.append(combination)
                            count += 1
        t2 = datetime.now()
        # self.combinations = combinations
        print(f'{count} Triangual Arbitrations Combinations found.')
        print(f'TTR: {t2-t1}')

    def get_crypto_data(self, crypto_symbol, sort_type=None):
        files = os.listdir(self.cache_path)
        crypto_symbol_split = crypto_symbol.split('-')
        crypto_symbol_reverse = f'{crypto_symbol_split[1]}-{crypto_symbol_split[0]}'

        exchange_prices = []
        for exchange in self.exchanges:
            for file in files:
                # Normal symbol
                if re.search(f'{exchange}-{crypto_symbol}', file) != None:
                    data = load_json(f'{self.cache_path}/{file}')
                    exchange_prices.append({'exchange':exchange,
                                            'rate':data['Data'][-1]['close']})

                # Reversed symbol
                elif re.search(f'{exchange}-{crypto_symbol_reverse}', file) != None:
                    data = load_json(f'{self.cache_path}/{file}')
                    exchange_prices.append({'exchange':exchange,
                                            'rate':data['Data'][-1]['close']})
        
        if len(exchange_prices) == 0:
            return None
        elif sort_type == True:
            return exchange_prices[0]
        elif sort_type == None:
            sort_by_value = sorted(exchange_prices, key=lambda i: i['rate'])
            return sort_by_value[0]


    def find_triangular_arbitrage_opportunities_2(self):
        # output opportunities to a file
        t1 = datetime.now()
        triangular_completion = []

        for combination in self.combinations:
            
            point_1 = self.get_crypto_data(combination[0])
            point_2 = self.get_crypto_data(combination[1])
            point_3 = self.get_crypto_data(combination[2])

            # INCORPORATE FEES
            if point_1 != None and point_2 != None and point_3 != None:
                price_info = {}
                investment_amount = self.investment
                final_investment = 0
                current_price_1 = point_1.get('rate')
                current_exchange_1 = point_1.get('exchange')
                
                buy_quantity_1 = (investment_amount - (self.fees[current_exchange_1] / 100 ) * investment_amount) / current_price_1
                investment_amount_2 = buy_quantity_1
                current_price_2 = point_2.get('rate')
                current_exchange_2 = point_2.get('exchange')

                buy_quantity_2 = (investment_amount_2 - (self.fees[current_exchange_2] / 100 ) * investment_amount_2) / current_price_2
                investment_amount_3 = buy_quantity_2
                current_price_3 = point_3.get('rate')
                current_exchange_3 = point_3.get('exchange')

                # sell_quantity_3 = investment_amount_3 
                sell_quantity_3 = investment_amount_3 - (investment_amount_3 * (self.fees[current_exchange_3] / 100 ))
                final_investment = round(sell_quantity_3 * current_price_3)
                price_info = {
                    f'{point_1.get("exchange")}-{combination[0]}':current_price_1,
                    f'{point_2.get("exchange")}-{combination[1]}':current_price_2,
                    f'{point_3.get("exchange")}-{combination[2]}':current_price_3,
                    'final_investment':final_investment,
                    'profit': final_investment - self.investment,
                    'time': str(self.time.date())
                }

                if final_investment > investment_amount and final_investment < investment_amount+2000:
                    triangular_completion.append(price_info)
                    print(price_info)

        t2 = datetime.now()

        if os.path.exists(self.file_path) is not True:
            with open(self.file_path, "w") as file:
                json.dump(triangular_completion, file, indent=3)

        else:
            tri_arb_data = load_json(self.file_path)
            today = str(self.time.date())

            if tri_arb_data[0]['time'] != today:
                print('new file downloaded')
                with open(self.file_path, "w") as file:
                    json.dump(triangular_completion, file, indent=3)

        print(f'{len(triangular_completion)} profitable Triangular Opportunites found.')
        print(f'Programme ran in {t2-t1}')

    def run_triangular_arbitrage(self):
        self.get_crypto_crypto_combinations()
        self.get_stable_crypto_combinations()
        self.find_triangular_arbitrage_opportunities_2()

TriangularArbitrage(8000).run_triangular_arbitrage()