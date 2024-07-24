#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 00:22:30 2024

@author: nascimento
"""
import pandas as pd 
from datetime import datetime
from BMF import real, nominal 




date_list = pd.date_range(start = '2005-01-01', end ='2024-04-19') # data range

type(date_list)

teste = real(pd.to_datetime('2024-07-01'))

date_list = pd.date_range(start = '2005-01-01', end ='2024-04-19') # data range

df_real = []

for dt in date_list: # request data and create data frame 
    
    print(dt)
    
    real_rate = real(dt) # request data based on date (dt)
    
    if(type(real_rate) != type(None)):

        real_rate = pd.pivot_table(real_rate, values = 'bd252', index = 'Date', columns = ['TenorsDays']).sort_values(by = 'Date') # format new data with pivot table
        df_real = real_rate if not len(df_real) else pd.concat([df_real, real_rate]) # concat new data to the data frame 
        
df_real.columns = df_real.columns.astype('float64') # format columns 
df_real.index = df_real.index.astype('datetime64[ns]') # format index (rows)

df_real = df_real.reindex(columns=sorted(list(df_real.columns))) # sort columns by tenure 

date_list = pd.date_range(start = '2005-01-01', end ='2024-04-19') # data range

df_nominal = []

for dt in date_list: # request data and create data frame 
    
    print(dt)
    
    nominal_rate = nominal(dt) # request data based on date (dt)
    
    if(type(nominal_rate) != type(None)):

        nominal_rate = pd.pivot_table(nominal_rate, values = 'bd252', index = 'Date', columns = ['TenorsDays']).sort_values(by = 'Date') # format new data with pivot table
        df_nominal = nominal_rate if not len(df_nominal) else pd.concat([df_nominal, nominal_rate]) # concat new data to the data frame 
        
df_nominal.columns = df_nominal.columns.astype('float64') # format columns 
df_nominal.index = df_nominal.index.astype('datetime64[ns]') # format index (rows)

df_nominal = df_nominal.reindex(columns=sorted(list(df_nominal.columns))) # sort columns by tenure 