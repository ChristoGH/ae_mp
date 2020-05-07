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
from dl_dataprep_lib import significant_figs,delta,depth,width
from dl_dataprep_lib import price_layer_fn,discrete_price_array_fn,return_array_fn
from dl_dataprep_lib import digital_fn
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

price_array=data.high[0:depth*width].values
price_array=discrete_price_array_fn(price_array, delta)
discrete_price_array=discrete_price_array_fn(price_array, delta)
return_array=return_array_fn(discrete_price_array)


h_panel=price_layer_fn(data.high[0:depth*width].values, depth, width, delta, significant_figs)
l_panel=price_layer_fn(data.low[0:depth*width].values, depth, width, delta, significant_figs)
c_panel=price_layer_fn(data.close[0:depth*width].values, depth, width, delta, significant_figs)

np.array([h_panel,l_panel, c_panel])
