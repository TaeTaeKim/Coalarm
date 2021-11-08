#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 09:24:05 2021

@author: bizzy
"""
import numpy as np
import pandas as pd
from pandas_ta.utils import recent_maximum_index, recent_minimum_index

# Moving Average
def MA(df, N):
    # Simple Moving Average
    df['MA'+str(N)] = df['close'].rolling(N).mean()
    # df['MA'+str(N)+'Slope'] = df['MA'+str(N)].diff()

# Bolinger Bands
def BB(df, N, multiplier):
    STD = df['close'].rolling(20).std()
    df['Middle'] = MA(df, N)
    df['Upper'] = df['Middle'] + multiplier * STD
    df['Lower'] = df['Middle'] - multiplier * STD

# Donchian Channels
def DonchianChannels(df, N):
    df['Up'] = df['high'].rolling(N).max()
    df['Down'] = df['low'].rolling(N).min()
    df['Middle'] = (df['Up'] + df['Down']) / 2    

    # df['Up2'] = df['Up'] - (df['Up'] - df['Down'])/9
    # df['Down2'] = df['Down'] + (df['Up'] - df['Down'])/9

def IBS(df):
    df['IBS'] = (df['close'] - df['low']) / (df['high'] - df['low'])

# Relative Strength Index
def RSI(df, N, signal_N=6):
    Diff = df['close'].diff()
    U = np.where(Diff > 0, Diff, 0)
    D = np.where(Diff < 0, -Diff, 0)
    # Exponential Moving Average
    AU = pd.DataFrame(U).ewm(N).mean()
    AD = pd.DataFrame(D).ewm(N).mean()
    df['RSI'] = np.array(AU / (AU+AD))
    df['RSI Signal'] = df['RSI'].rolling(signal_N).mean()

# Stochastic Slow
def StochasticSlow(df, N, K, D):
    numerator = df['close'] - df['low'].rolling(N).min()
    denominator = df['high'].rolling(N).max() - df['low'].rolling(N).min()   
    # Stochastic Fast K or Stochastic N
    FastK = numerator/denominator
    # # Stochastic Fast D
    # FastD = FastK.rolling(D).mean()
    
    # Stochastic Slow K
    df['SlowK'] = FastK.rolling(K).mean()
    # Stochastic Slow D
    df['SlowD'] = df['SlowK'].rolling(D).mean() 

# Stochastic RSI Slow
def StochasticRSI(df, N, K, D):
    RSI(df, N)
    numerator = df['RSI'] - df['RSI'].rolling(N).min()
    denominator = df['RSI'].rolling(N).max() - df['RSI'].rolling(N).min()   
    # Stochastic RSI Fast K or Stochastic RSI N
    RSIfastK = numerator/denominator
    # # Stochastic RSI Fast D
    # FastD = FastK.rolling(D).mean()

    # Stochastic RSI Slow K
    df['RSIslowK'] = RSIfastK.rolling(K).mean()
    # Stochastic RSI Slow D
    df['RSIslowD'] = df['RSIslowK'].rolling(D).mean() 

# Momentum 
def Momentum(df,N):
    Shift = df['close'].shift(N)
    df['Momentum'] = df['close'] / Shift * 100
    
# Ichmoku
def Ichmoku(df, A, B, C):
    # A, B, C -> short term, middle term, long term
    df['Conversion'] = ( df['high'].rolling(A).max() + df['low'].rolling(A).min() )/ 2
    df['Base'] = ( df['high'].rolling(B).max() + df['low'].rolling(B).min() )/ 2
    df['Lagging'] = df['close'].shift(-B)
    df['Leading1'] = ( ( df['Conversion'] + df['Base'] ) / 2 ).shift(B)
    df['Leading2'] = ( ( df['high'].rolling(C).max() + df['low'].rolling(C).max() ) / 2 ).shift(B)

# TR
def TR(df):
    tr = np.zeros(len(df))
    tr[0] = df['high'][0] - df['low'][0]
    for i in range(1, len(df)):            
        tr[i] = max(
            df['high'][i] - df['low'][i],
            abs(df['high'][i] - df['close'][i-1]),
            abs(df['low'][i] - df['close'][i-1])
            )    
    df['TR'] = tr

# ATR using Rolling Moving Average
def ATR(df, N):
    TR(df)
    atr = np.zeros(len(df))
    atr[0] = df['TR'][0]
    for i in range(1, len(df)):            
        atr[i] = df['TR'][i]/N + atr[i-1]*(N-1)/N
    df['ATR'] = atr

# ATR using Exponential Weighted Moving Average     
def ewATR(df, N):
    TR(df)
    df['ATR'] = df['TR'].ewm(N).mean()

# Exponential Weighted SuperTrend by Sofien Kaabar
# https://medium.com/swlh/the-supertrend-indicator-in-python-coding-and-back-testing-its-strategy-e37d631c33f
def SuperTrendSK(df, Pd, Factor): 
    N, multiplier = Pd, Factor
    ewATR(df, N)
    # Basic Upper Band
    df['BUB'] = ( df['high'] + df['low'] ) / 2 + multiplier*df['ATR']   
    # Basic Lower Band
    df['BLB'] = ( df['high'] + df['low'] ) / 2 - multiplier*df['ATR']   

    # Final Upper Band
    FUB = np.zeros(len(df))
    for i in range(1, len(df)):        
        if (df['BUB'][i] < FUB[i-1]) or (df['close'][i-1] > FUB[i-1]):
            FUB[i] = df['BUB'][i]            
        else:
            FUB[i] = FUB[i-1]
    df['FUB'] = FUB
    
    # Final Lower Band
    FLB = np.zeros(len(df))
    for i in range(1, len(df)):
        if (df['BLB'][i] > FLB[i-1]) or (df['close'][i-1] < FLB[i-1]):
            FLB[i] = df['BLB'][i]
        else:
            FLB[i] = FLB[i-1]
    df['FLB'] = FLB

    # SuperTrend
    ST = np.zeros(len(df))
    BUY = np.zeros(len(df))
    SELL = np.zeros(len(df))
    for i in range(1, len(df)):
        if (ST[i-1] == df['FUB'][i-1]) and (df['close'][i] <= df['FUB'][i]):
            ST[i] = df['FUB'][i]
            SELL[i] = 1
        elif (ST[i-1] == df['FUB'][i-1]) and (df['close'][i] > df['FUB'][i]):
            ST[i] = df['FLB'][i]        
            BUY[i] = 1
        elif (ST[i-1] == df['FLB'][i-1]) and (df['close'][i] >= df['FLB'][i]):
            ST[i] = df['FLB'][i]
            BUY[i] = 1
        elif (ST[i-1] == df['FLB'][i-1]) and (df['close'][i] < df['FLB'][i]):
            ST[i] = df['FUB'][i]        
            SELL[i] = 1

    df['ST'] = ST
    df['BUY'] = BUY
    df['SELL'] = SELL
    # del df['volume'], df['value'], df['TR'], df['ATR'], df['BUB'], df['BLB'], df['FUB'], df['FLB'], df['ST']

# SuperTrend V1.0 - Buy or Sell Signal by Mejia Lucas
def SuperTrend(df, Pd, Factor): 
    ATR(df, Pd)
    df['BUB'] = ( df['high'] + df['low'] ) / 2 + Factor*df['ATR']   
    df['BLB'] = ( df['high'] + df['low'] ) / 2 - Factor*df['ATR']   

    # Final Upper Band
    FUB = np.zeros(len(df))
    for i in range(1, len(df)):        
        if (df['BUB'][i] < FUB[i-1]) or (df['close'][i-1] > FUB[i-1]):
            FUB[i] = df['BUB'][i]            
        else:
            FUB[i] = FUB[i-1]
    df['FUB'] = FUB
    
    # Final Lower Band
    FLB = np.zeros(len(df))
    for i in range(1, len(df)):
        if (df['BLB'][i] > FLB[i-1]) or (df['close'][i-1] < FLB[i-1]):
            FLB[i] = df['BLB'][i]
        else:
            FLB[i] = FLB[i-1]
    df['FLB'] = FLB

    # SuperTrend
    ST = np.zeros(len(df))
    BUY = np.zeros(len(df))
    SELL = np.zeros(len(df))
    for i in range(1, len(df)):
        if (ST[i-1] == df['FUB'][i-1]) and (df['close'][i] <= df['FUB'][i]):
            ST[i] = df['FUB'][i]
            SELL[i] = 1
        elif (ST[i-1] == df['FUB'][i-1]) and (df['close'][i] > df['FUB'][i]):
            ST[i] = df['FLB'][i]        
            BUY[i] = 1
        elif (ST[i-1] == df['FLB'][i-1]) and (df['close'][i] >= df['FLB'][i]):
            ST[i] = df['FLB'][i]
            BUY[i] = 1
        elif (ST[i-1] == df['FLB'][i-1]) and (df['close'][i] < df['FLB'][i]):
            ST[i] = df['FUB'][i]        
            SELL[i] = 1

    df['ST'] = ST
    df['BUY'] = BUY
    df['SELL'] = SELL

# Heiken Ashi
def HeikenAshi(df):
    df['HEIKENclose'] = ( df['high'] + df['low'] + df['open'] + df['close'] ) / 4
    df['HEIKENopen'] = ( df['open'].shift(1) + df['close'].shift(1) ) / 2
    
    HEIKENdf = pd.DataFrame()
    HEIKENdf['close'] = df['HEIKENclose']
    HEIKENdf['oepn'] = df['HEIKENopen']
    HEIKENdf['high'] = df['high']
    HEIKENdf['low'] = df['low']
    HEIKENdf['Realclose'] = df['close']
    return HEIKENdf
    
# Aroon
def Aroon(df, N):    
    df['UP'] = 1 - ( df['high'].rolling(N+1).apply(recent_maximum_index, raw=True) / N )
    df['DOWN'] = 1 - ( df['low'].rolling(N+1).apply(recent_minimum_index, raw=True) / N )
    

class Goti:
    def __init__(self):
        self.isON = True
        self.MAX = 0
        self.MIN = 0
        self.price1 = 0
        self.price2 = 0
        self.t1 = 0
        self.t2 = 0
        self.SEED = 10000
        self.is3 = True
        self.is6 = True
        
