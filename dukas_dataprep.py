#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 12:17:33 2020

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
from fxcm_timezone_lib import london_timestamp, ny_timestamp, jhb_timestamp
#from datetime import datetime
import sys
import time
MP_DUKA_DATETIME_FORMAT='%d.%m.%Y %H:%M:%S.%f'

#%%

def universaldf_fn():
   universaldf=pd.DataFrame()
   universaldf['day']=range(1,36)
   universaldf['weekday']=[6,0,1,2,3,4,5] * 5
   universaldf['weekno']=np.repeat([1,2,3,4,5],7)
   return universaldf

def is_business_day(date):
    return bool(len(pd.bdate_range(date, date)))

def second_fn(df):
   # df=fxcm_df.copy()
        y_list=list(df['date'])
        z_list=list(df['timestamp'])
        # z_list=df['timestamp'][0] - datetime.timestamp(datetime(y.year,y.month,y.day))
        # [df['timestamp'] - datetime.timestamp(datetime(y.year,y.month,y.day)) for y in df['date']]
        x_list=[]
        # c=5*60
        for y,z in zip(y_list,z_list):
           # y=y_list[0]
           # z=z_list[0]
           s=z-Timestamp(datetime.datetime(y.year,y.month,y.day))
           x_list.append(s.seconds)
        return x_list
     
def ymd_fn(myDate): return myDate.year,myDate.month,myDate.day

def num_days_fn(year, month):return calendar.monthrange(year, month)[1]

def dayslist_fn(year, month, day):
   num_days = num_days_fn(year, month)
   return [datetime.datetime(year, month, day) for day in range(1, num_days+1)]

def weekdaylist_fn(dayslist):return [i.weekday() for i in dayslist]

def weekth_fn(day):
   l = list(np.repeat([1,2,3,4,5],7))
   return l[day-1]

def weekday_fn(dayslist,day):
   weekdaylist=weekdaylist_fn(dayslist)
   return weekdaylist[day-1] 

def universaldate_fn(universaldf,myDate):
    #     This function categorizes a date.  weekday is the standard day of the week count,
#     1 being Sunday and 6 Friday.  weekth is the week count, the two numbers give the first sunday of the Month for instance
#     daycat(datetime(2018,5,4)) (6, 1, 5). It is the first(1) Friday(=6) of the month(5). 
#     This uses the concept of a universal month.  What about a universal year?  A universal year always has the first Sunday
#       numbered 1 all days are incremented from there onwards.  Day number 32 or February 1 will always be a Wednesday!
#     In this way , 1 January 2018 a Monday is number 2 in the universal year format.  Why bother with a universal what what?
#     Just as a Monday (the second day of the week) carries a different dimension to a Friday the 6th days of the week,
#     the first Monday may carry a different meaning to shopping behaviour to second Monday vs the third Monday etc.
#     It makes it 'easier' for a classifiction algorithm to disect the data.  A universal year may be of less importance
#     next to the other number but its importance will be shown by the data!
    # l=[]
    year, month, day =ymd_fn(myDate)
    weekth=weekth_fn(day)    
#   Find number of days in this month:
    # num_days = num_days_fn(year, month)
#   create a days list for this month:
    dayslist = dayslist_fn(year, month, day)
    # udayslist = [datetime(2017, 1, 1) for day in range(1, num_days+1)]
#   create a weekdaylist (day of week) for this month
    # weekdaylist = weekdaylist_fn(dayslist)

    # weekth = l[day-1]
    #     print(len(weekdaylist),day,myDate, num_days)
    weekday = weekday_fn(dayslist, day)
#   Ammended as follows: --------------------------------------------------------------------------------------------
    m1=universaldf['weekno']==weekth
    m2=universaldf['weekday']==weekday
    universaldate=universaldf[m1&m2]['day'].iloc[0]
#     universaldate = (weekth-1)*7+weekday
#   --------------------------------------------------------------------------------------------------------------------   
    # dayname = calendar.day_name[myDate.weekday()]
    return(universaldate)

