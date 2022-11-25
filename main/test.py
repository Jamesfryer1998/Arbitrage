import sys
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json

print(load_json('/Users/james/Projects/arbitrage/crypto_download/api.json')['API_KEY'])