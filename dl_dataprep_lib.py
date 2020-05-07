#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:07:01 2020

@author: Christo Strydom
"""



# import fxcmpy
# import sys
# sys.path.append("/home/lnr-ai/github_repos/fxcm/")
# import os
# os.chdir('/home/lnr-ai/github_repos/eximia/')
# os.chdir('/media/lnr-ai/christo/github_repos/ae_mp/')
import pandas as pd
import numpy as np
from pandas import Timestamp
from pandas.tseries.offsets import BDay
# from fxcm_timezone_lib import london_timestamp, ny_timestamp, jhb_timestamp
#from datetime import datetime
# import sys
# import time
# MP_DUKA_DATETIME_FORMAT='%d.%m.%Y %H:%M:%S.%f'
significant_figs=5
delta=0.00015
depth=60
width=24
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
