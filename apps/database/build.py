from apps.database.bmf import BMF
import numpy as np
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
from nelson_siegel_svensson.calibrate import calibrate_ns_ols
from nelson_siegel_svensson.calibrate import betas_nss_ols


import json
import os
import pandas as pd
from apps.interpolation.nss import interpolate
from apps.plots.plot import plot_curve
#
# start_date = '2005-01-01'
# end_date = '2024-12-31'
#
# dus = [True, False]
# rates = ['PRE', 'DIC']

# %%# From Website
# def build_base(rate, du):
#     print(f'\n--------\n{rate} - {du}')
#     path = f'data/bmf/{rate.lower()}/{'du' if du else 'dc'}/'
#     files = os.listdir(path)
#     files = [file for file in files if os.path.isfile(os.path.join(path, file))]
#     dates_stored = [file[:10] for file in files]
#     return BMF(rate=rate, du=du).get_dataframe(start_date=start_date, end_date=end_date, dates_stored=dates_stored)
#
#
# build_base('PRE', True)
# build_base('PRE', False)
# build_base('DIC', True)

# %% Build Dataframe

# def get_df(rate, du):
#     path = f'data/bmf/{rate.lower()}/{'du' if du else 'dc'}/'
#     files = os.listdir(path)
#     files = [file for file in files if os.path.isfile(os.path.join(path, file))]
#
#     dict_to_df = {}
#
#
#     for file in files:
#         with open(path + file, "r") as file:
#             data = json.load(file)
#         key = list(data.keys())[0]
#         print(f'{file} read!')
#         data_parsed = data[key]
#         dict_to_df[key] = dict(sorted(data_parsed.items(), key=lambda x: float(x[0])))
#
#     df = pd.DataFrame(dict_to_df)
#     df.index = df.index.astype(float).astype(int)
#     df = df.sort_index(ascending=True)
#     df = df.dropna(axis=1, how='all')
#     df = df[sorted(df.columns, key=pd.to_datetime)]
#
#     print()
#     return df
#
# df_pre_du = get_df('PRE', True)
# df_pre_du.to_excel('df_pre_du.xlsx')
#
# df_pre_dc = get_df('PRE', False)
# df_pre_dc.to_csv('df_pre_dc.csv')
#
# df_dic_du = get_df('DIC', True)
# df_dic_du.to_csv('df_dic_du.csv')

# df_name = f'data/bmf/df_{rate.lower()}_{'du' if du else 'dc'}.xlsx'
# df.to_excel(df_name)


# dfs = ['data/bmf/df_pre_du.csv', 'data/bmf/df_pre_dc.csv', 'data/bmf/df_dic_du.csv']

