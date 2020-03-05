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
ae_df['overnight_range']=False
ae_df['overnight_range']=(ae_df['int_seconds']>=0) & (ae_df['int_seconds']<=28800)

days=list(set(ae_df['date'])) 
ae_df['on_low']=0
ae_df['on_high']=0
for day in days:
   index=days.index(day)
   print('Doing day = {day} and index = {index}...'.format(index=index, day=day))
   # day =days[0]
   df=ae_df[ae_df['date']==day].copy()
   on_high=max(df.loc[df['overnight_range'],'high'])
   on_low=min(df.loc[df['overnight_range'],'low'])
   ae_df.loc[ae_df['date']==day, 'on_low']=on_low
   ae_df.loc[ae_df['date']==day, 'on_high']=on_high   

def datetime_fxcm_df(df, format_str):
   # print('2. create datetime column...')
        print('2. create datetime column...')
        df['datetime'] =  pd.to_datetime(df.date, format=format_str)
        # df.drop(labels=['date'], axis=1,inplace=True)
        return df