def df_all_fn(df1, df2):
#   common = df1.merge(df2.drop_duplicates(),right_index=True,left_index=True)
#   df_all = df1.merge(df2.drop_duplicates(), on=['col1','col2'], 
#                      how='left', indicator=True)
   try:
      df_all=df1.merge(df2,right_index=True,how='right', left_index=True, indicator=True)
   except:
      logging.error('This error occurred in df_all_fn:{e}'.format(e=sys.exc_info()[0]))            
   return df_all

def df_merge_fn(df_all):
   try:
      df_all['_merge'] == 'right_only'
      bool_list = [i for i, x in enumerate(list(df_all['_merge']=='right_only')) if x]
      add_new=len(bool_list)>0
   except:
      logging.error('This error occurred in df_merge_fn:{e}'.format(e=sys.exc_info()[0]))            
   return df_all, add_new

def standard_list_fn(): return list(range(0,24*60*60,30*60))

def fxcm_mean_OHLC_fn(df, mean_str, str_1, str_2):
   df[mean_str]=(df[str_1]+df[str_2])/2
   return df

def fxcm_candles_OHLC(df):
   df=fxcm_mean_OHLC_fn(df, 'open', 'bidopen', 'askopen')
   df=fxcm_mean_OHLC_fn(df, 'high', 'bidhigh', 'askhigh')   
   df=fxcm_mean_OHLC_fn(df, 'low', 'bidlow', 'asklow')
   df=fxcm_mean_OHLC_fn(df, 'close', 'bidclose', 'askclose')
   return df     
   # fxcm_df['open'] =  (fxcm_df['bidopen'] + fxcm_df['askopen'])/2
   # fxcm_df['high'] =  (fxcm_df['bidhigh'] + fxcm_df['askhigh'])/2
   # fxcm_df['low'] =  (fxcm_df['bidlow'] + fxcm_df['asklow'])/2
   # fxcm_df['close'] =  (fxcm_df['bidclose'] + fxcm_df['askclose'])/2
   
def datetime_fxcm_df(df, format_str):
   # print('2. create datetime column...')
        print('2. create datetime column...')
        df['datetime'] =  pd.to_datetime(df.date, format=format_str)
        # df.drop(labels=['date'], axis=1,inplace=True)
        return df

def period_f():return lambda x: x.strftime('%Y%m')

def dom_f():return lambda x: x.strftime('%-d')

def awdn_f():return lambda x: x.strftime('%a')

def month_f():return lambda x: x.strftime('%-m')

def doy_f():return lambda x: x.strftime('%j')

def f_fn(f_str):
   return lambda x: x.strftime(f_str)

def column_fn(df, target_column_str, from_column_str, f_str):
   # print('3. create period column...')
   f=f_fn(f_str=f_str)
   df[target_column_str] = df[from_column_str].apply(f) #insert a period value in the shape of 'yyyymm'
   return df

def period_column_fn(df):
   print('3. create period column...')
   f=f_fn(f_str='%Y%m')
   df['period'] = df['datetime'].apply(f) #insert a period value in the shape of 'yyyymm'
   return df
     
def fxcm_dom_fn(df):
   print('4. create dom column...')
   f=f_fn(f_str='%-d')
   df['dom'] = df['datetime'].apply(f) # day of month
   return df
    
def fxcm_awdn_fn(df):
   print('5. create awdn column...')
   f=awdn_f()
   f=f_fn(f_str='%a')   
   df['awdn'] = df['datetime'].apply(f) # abbreviated week day name
   return df

def fxcm_month_fn(df):
   print('6. create month column...')
   f=month_f()
   df['month'] = df['datetime'].apply(f) # month name

def fxcm_doy_fn(df):
   print('7. create dy column...')
   df['doy'] = df['datetime'].apply(lambda x: x.strftime('%j')) # day-of-the-year
   
def date_f(): return lambda x: x.date()

def fxcm_date_fn(df):
   print('create date column...')
   f=date_f()
   df['date'] = df['datetime'].apply(f) # day-of-the-year
   return df
   
def time_f(): return lambda x: Timestamp(x)

def fxcm_timestamp_fn(df):
   print('create timestamp column...')
   f=time_f()
   df['timestamp'] = df['datetime'].apply(f) # day-of-the-year
   return df

def int_seconds_fn(df):
   # df=fxcm_df.copy()
   second_list=second_fn(df)
   print('create int_seconds column...')            
   df['int_seconds'] = second_list
   return df