def read_json(date, rate, du):

    root_path = f"data/bmf/{rate}/{du}/"
    file_path = f"{date}_{rate}_{du}.json"

    with open(root_path + file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = data[date]
    data = {int(float(k)): v for k, v in sorted(data.items(), key=lambda item: int(float(item[0])))}

    t = np.array([int(float(k)) for k in data.keys()])
    y = np.array(list(data.values()))
    #
    # print(f'{date} | {rate} | {du} Maturity: {t}')
    # print(f'{date} | {rate} | {du} Yield: {y}')
    return data, t, y


def fit_yield(rate, du):
    yield_parameters = {}

    path = f'data/bmf/{rate.lower()}/{du}/'
    files = os.listdir(path)
    files = [file for file in files if os.path.isfile(os.path.join(path, file))]
    dates = [date[:10] for date in files]

    for date, file in zip(dates, files):
        data, t, y = read_json(date, rate, du)
        try:
            curve, status = calibrate_nss_ols(t=t, y=y)
        except Exception as e:
            print(f'\n\n{date} | {rate} | {du}: {e}\n\n')
            curve = None

        if curve:
            plot_curve(curve, y, t, output_name=f'{date}_nss_{rate}_{du}', date=date, rate=rate)

            params = {
                'b0': float(curve.beta0),
                'b1': float(curve.beta1),
                'b2': float(curve.beta2),
                # 'b3': float(curve.beta3),
                'tau': float(curve.tau),
                # 't2': float(curve.tau2),
            }
            yield_parameters[date] = params

            root_path = f"data/yield/{rate}/{du}/"
            file_path = f"{date}_{rate}_{du}.json"

            #
            # with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
            #     json.dump(params, json_file, ensure_ascii=False, indent=4)
            #     print(f'Saved at: {(root_path + file_path).lower()}')

            print(f' - {date}: done!')

    root_path = f"data/yield/"
    file_path = f"{rate}_{du}.json"

    with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
        json.dump(yield_parameters, json_file, ensure_ascii=False, indent=4)
        print(f'Saved at: {(root_path + file_path).lower()}')

    return yield_parameters

yield_1 = fit_yield('pre', 'du')
# yield_2 = fit_yield('pre', 'dc')
# yield_3 = fit_yield('dic', 'du')
# #
# # def fit_yield(df):
#
#     name = df
#     print(f'\n\n--------------------\n{name}')
#     rate = name.split('/')[2].split('_')[1]
#     du = name.split('/')[2].split('_')[2][:2]
#
#     df = pd.read_csv(df)
#
#     for date in df.columns:
#
#         print(f'- {date}: starting')
#
#         curve, status = calibrate_nss_ols(t=t, y=y)
#
#         if curve:
#
#             plot_curve(curve, y, t, output_name=f'{date}_{rate}_{du}', date=date, rate =rate)
#
#             params = {
#                 'b0': float(curve.beta0),
#                 'b1': float(curve.beta1),
#                 'b2': float(curve.beta2),
#                 'b3': float(curve.beta3),
#                 't1': float(curve.tau1),
#                 't2': float(curve.tau2),
#             }
#             yield_parameters[date] = params
#
#             root_path = f"data/yield/{rate}/{du}/"
#             file_path = f"{date}_{rate}_{du}.json"
#
#             with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
#                 json.dump(params, json_file, ensure_ascii=False, indent=4)
#                 print(f'Saved at: {(root_path + file_path).lower()}')
#
#             print(f' - {date}: done!')
#
#     root_path = f"data/yield/"
#     file_path = f"{rate}_{du}.json"
#
#     with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
#         json.dump(yield_parameters, json_file, ensure_ascii=False, indent=4)
#         print(f'Saved at: {(root_path + file_path).lower()}')
#
#     return yield_parameters
# #
# # yield_3 = fit_yield('data/bmf/df_dic_du.csv')
# # del yield_3


# del yield_1
# yield_2 = fit_yield('data/bmf/df_pre_dc.csv')
# del yield_2


#%%#

#
# name = 'data/bmf/df_pre_du.csv'
# print(f'\n\n--------------------\n{name}')
# rate = name.split('/')[2].split('_')[1]
# du = name.split('/')[2].split('_')[2][:2]
#
#
# from nelson_siegel_svensson.calibrate import betas_nss_ols
# df = pd.read_csv(name)
# df_backup = df
#
# data = df
# date = '2005-02-03'
#
# df = data.loc[:, 'maturity', date]
#
# df = df.dropna(how='all')
# df = df.loc[df['maturity'] <= 3600]
# # df = df.loc[df.index > 15]
# df = df[df != 0.0]
# t = np.array(df.index)
# y = np.array(df)
#
# # curve, status = betas_nss_ols(t=t, y=y, tau=(-5, 5))
# curve, status = calibrate_nss_ols(t=t, y=y)
#
#
#

path_bmf = f'data/bmf/pre/du/'
files_bmf = os.listdir(path_bmf)
files_bmf = [file for file in files_bmf if os.path.isfile(os.path.join(path_bmf, file))]
dates_bmf = [file[:10] for file in files_bmf]

path_yield = f'data/yield/pre/du/'
files_yield = os.listdir(path_yield)
files_yield = [file for file in files_yield if os.path.isfile(os.path.join(path_yield, file))]
dates_yield = [file[:10] for file in files_yield]

dates_missing = [date for date in dates_bmf if date not in dates_yield]
files_missing = [f'data/bmf/pre/du/{date}_pre_du.json' for date in dates_missing]

['2011-06-24', '2011-10-28', '2015-02-26']

for date, file in zip(dates_missing, files_missing):
    rate = 'pre'
    du = 'du'
    data, t, y = read_json(date, rate, du)
    curve, status = betas_nss_ols(t=t, y=y, tau=(0.03, 0.42))
    plot_curve(curve, y, t, output_name=f'{date}_{rate}_{du}', date=date, rate=rate)




date = '2008-08-06'
rate = 'pre'
du = 'du'
data, t, y = read_json(date, rate, du)
curve, status = calibrate_nss_ols(t=t, y=y)
plot_curve(curve, y, t, output_name=f'{date}_{rate}_{du}_nss', date=date, rate=rate)

