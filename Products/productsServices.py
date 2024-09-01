import pandas_ta as ta
from Products.products import Products 
import pandas as pd
from functools import cache
import time
from datetime import datetime


class ProductsServices:  
    def __init__(self, mt5, timeFrame, ASSET, HOURSSTART):
        self.mt5 = mt5
        self.products = Products(self.mt5, timeFrame, ASSET, HOURSSTART)
        self.pd = pd
        self.futureNegative = 0
        self.futurePositive = 0
        self.positive = False
        self.negative = False
        
    def toTimeFrame(self):
        return self.products.tOtimeFrame()
              
    #name for dateframes func    
    def selectBar(self, valor):
        bar = self.products.selectBar(valor)
        return bar
    
    #mid price   
    def calcAMV(self):
        media = ta.midprice(self.selectBar('open'), self.selectBar('close'), 20, 0 , 0 )
        return media
        
    #Exponential Moving Average    
    def calcEma(self):
        mov = ta.ema(self.selectBar('close'), length=10)
        return mov
      
    def copyFromRates(self, mt5, asset, enumsFrame, rangeStart, rangeStop):
        copyRatesRange = self.products.copyFromRates(mt5, asset, enumsFrame, 
                            rangeStart, rangeStop)   
        return copyRatesRange
          
    #fixing  
    def vwap(self):
        vol = ta.vwap(self.selectBar('high'), self.selectBar('low'), 
              self.selectBar('close'), self.selectBar('real_volume'), anchor= 'W') 
        return vol
    
    #Accumulation/Distribution Index
    def adv(self):
        adVol = ta.ad(self.selectBar('high'), self.selectBar('low'), 
              self.selectBar('close'), self.selectBar('real_volume'),
              self.selectBar('open'), talib=False )
        return adVol
    
    #Price volume
    @cache
    def priceVol(self):
        pricevol = ta.pvol(self.selectBar('close'), self.selectBar('real_volume')) 
        pricevolConv = pd.DataFrame(pricevol)
        return pricevolConv
    
    #last bar in market
    def lastbar(self):
        bar = self.products.lastBar()
        return bar
    
    def convertToList(self, x):
        return self.products.convertToList(x)
                                        
    def addListDynamics(self, value):
        return self.products.addListDynamics(value)
   
    def maxIndex(self, value, counts):
        return self.products.maxIndex(value, counts)
        
    def lastIndex(self, value): 
        return self.products.lastIndex(value)
    
    def dayGraph(self,  value):
        return self.products.dayGraph(value)
        
    def dayForconvert(self):
        return self.products.current_day()
        
    def timeSleepNow(self):
        return self.products.timeSleepNow()

    #(mfi)volume force in buy and sell 
    def mfi(self):
        highNotConv = self.selectBar('high')
        high = pd.to_numeric(highNotConv, downcast='float')
        closeNotConv = self.selectBar('low')
        close = pd.to_numeric(closeNotConv, downcast='float') 
        mfiDataFrame = ta.mfi(high,closeNotConv,
                            self.selectBar('close'), self.selectBar('real_volume'))
        return mfiDataFrame
    
    def ad(self):
        adData = ta.ad(self.selectBar('high'), self.selectBar('low')
                       , self.selectBar('close'),  self.selectBar('real_volume'))
        return adData
    
    def eom(self):
        eomData = ta.eom(self.selectBar('high'), self.selectBar('low')
                       , self.selectBar('close'),  self.selectBar('real_volume') )
        return eomData
    
    # calcv call method
    def calcVfunc(self):
        for i in range(1000):
            calc = self.convertToList(self.lastbar()) 
            self.calcV(calc)
            self.timeSleepNow()
    
    def calcvLive(self):
        data = self.lastbar()
        self.calcV(data)
        self.timeSleepNow()
    
    #Beta  calcV method
    def calcV(self, data):
        data = round(data.iloc[4], 5) 
        if self.futureNegative == 0:
            self.futurePositive = round((data +  ((data * 0.69)/100)), 5)
            self.futureNegative = round((data - (data * 0.69)/100), 5)
        elif data < self.futurePositive and self.positive:
            #self.aiColect.colectID("Buy", self.futurePositive, data , "none",
                             #data, "Calcv", "why") #Ai 
            self.futurePositive = 0
            self.positive = False
            return True
        elif data > self.futureNegative and self.negative: 
            #self.aiColect.colectID("Sell", self.futurePositive, "none" , data , 
                            #data,"Calcv", "why") #Ai 
            self.futureNegative = 0
            self.negative = False  
            return True      
        elif data > self.futurePositive:
            if self.positive == False:
                self.futurePositive = round((data - (data * 0.48)/100), 5)
                self.positive = True
                #self.aiColect.colectID("Buy", self.futurePositive, data,
                            #"none","none", "Calv","how") #Ai
                print(self.futurePositive)
                print(datetime.now())
        elif data < self.futureNegative:
            if self.negative == False:
                self.futureNegative = round((data + (data* 0.48)/100), 5)
                self.negative = True
                print(self.futureNegative)
                print(datetime.now())
                #self.aiColect.colectID("Sell", self.futureNegative, "none",
                            #data,"none", "Calv","how") #Ai
                
                           
   