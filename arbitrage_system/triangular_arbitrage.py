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

    def get_crypto_data(self, exchange, crypto_symbol):
        files = os.listdir(self.cache_path)
        crypto_symbol_split = crypto_symbol.split('-')
        crypto_symbol_reverse = f'{crypto_symbol_split[1]}-{crypto_symbol_split[0]}'

        for file in files:
            # Normal symbol
            if re.search(f'{exchange}-{crypto_symbol}', file) != None:
                data = load_json(f'{self.cache_path}/{file}')
                return data['Data'][-1]['close']
            
            # Reversed symbol
            elif re.search(f'{exchange}-{crypto_symbol_reverse}', file) != None:
                print(file)
                data = load_json(f'{self.cache_path}/{file}')
                return data['Data'][-1]['close']
    
    # def find_triangular_arbitrage_opportunities_1(self):

    #     # self.get_crypto_data('Binance', 'BNB-ADA')
    #     successful = []
    #     for exchange in self.exchanges:
    #         first_exchange = [][0]
    #         best_exchange = []

    #         for combination in self.combinations:
    #             point_1 = combination[0]
    #             point_2 = combination[1]
    #             point_3 = combination[2]

    #             point_1_close = self.get_crypto_data(exchange, point_1)
    #             point_2_close = self.get_crypto_data(exchange, point_2)
    #             point_3_close = self.get_crypto_data(exchange, point_3)

    #             if point_1_close != None and point_2_close != None and point_3_close != None:
    #                 dict = {
    #                     'base':{
    #                         'exchange':exchange,
    #                         'symbol':point_1,
    #                         'exchange_rate':point_1_close
    #                     },
    #                     'inter':{
    #                         'exchange':exchange,
    #                         'symbol':point_2,
    #                         'exchange_rate':point_2_close
    #                     },
    #                     'end':{
    #                         'exchange':exchange,
    #                         'symbol': point_3,
    #                         'exchange_rate':point_3_close
    #                     }}
    #                 successful.append(dict)

    #     print(len(successful))
    #     print(successful[:10])

    def find_triangular_arbitrage_opportunities_2(self)
        return 


    def find_triangular_arbitrage_opprotunities(self):
        # self.get_all_crypto_combinations()
        self.get_stable_crypto_combinations()
        self.find_triangular_arbitrage_opportunities_2()

time = datetime.now()
TriangularArbitrage(1000).find_triangular_arbitrage_opprotunities()

# print(load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')['fsym'])
