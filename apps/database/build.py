from apps.database.bmf import BMF
import numpy as np
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
import json
import os
import pandas as pd
from apps.interpolation.nss import interpolate
from apps.plots.plot import plot_curve

start_date = '2005-01-01'
end_date = '2024-12-31'

dus = [True, False]
rates = ['PRE', 'DIC']

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


dfs = ['data/bmf/df_pre_du.csv', 'data/bmf/df_pre_dc.csv', 'data/bmf/df_dic_du.csv']

for df in dfs:

    name = df
    print(f'\n\n--------------------\n{name}')
    rate = name.split('/')[2].split('_')[1]
    du = name.split('/')[2].split('_')[2][:2]

    df = pd.read_csv(df)
    yield_parameters = {}

    for date in df.columns:

        print(f'- {date}: starting')
        curve, y, t = interpolate(df, date)

        if curve:
            plot_curve(curve, y, t, output_name=f'{date}_{rate}_{du}')

            params = {
                'b0': float(curve.beta0),
                'b1': float(curve.beta1),
                'b2': float(curve.beta2),
                'b3': float(curve.beta3),
                't1': float(curve.tau1),
                't2': float(curve.tau2),
            }
            yield_parameters[date] = params

            root_path = f"data/yield/{rate}/{du}/"
            file_path = f"{date}_{rate}_{du}.json"

            with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
                json.dump(params, json_file, ensure_ascii=False, indent=4)
                print(f'Saved at: {(root_path + file_path).lower()}')

            print(f' - {date}: done!')

    root_path = f"data/yield/"
    file_path = f"{rate}_{du}.json"

    with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
        json.dump(yield_parameters, json_file, ensure_ascii=False, indent=4)
        print(f'Saved at: {(root_path + file_path).lower()}')


    # Todo: gerar dataframe com tudo que não teve fit