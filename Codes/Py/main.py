#%%# Setup folder
import os

def folder():
    folder_name = 'Py'
    for root, dirs, files in os.walk(os.getcwd()):
        if folder_name in dirs:
            new_path = os.path.join(root, folder_name)
            os.chdir(new_path)
        
folder() 
#%%# Libraries

import pandas as pd 
from bmf import real, nominal, update
from visualization import dim_plot, flat_plot  
from bcb import bcb

bcb_update = bcb().bcb_update
bcb_load = bcb().bcb_load
bcb_update_thread = bcb().bcb_update_thread

#%%# Functions sandbox 

# df_real_hist = pd.read_csv(r'./Data/ipca.csv',index_col = 0)
# df_nominal_hist = pd.read_csv(r'./Data/pre.csv', index_col = 0)

df = nominal('2024-01-01', '2024-02-15')

dim_plot(df, start_date = None, end_date = None, lim = [8, 14])

flat_plot(df, ['2024-01-02', '2024-01-03', '2024-02-02'], ['markers', 'markers', 'lines+markers'])

#%%# BCB download 

df_list_bcb = bcb_update()

#%%# BCB load

df_list_bcb = bcb_load()

#%%# NSS 