def mp_period_fn(df):
   print('create mp_period column...')
   standard_list = standard_list_fn()
   df['mp_period'] = [standard_list.index(i) for i in df['int_seconds']]
   return df

def universal_f(): return lambda x: universaldate_fn(x)

def universaldate_column_fn(df):
   print('17. create universaldate column...')
   # df['mp_period'] = [standard_list.index(i) for i in df['int_seconds']]
   f=universal_f()
   df['universaldate'] = df['date'].apply(f)
   return df

def is_business_day_f():return lambda x: is_business_day(x)
        
def is_business_day_fn(df):
   print('create boolean business day column:')
   f=is_business_day_f()
   df['is_business_day'] = df['date'].apply(f)
   return df

def previous_business_day_f(ndays):return lambda x: x - BDay(ndays)

def previous_business_day_fn(df,column_header,ndays):
   print('create {ndays} previous business day column:'.format(ndays=ndays))
   f=previous_business_day_f(ndays)
   df[column_header] = df['date'].apply(f)
   return df


def weekday_f():return lambda x: x.weekday()

def weekday_column_fn(df):
   print('create the weekday column:')
   f=weekday_f()
   df['weekday'] = df['date'].apply(f)
   # df[column_header] = df['date'].apply(f)
   return df

def ud_df(gf):
   universaldf=universaldf_fn()
   datelist=list(set(gf['date']))
   udlist=[universaldate_fn(universaldf=universaldf, myDate=d) for d in datelist]
   for d, u  in zip(datelist, udlist):
        print(d, u)
        gf.loc[gf['date']==d,'universaldate']=u
   return gf

def timestamp_intseconds_fn(df, timestamp_field):
   x=df[timestamp_field][0]
   seconds_f= lambda x:(time.mktime(x.timetuple())-time.mktime(datetime.datetime(x.year,x.month,x.day).timetuple()))
   df[timestamp_field+'_int_seconds']=df[timestamp_field].apply(seconds_f)
   return df

#%%
   
   
def fdict_fn():
   return {'period_f':'%Y%m',
    'dom_f':'%-d',
    'awdn_f':'%a',
    'month_f':'%-m',
    'doy_f':'%j',
    'wny':'%U'}

def eximia_wrangle_fn(fxcm_df):
   # fxcm_df=data.copy()
   fxcm_df.reset_index(inplace=True)
   MP_FXCM_DATETIME_FORMAT='%Y-%m-%d %H:%M:%S'
   fdict=fdict_fn()
   fxcm_df=fxcm_candles_OHLC(fxcm_df)
   fxcm_df=datetime_fxcm_df(df=fxcm_df, format_str=MP_FXCM_DATETIME_FORMAT)
   fxcm_df=column_fn(df=fxcm_df, target_column_str='period', from_column_str='datetime', f_str=fdict['period_f'])
   fxcm_df=column_fn(df=fxcm_df, target_column_str='dom', from_column_str='datetime', f_str=fdict['dom_f'])
   fxcm_df=column_fn(df=fxcm_df, target_column_str='awdn', from_column_str='datetime', f_str=fdict['awdn_f'])
   fxcm_df=column_fn(df=fxcm_df, target_column_str='month', from_column_str='datetime', f_str=fdict['month_f'])
   fxcm_df=column_fn(df=fxcm_df, target_column_str='doy', from_column_str='datetime', f_str=fdict['doy_f'])
   fxcm_df=column_fn(df=fxcm_df, target_column_str='wny', from_column_str='datetime', f_str=fdict['wny'])
   fxcm_df=fxcm_date_fn(fxcm_df)
   fxcm_df=fxcm_timestamp_fn(fxcm_df)
   fxcm_df=ny_timestamp(fxcm_df)
   fxcm_df=london_timestamp(fxcm_df)
   fxcm_df=jhb_timestamp(fxcm_df)
   fxcm_df=timestamp_intseconds_fn(df=fxcm_df.copy(), timestamp_field='timestamp')
   fxcm_df=timestamp_intseconds_fn(df=fxcm_df.copy(), timestamp_field='ny_timestamp')
   fxcm_df=timestamp_intseconds_fn(df=fxcm_df.copy(), timestamp_field='london_timestamp')
   fxcm_df=timestamp_intseconds_fn(df=fxcm_df.copy(), timestamp_field='jhb_timestamp')
   fxcm_df=int_seconds_fn(fxcm_df)
   # fxcm_df=mp_period_fn(fxcm_df)
   # fxcm_df=universaldate_column_fn(fxcm_df)
   fxcm_df=ud_df(fxcm_df)
   fxcm_df=is_business_day_fn(fxcm_df)
   fxcm_df=previous_business_day_fn(df=fxcm_df,column_header='previous_business_day',ndays=1)
   fxcm_df=previous_business_day_fn(df=fxcm_df,column_header='five_previous_business_day',ndays=5)
   fxcm_df.set_index('datetime', inplace=True)
   return fxcm_df

