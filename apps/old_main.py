# %%# Setup folder
import os


def folder():
    folder_name = 'Codes'
    for root, dirs, files in os.walk(os.getcwd()):
        if folder_name in dirs:
            new_path = os.path.join(root, folder_name)
            os.chdir(new_path)


folder()
# %%# Libraries

from apps.database.bcb import bcb

bcb_download = bcb().bcb_download
bcb_load = bcb().bcb_load
bcb_download_thread = bcb().bcb_download_thread

# %%# Functions sandbox

"""
df_real_hist = pd.read_csv(r'./Data/ipca.csv',index_col = 0)
df_nominal_hist = pd.read_csv(r'./Data/pre.csv', index_col = 0)

df = nominal('2024-01-01', '2024-02-15')

dim_plot(df, start_date = None, end_date = None, lim = [8, 14])

flat_plot(df, ['2024-01-02', '2024-01-03', '2024-02-02'], ['markers', 'markers', 'lines+markers'])

df_list_bcb = bcb_download_thread()

df_selic_reuniao, df_pib_trimestral, df_ipca_12, df_selic_anual, df_pib_anual, df_usd_anual, df_ipca_anual, df_ipca_mensal, df_usd_mensal = bcb_load()

"""
