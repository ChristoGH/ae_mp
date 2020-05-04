#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:07:01 2020

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
MP_DUKA_DATETIME_FORMAT='%d.%m.%Y %H:%M:%S.%f'

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

loadfilename = 'data/alldata_wrangled'
tick_symbol='USD/ZAR'
data=pd.read_csv(loadfilename+'.csv')

# We create 60x24x5 rolling images of the candle data,
# H,L,C,ny_timestamp_int_seconds, universaldate
list(data)
data=data[data.is_business_day].copy()

#%%

# lets create the high (60x24) colour layer:
# take 1440 highs:
h=data.high[0:1440].values
np_h=np.reshape(h, (60, 24))
np.log(np_h/np_h[0][0])

x=np.arange(0,1440,1)
np.reshape(x, (60, 24))
#%%
def discrete_delta_array_fn(price_array, delta):
   return np.round(price_array/(delta),0)-int(np.round(price_array[0]/(delta),0))

def discrete_price_array_fn(price_array, delta):
   return np.round(price_array/(delta),0)

def return_array_fn(price_array):
   return np.log(price_array/price_array[0])

def price_layer_fn(xarray, x, y, delta, significant_figs):
   price_array=digital_fn(xarray, delta, significant_figs)
   discrete_price_array=discrete_price_array_fn(price_array, delta)
   return_array=return_array_fn(discrete_price_array)
   layer=np.reshape(return_array,(x,y))
   return layer

#%%
hd_array=digital_fn(xarray, delta, significant_figs)
hd_discrete_array=np.round(hd_array/(delta),0)-int(np.round(hd_array[0]/(delta),0))
hd_layer=np.reshape(hd_discrete_array,(x,y))

significant_figs=5
delta=0.00015
depth=60
width=24
price_array=data.high[0:depth*width].values
price_array=discrete_price_array_fn(price_array, delta)
discrete_price_array=discrete_price_array_fn(price_array, delta)
return_array=return_array_fn(discrete_price_array)

x=np.arange(0,1440,1)
h_panel=price_layer_fn(data.high[range(1440)].values, depth, width, delta, significant_figs)
range(1440)
data.iloc(list(x))

h_panel=price_layer_fn(data.high[0:depth*width].values, depth, width, delta, significant_figs)
l_panel=price_layer_fn(data.low[0:depth*width].values, depth, width, delta, significant_figs)
c_panel=price_layer_fn(data.close[0:depth*width].values, depth, width, delta, significant_figs)

np.array([h_panel,l_panel, c_panel])