def get_candle_history(tick_symbol, filename):
   candles_df=pd.DataFrame()
   try:
      candles_df = pd.read_csv(filepath_or_buffer=filename)
      candles_df.drop_duplicates(inplace=True)
      # candles_df.set_index('date')
      # candles_df.sort_values(by='date')
      candles_df.set_index('datetime', inplace=True)
      # store.close()
   except IOError:
      print("File not accessible")
      logging.error('This error occurred in get_candle_history:{e}'.format(e=sys.exc_info()[0]))      
   return candles_df

def append_candles_fn(old_candles_df, new_candles_df):
   try:
      appended_candles_df=old_candles_df.copy()   
      if not new_candles_df.empty:
         new_candles_df.drop_duplicates(inplace=True)
         # new_candles_df.sort_index(inplace=True)   
         # df_all=df_all_fn(df1=old_candles_df, df2=new_candles_df)
         df,add_new=df_merge_fn(df_all_fn(df1=old_candles_df, df2=new_candles_df))
         new_index=df[list(df['_merge']=='right_only')].index
         new_candles_bool=new_candles_df.index.isin(new_index)
         if add_new:
            appended_candles_df=appended_candles_df.append(new_candles_df[new_candles_bool])
         # appended_candles_df.drop(['_merge'], inplace=True, axis=1)    
         # else:
         #    appended_candles_df=candles_df.copy()
   except:
#      e = sys.exc_info()[0]
      logging.error('This error occurred in candles_fn:{e}'.format(e=sys.exc_info()[0]))
   return appended_candles_df
   

def save_candles_fn(tick_symbol, filename, new_candles):
#   store = pd.HDFStore(filename)
   try:
      # new_candles.to_csv(path_or_buf=filename, 
      #                key='test', 
      #                complevel=9,
      #                format='table',
      #                mode='a')
      new_candles.to_csv(path_or_buf=filename)

      
                     # format='table', 
                     # append=True) # append=True)
   except: 
      logging.error('This error occurred in save_candles_fn:{e}'.format(e=sys.exc_info()[0]))
   return
   
#
##%%
#print('set tick symbol:')
#tick_symbol='USD/ZAR'
#print('connect to fxcm:')
#con = fxcmpy.fxcmpy(config_file='/home/lnr-ai/github_repos/fxcm/config/fxcm.cfg', server='demo')
#print('collect candles:')
#m30_df = con.get_candles(tick_symbol, period='m30', number=250)
#print('unsubscribe:')
#con.unsubscribe_market_data(tick_symbol)
#
#common = m30_df.merge(candles_df,right_index=True,left_index=True)
#print(common)
#new_df=m30_df[(~m30_df.index.isin(common.index))&(~m30_df.index.isin(common.index))]

def duka_tick_prep_fn(dukas_df):
   dukas_df['date'] =  pd.to_datetime(dukas_df['Gmt time'], format=MP_DUKA_DATETIME_FORMAT)
   dukas_df['bidopen']=dukas_df['Open']
   dukas_df['bidclose']=dukas_df['Close']
   dukas_df['bidhigh']=dukas_df['High']
   dukas_df['bidlow']=dukas_df['Low']
   dukas_df['askopen']=dukas_df['Open']
   dukas_df['askclose']=dukas_df['Close']
   dukas_df['askhigh']=dukas_df['High']
   dukas_df['asklow']=dukas_df['Low']
   dukas_df['tickqty']=dukas_df['Volume']
   dukas_df.set_index('date', inplace=True)
   return dukas_df

