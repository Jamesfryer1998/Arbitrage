import sys
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

# print(load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')['exchange_fees'])


import os
import re

count = 0
files = os.listdir('/Users/james/Projects/arbitrage/crypto_download/cache')
ref_data = load_json('/Users/james/Projects/arbitrage/crypto_download/symbol_list.json')
exchanges = ref_data['exchanges']
symbol = 'BTC-USDC'

for file in files:
    for exchange in exchanges:
        # print(f'{exchange}-{symbol}')
        if re.search(f'{exchange}-{symbol}', file) != None:
            count += 1

        if count > 1:
            break
print(count)
    
    # if count >= 2 and count <= len(exchanges):
    #     print('working')
    #     return True
    # else: 
    #     return False