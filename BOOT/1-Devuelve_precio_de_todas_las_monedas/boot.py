import config
from binance.client import Client
from binance.enums import *

client = Client( config.API_KEY, config.API_SECRET, tld='com' ) 

list_of_tickers = client.get_all_tickers()
print(list_of_tickers)