#%%

def significant_price_fn(price_range, significant_figs):
   return [int(np.round((p*10**significant_figs))) for p in price_range]

def unique_price_range_fn(unique_price_list, significant_figs):
   return [np.round(u/(10**(significant_figs)),significant_figs) for u in unique]

def digital_price_range_fn(price_range, significant_figs):
   pl=significant_price_fn(price_range, significant_figs)
   (upl, count_list) = np.unique(pl, return_counts=True)
   unique_price_list=unique_price_range_fn(upl, significant_figs)
   return unique_price_list, count_list

def digital_fn(x, delta, significant_figs):
   # this function digitizes a single price:
   return np.round(np.floor(x/delta)*delta,significant_figs)

def make_tickbins_fn(delta, high, low, significant_figs):
   # This function is used at every bar, using only the high and low,
   # and the output to be appended
   # to a previous result to arrive at a raw (cumulative) result of 
   # digitzed prices,
   # based on delta and significant_figs
   l=digital_fn(low, delta, significant_figs)
   h=digital_fn(high, delta, significant_figs)
   return np.arange(l,h,delta)

#%%
eximia_candles_filename = 'data/USDZAR_Candlestick_5_M_BID_01.01.2019-08.02.2020'
tick_symbol='USD/ZAR'
data=pd.read_csv(eximia_candles_filename+'.csv')
#%%
eximia_candles_filename_merge = 'data/USDZAR_Candlestick_5_M_BID_08.02.2020-20.04.2020'
tick_symbol='USD/ZAR'
data_merge=pd.read_csv(eximia_candles_filename_merge+'.csv')
#%%
set(list(data))-set(list(data_merge))
# data_merge.set_index('Gmt time',inplace=True)
# data.set_index('Gmt time',inplace=True)
print(data.shape,' and ', data_merge.shape)
# df=data.merge(data_merge, left_index=True, right_index=True, how='inner')
df=data.append(data_merge)
np.where(df.duplicated())
df.drop_duplicates(inplace=True)
print(len(list(data.index)),len(list(set(data.index))))
#%%
data=duka_tick_prep_fn(df)
eximia_df=eximia_wrangle_fn(data)
savefilename='data/alldata'
eximia_df.to_csv(savefilename+'_wrangled'+ '.csv')

#%%
significant_figs=5
nominal=10**(significant_figs)
delta=0.00015
low=14.31091
high=14.72770
# delta=int(0.00015*10**5)
# low=int(14.31091*10**5)
# high=int(14.72770*10**5)
# lowi=int(np.round(np.floor(low/delta)*delta))
# highi=int(np.round(np.floor(high/delta)*delta))
# (highi-lowi)*delta
# nominal=10**significant_figs
d=int(delta*nominal)
# l=int(low/nominal)
# h=int(high/nominal)
l=digital_fn(low, delta, significant_figs)
h=digital_fn(high, delta, significant_figs)
np.arange(l,h,delta)

significant_figs=5
delta=0.00015
low=14.72494
high=14.72770
price_range=[]
pr=make_tickbins_fn(delta, high, low, significant_figs)
price_range=np.append(price_range,pr)
# significant_figs=5
# delta=0.00015
low=14.72704
high=14.72770
pr=make_tickbins_fn(delta, high, low, significant_figs)
price_range=np.append(price_range,pr)

low=14.72760
high=14.72808
pr=make_tickbins_fn(delta, high, low, significant_figs)
price_range=np.append(price_range,pr)

low=14.72721
high=14.72769
pr=make_tickbins_fn(delta, high, low, significant_figs)
price_range=np.append(price_range,pr)



digital_price_range_fn(price_range, significant_figs)

#%%

# def price_range_fn(pricelist, high, low, significant_figs):
#    l=digital_fn(low, delta, significant_figs)
#    h=digital_fn(high, delta, significant_figs)
#    return np.arange(l,h,delta)

#%%
loadfilename = 'data/alldata_wrangled'
tick_symbol='USD/ZAR'
data=pd.read_csv(loadfilename+'.csv')
#%%
make_tick_fn(delta, high, low, nominal)
np.arange(lowi,highi,delta)
