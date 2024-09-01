import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz
from functools import cache
from Products.products import Products
from services.servicesOptions import ServicesMql
import os

TIMEFRAME = "1" #select time here, string type exp '2' or '3'
ASSET = "GBPUSD" #Change name of ASSETS HERE exemple :"WDOc1"
SECONDS = 2 # seconds that the graphs will be shown here 
PHONENUMBER = 4444444
HOURSSTART = '9:00:00' # IF you wish market start hours exemple '9:00:00'
#TOLLS constant
SIZESYMBOLS = 20 # size of the asset name output
DAY = 20 
MONTH = 3
YEAR = 2024
POSITIONID = 0 # name of asset id

os.system('cls')

def main(): 
    mt5.initialize()
   
    products = Products(mt5, TIMEFRAME, ASSET, HOURSSTART)
    products.colectDate()
    print("aaa")
    products.lastBar()
   
    #services = ServicesMql()
    #services.getSymbols(30)
    
    
    
    

if __name__ == "__main__":
    main()