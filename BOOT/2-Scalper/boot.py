#CREAMOS UN BOOT DE SCALPER PARA LA COMPRA DE MONEDA#
#Autor: Daniel A. Juarez
#Fecha: 02/03/2022
#
import config #importamos las APIS
from binance.client import Client #Importamos el cleinte
from binance.enums import *
import time
import datetime
import numpy as np

client = Client( config.API_KEY, config.API_SECRET, tld='com' ) #Pasamos las APIS al cliente
symbolTicker = 'BTCUSDT'
quantityOrders = '0.00011' #aprox 5usd para operar

#Funcion que calcula la media de 50 en un punto actual
def _ma50_():
    klines = client.get_historical_klines(symbolTicker, Client.KILINE_INTERNAL_15MINUTE, "15 hour ago UTC")

    
