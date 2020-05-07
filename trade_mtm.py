#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 07:08:08 2020

@author: Christo Strydom
"""



# import fxcmpy
import sys
sys.path.append("/home/lnr-ai/github_repos/fxcm/")
import os
os.chdir('/home/lnr-ai/github_repos/eximia/')
os.chdir('/media/lnr-ai/christo/github_repos/ae_mp/')
import pandas as pd
import logging
import numpy as np
import calendar
import datetime as datetime
from datetime import datetime as dt
from pandas import Timestamp
from pandas.tseries.offsets import BDay
# from fxcm_timezone_lib import london_timestamp, ny_timestamp, jhb_timestamp
#from datetime import datetime
import sys
import time
from dl_dataprep_lib import digital_fn
from trade_mtm_lib import stoploss_fn, mtm_fn, stop_fn
MP_DUKA_DATETIME_FORMAT='%d.%m.%Y %H:%M:%S.%f'
#%%
loadfilename = 'data/alldata_wrangled'
tick_symbol='USD/ZAR'
ae_df=pd.read_csv(loadfilename+'.csv')
#%%
ae_df.columns
# Index(['datetime', 'date', 'Gmt time', 'Open', 'High', 'Low', 'Close',
#        'Volume', 'bidopen', 'bidclose', 'bidhigh', 'bidlow', 'askopen',
#        'askclose', 'askhigh', 'asklow', 'tickqty', 'open', 'high', 'low',
#        'close', 'period', 'dom', 'awdn', 'month', 'doy', 'wny', 'timestamp',
#        'ny_timestamp', 'london_timestamp', 'jhb_timestamp',
#        'timestamp_int_seconds', 'ny_timestamp_int_seconds',
#        'london_timestamp_int_seconds', 'jhb_timestamp_int_seconds',
#        'int_seconds', 'universaldate', 'is_business_day',
#        'previous_business_day', 'five_previous_business_day'],
#       dtype='object')
def digitize_candle(high,low,close):
   return digital_fn(high), digital_fn(low), digital_fn(close)

#%%
df=ae_df[2000:2121].copy()
for entry_index, (df_index, entry_datetime, entry_high,entry_low,entry_price) in enumerate(zip(df.index, df['datetime'], df['high'], df['low'], df['close'])):
   entry_high,entry_low,entry_price=digitize_candle(entry_high,entry_low,entry_price)
   print(entry_index, df_index)
   count=0
   index=entry_index
   in_bounds=(index+2)<df.shape[0]   
   current_price=entry_price
   stop_iter=False
   max_mtm=0
   stop_loss0=False #the CURRENT candle close does not fall below the ORIGINAL 
   # candle close, ie mtm does not go < 0
   stop_loss1=False #the CURRENT candle low does not fall below the ORIGINAL 
   # candle low 
   stop_loss2=False #the CURRENT candle low does not fall below the ORIGINAL 
   # entry price
   # in_bounds=True
   while (in_bounds&(not stop_iter)):
      count+=1
      index+=1
      in_bounds=(index+2)<df.shape[0]
      print(in_bounds, in_bounds&(not stop_iter), stop_iter,index+2, df.shape[0])
      current_price=df.iloc[index].close
      current_high=df.iloc[index].high
      current_low=df.iloc[index].low
      current_datetime=df.iloc[index].datetime
      # mtm=current_price-entry_price
      # max_mtm=max(max_mtm,mtm)
      mtm, max_mtm=mtm_fn(max_mtm, current_price, entry_price)
      stop_loss0,stop_loss1,stop_loss2=stoploss_fn(current_price,current_low,entry_price,entry_low)
      # stop_loss0=current_price<entry_price      
      # stop_loss1=current_low<entry_price
      # stop_loss2=current_low<entry_low      
      print(df_index, entry_index, index, count, entry_datetime, current_datetime, entry_price,current_price,mtm,max_mtm) 
      # if stop_loss0:
      #    stop=True
      #    print('-stop_loss0: mtm<0-----------------------')
      # if (count>1)&(stop_loss1):
      #    stop=True
      #    print('-stop_loss1: current low<entry price--------------------------')
      # if (stop_loss2):
      #    stop=True
      #    print('-stop_loss1: current low<entry low--------------------------')         
      # if (not in_bounds):
      #    # print(in_bounds,not in_bounds)
      #    print('-out of bounds----------------------')
      stop_iter,stop_ind=stop_fn(count,in_bounds,stop_loss0,stop_loss1,stop_loss2)
         
      
      
   
   