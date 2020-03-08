#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 10:59:46 2020

@author: Christo Strydom
"""
import tensorflow as tf
from tensorflow import keras

import os
import tempfile

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import sklearn
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
os.chdir('/media/lnr-ai/christo/github_repos/ae_mp/')
# from sklearn.model_selection import train_test_split
# import pandas as pd
# import numpy as np
#%%
mpl.rcParams['figure.figsize'] = (12, 10)
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

#%%
ae_candles_filename = 'data/USDZAR_Candlestick_5_M_BID_01.01.2019-08.02.2020_wrangled.csv'
ae_df=pd.read_csv(ae_candles_filename)

#%%

def time_filter_fn(df, start_int_seconds, end_int_seconds):
   return (ae_df['int_seconds']>=start_int_seconds) & (ae_df['int_seconds']<=end_int_seconds)

def businessday_filter_fn(df):
   return df['is_business_day']

def mp_filter_fn(df, start_int_seconds, end_int_seconds):
   time_filter=time_filter_fn(df, start_int_seconds, end_int_seconds)
   businessday_filter=businessday_filter_fn(df)
   return time_filter&businessday_filter

def days_fn(df,mp_filter):
   return list(set(df.loc[mp_filter, 'date'])) 
# days=list(set(ae_df.loc[mp_filter, 'date'])) 

def day_filter_fn(df,day):
   return df['date']==day

def range_fn(df, day_filter):
   on_high=max(df.loc[day_filter, 'high'])
   on_low=max(df.loc[day_filter, 'low'])   
   on_range=on_high-on_low
   return on_high, on_low, on_range

def on_fn(df, day_filter, on_high, on_low, on_range):
   df.loc[day_filter, 'on_low']=on_low
   df.loc[day_filter, 'on_high']=on_high
   df.loc[day_filter, 'on_range']=on_range
   return df

def order_fn(df,day_filter, perc_level, on_high, on_low, on_range):   
   df.loc[day_filter, 'sell_{perc_level}'.format(perc_level=perc_level)]=on_high+perc_level*on_range/100
   df.loc[day_filter, 'buy_{perc_level}'.format(perc_level=perc_level)]=on_low-perc_level*on_range/100
   return df

def trade_range_fn(df, day):
   day_filter=day_filter_fn(df, day)
   on_high, on_low, on_range=range_fn(df, day_filter)
   df=on_fn(df, day_filter, on_high, on_low, on_range)
   for perc_level in [50,75,100]:
      df=order_fn(df=df,day_filter=day_filter, 
                  perc_level=perc_level, 
                  on_high=on_high, 
                  on_low=on_low, 
                  on_range=on_range)
   return df

#%%
# ae_df['jhb_timestamp']==2019-01-01 02:05:00
list(ae_df)
ae_df_list=['datetime',
 'date',
 'Gmt time',
 'Open',
 'High',
 'Low',
 'Close',
 'Volume',
 'bidopen',
 'bidclose',
 'bidhigh',
 'bidlow',
 'askopen',
 'askclose',
 'askhigh',
 'asklow',
 'tickqty',
 'open',
 'high',
 'low',
 'close',
 'period',
 'dom',
 'awdn',
 'month',
 'doy',
 'wny',
 'timestamp',
 'ny_timestamp',
 'london_timestamp',
 'jhb_timestamp',
 'int_seconds',
 'universaldate',
 'is_business_day',
 'previous_business_day',
 'five_previous_business_day']
format_str=MP_FXCM_DATETIME_FORMAT='%Y-%m-%d %H:%M:%S'
ae_df['jhb_timestamp'] =  pd.to_datetime(ae_df['jhb_timestamp'], format=format_str)
format_str='%Y-%m-%d'
ae_df['date'] =  pd.to_datetime(ae_df['date'], format=format_str)
# ae_df['overnight_range']=False
# time_filter=(ae_df['int_seconds']>=0) & (ae_df['int_seconds']<=28800)
# businessday_filter=ae_df['is_business_day']
# mp_filter=time_filter&businessday_filter


mp_filter=mp_filter_fn(df=ae_df, start_int_seconds=0, end_int_seconds=28800)
ae_df['overnight_range']=mp_filter
days = days_fn(ae_df,mp_filter)
for day in days:
   index=days.index(day)
   print('Doing day = {day} and index = {index}...'.format(index=index, day=day))
   ae_df=trade_range_fn(ae_df, day)




