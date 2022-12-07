import os
import re
import sys
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
        self.combinations = None

    def get_all_crypto_combinations(self):
        t1 = datetime.now()
        all_symbols = []
        combinations = []
        [all_symbols.append(fsym) for fsym in self.fsym]
        [all_symbols.append(tsym) for tsym in self.tsym]
        
        count = 0
        print(all_symbols)
        for base in all_symbols:
            for inter in all_symbols:
                if inter != base:
                    for end in all_symbols:
                        if end != base and end != inter:
                            combination = [base, inter, end]
                            combinations.append(combination)
                            count += 1
        t2 = datetime.now()
        print(f'TTR: {t2-t1}')

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
                            combinations.append(combination)
                            count += 1
        t2 = datetime.now()
        self.combinations = combinations
        print(f'{len(self.combinations)} Triangual Arbitrations Combinations found.')
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
        # opportunities to a file
        triangular_completion = []

        for combination in self.combinations:
            point_1 = self.get_crypto_data(combination[0])
            point_2 = self.get_crypto_data(combination[1])
            point_3 = self.get_crypto_data(combination[2])


            # INCORPORATE FEES
            if point_1 != None and point_2 != None and point_3 != None:
                investment_amount = self.investment
                current_price_1 = point_1.get('rate')
                final_investment = 0
                price_info = {}

                buy_quantity_1 = investment_amount / current_price_1
                investment_amount_2 = buy_quantity_1
                current_price_2 = point_2.get('rate')

                buy_quantity_2 = investment_amount_2 / current_price_2
                investment_amount_3 = buy_quantity_2
                current_price_3 = point_3.get('rate')

                sell_quantity_3 = investment_amount_3
                final_investment = round(sell_quantity_3 * current_price_3)
                price_info = {
                    f'{point_1.get("exchange")}-{combination[0]}':current_price_1,
                    f'{point_2.get("exchange")}-{combination[1]}':current_price_2,
                    f'{point_3.get("exchange")}-{combination[2]}':current_price_3,
                    'final_investment':final_investment
                }

                if final_investment > investment_amount and final_investment < investment_amount+2000:
                    print(price_info)

    def run_triangular_arbitrage(self):
        # self.get_all_crypto_combinations()
        self.get_stable_crypto_combinations()
        self.find_triangular_arbitrage_opportunities_2()

TriangularArbitrage(8000).run_triangular_arbitrage()