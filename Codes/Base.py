#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 19:05:45 2024

@author: nascimento
"""

import pandas as pd 
import numpy as np

path = '/home/nascimento/Documents/USP/Monografia/Data/Raw'

save = [path + '/Di-IPCA',path + '/Di-Pre']

def real(dt):
    url = r'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data=' + dt.strftime('%d/%m/%Y') + '&slcTaxa=DIC'
    html = pd.read_html(url)
    data = None 

    if 'Não há dados para a data fornecida!' not in list(html[1].iloc[0]):
        data_list = [float(taxa) for taxa in list(html[1][0])[0].replace('Dias Corridos DI x IPCA 252(2) ', '').replace('Dias Corridos 252(2) ', '').replace(',', '.').split(' ')]
        n = 0 
        data = []

        while n + 2 < len(data_list):
            data.append(np.array(data_list[n: n + 2]).astype('float64'))
            n += 2
        
        data = pd.DataFrame(data, columns = ['TenorsDays', 'bd252'])
        data['Date'] = [dt for n in range(len(data))]

    return data 

date_list = pd.date_range(start = '2005-01-01', end ='2024-04-19')

df_real = []

for dt in date_list:
    
    print(dt)
    
    real_rate = real(dt)
    
    if(type(real_rate) != type(None)):
        real_rate = pd.pivot_table(real_rate, values = 'bd252', index = 'Date', columns = ['TenorsDays']).sort_values(by = 'Date')
        df_real = real_rate if not len(df_real) else pd.concat([df_real, real_rate])
        
df_real.columns = df_real.columns.astype('float64')

df_real.index = df_real.index.astype('datetime64[ns]')

df_real = df_real.reindex(columns=sorted(list(df_real.columns)))

df_real.to_csv(save[0] + '.csv')


