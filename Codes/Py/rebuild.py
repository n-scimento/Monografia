"""
import sys         
sys.path.append('D:/projects/base/app/modules') 

see more at https://realpython.com/python-import/ or https://www.geeksforgeeks.org/python-import-module-outside-directory/
"""


import pandas as pd 
from bmf import real, nominal 

def update():
    df_real_hist = pd.read_csv(r'./Data/ipca.csv', index_col = 0)
    df_nominal_hist = pd.read_csv(r'./Data/pre.csv', index_col = 0)
    
    df_nominal_update = nominal(df_nominal_hist.iloc[-1].name, pd.Timestamp.now().date().strftime('%Y-%m-%d'))
    df_real_update = nominal(df_real_hist.iloc[-1].name, pd.Timestamp.now().date().strftime('%Y-%m-%d'))
    
    df_nominal = df_nominal_update if not len(df_nominal_hist) else pd.concat([df_nominal_hist, df_nominal_update]) # concat new data to the data frame 
    df_real = df_real_update if not len(df_real_hist) else pd.concat([df_real_hist, df_real_update]) # concat new data to the data frame 
    
    df_nominal.to_csv(r'.Data/pre.csv')
    df_real.to_csv(r'.Data/ipca.csv')
    return df_nominal, df_real


##
df_real_hist = pd.read_csv(r'./Data/ipca.csv', index_col = 0)
df_nominal_hist = pd.read_csv(r'./Data/pre.csv', index_col = 0)
##
df_real_hist.columns = df_real_hist.columns.astype('float64') # format columns 
df_real_hist.index = df_real_hist.index.astype('datetime64[ns]') # format index (rows)

df_nominal_hist.columns = df_nominal_hist.columns.astype('float64') # format columns 
df_nominal_hist.index = df_nominal_hist.index.astype('datetime64[ns]') # format index (rows)
##
df_nominal_update = nominal(df_nominal_hist.iloc[-1].name, pd.Timestamp.now().date().strftime('%Y-%m-%d'))
df_real_update = nominal(df_real_hist.iloc[-1].name, pd.Timestamp.now().date().strftime('%Y-%m-%d'))
##
df_nominal = pd.concat([df_nominal_hist, df_nominal_update]).drop_duplicates() # concat new data to the data frame 
df_real = pd.concat([df_real_hist, df_real_update]) # concat new data to the data frame 

## For some reason dates are changing format :/ 
### Database is fine, the problem emerges when getting the new data!!!!! look at the formatting being passed 

pd.DataFrame(df_real.index).to_excel('index_real.xlsx')

df_nominal.to_csv(r'./Data/pre.csv')
df_real.to_csv(r'./Data/ipca.csv')