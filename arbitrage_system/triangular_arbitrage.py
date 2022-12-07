import os
import sys
import pandas as pd
from datetime import datetime
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

class TriangularArbitrage:
    def __init__(self):
        self.time = time
        self.cache_path = '/Users/james/Projects/arbitrage/crypto_download/cache'
        ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
        self.fsym = ref_data['fsym']
        self.tsym = ref_data['tsym']

    def get_crypto_combinations(self):
        all_symbols = []
        [all_symbols.append(fsym) for fsym in self.fsym]
        [all_symbols.append(tsym) for tsym in self.tsym]
        num_symbols = len(all_symbols)

        combinations = []
        count = 0
        print(all_symbols)
        for base in all_symbols:
            print(base)
            for inter in all_symbols:
                if inter != base:
                    for end in all_symbols:
                        if end != base and end != inter:
                            combination = [base, inter, end]
                            combinations.append(combination)
                            count += 1

        df = pd.DataFrame(combinations, columns=['base', 'inter', 'end'])

        if os.path.exists("/Users/james/Projects/arbitrage/arbitrage_system/crypto_combinations.csv") == False:
            df.to_csv('/Users/james/Projects/arbitrage/arbitrage_system/crypto_combinations.csv')
            print('Combaintions Calculated.')
        elif os.path.exists("/Users/james/Projects/arbitrage/arbitrage_system/crypto_combinations.csv") == True:
            # find the length of the df



        else:
            print('Combaintions Already Calculated.')
            












    def find_triangular_arbitrage_opprotunities(self):
        self.get_crypto_combinations()

time = datetime.now()
TriangularArbitrage().find_triangular_arbitrage_opprotunities()

# print(load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')['fsym'])
