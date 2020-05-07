#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 06:11:36 2020

@author: Christo Strydom
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 07:08:08 2020

@author: Christo Strydom
"""

import pandas as pd
import numpy as np
import calendar
import datetime as datetime
from datetime import datetime as dt
from pandas import Timestamp
from pandas.tseries.offsets import BDay
import time
# MP_DUKA_DATETIME_FORMAT='%d.%m.%Y %H:%M:%S.%f'

#%%
def stoploss_fn(exit_price, exit_low,entry_price,entry_low):
   stop_loss0=exit_price<entry_price      
   stop_loss1=exit_low<entry_price
   stop_loss2=exit_low<entry_low        
   return stop_loss0,stop_loss1,stop_loss2

def mtm_fn(max_mtm, exit_price, entry_price):
   mtm=exit_price-entry_price
   max_mtm=max(max_mtm,mtm)   
   return mtm, max_mtm

def stop_fn(count,in_bounds,stop_loss0,stop_loss1,stop_loss2):
   stop_iter=False
   stop_ind=-1
   if stop_loss0:
      stop_iter=True
      stop_ind=0
      print('-stop_loss0: mtm<0-----------------------')
   if (count>1)&(stop_loss1):
      stop_iter=True
      stop_ind=1
      print('-stop_loss1: current low<entry price--------------------------')
   if (stop_loss2):
      stop_iter=True
      stop_ind=2
      print('-stop_loss2: current low<entry low--------------------------')         
   if (not in_bounds):
      stop_iter=True
      print('-out of bounds----------------------')
   return stop_iter,stop_ind
   
      
   
   