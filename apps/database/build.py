from apps.database.bmf import BMF
import numpy as np
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
# from apps.interpolation.nss_library.calibrate import calibrate_nss_ols
import json
import os
import pandas as pd
from apps.interpolation.nss import interpolate
from apps.plots.plot import plot_curve


def read_json(date, rate, du):
    root_path = f"data/bmf/{rate}/{du}/"
    file_path = f"{date}_{rate}_{du}.json"

    with open(root_path + file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = data[date]
    # data = {int(float(k)): v for k, v in sorted(data.items(), key=lambda item: int(float(item[0])))}
    data = {int(float(k)): v for k, v in sorted(data.items(), key=lambda item: int(float(item[0]))) if int(float(k)) <= 3600}

    t = np.array([int(float(k)) for k in data.keys()])
    y = np.array(list(data.values()))

    return data, t, y / 100


# def fit_yield(rate, du):
#     yield_parameters = {}
#
#     path = f'data/bmf/{rate.lower()}/{du}/'
#     files = os.listdir(path)
#     files = [file for file in files if os.path.isfile(os.path.join(path, file))]
#     dates = [date[:10] for date in files]
#
#     for date, file in zip(dates, files):
#         data, t, y = read_json(date, rate, du)
#         try:
#             curve, status = calibrate_nss_ols(t=t, y=y)
#         except Exception as e:
#             print(f'\n\n{date} | {rate} | {du}: {e}\n\n')
#             curve = None
#
#         if curve:
#             plot_curve(curve, y, t, output_name=f'{date}_nss_{rate}_{du}', date=date, rate=rate)
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
#             root_path = f"data/yield/nss/{rate}/{du}/"
#             file_path = f"{date}_{rate}_{du}.json"
#
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
#
# yield_1 = fit_yield('pre', 'du')
#
#
# path_bmf = f'data/bmf/pre/du/'
# files_bmf = os.listdir(path_bmf)
# files_bmf = [file for file in files_bmf if os.path.isfile(os.path.join(path_bmf, file))]
# dates_bmf = [file[:10] for file in files_bmf]
#
# path_yield = f'data/yield/pre/du/'
# files_yield = os.listdir(path_yield)
# files_yield = [file for file in files_yield if os.path.isfile(os.path.join(path_yield, file))]
# dates_yield = [file[:10] for file in files_yield]
#
# dates_missing = [date for date in dates_bmf if date not in dates_yield]
# files_missing = [f'data/bmf/pre/du/{date}_pre_du.json' for date in dates_missing]
#
# ['2011-06-24', '2011-10-28', '2015-02-26']
#
# for date, file in zip(dates_missing, files_missing):
#     rate = 'pre'
#     du = 'du'
#     data, t, y = read_json(date, rate, du)
#     curve, status = betas_nss_ols(t=t, y=y, tau=(0.03, 0.42))
#     plot_curve(curve, y, t, output_name=f'{date}_{rate}_{du}', date=date, rate=rate)
#
#


# date = '2005-03-02'
# dates = ['2005-03-02','2005-02-03','2005-11-07', '2006-04-17', '2007-01-26', '2007-03-02', '2018-05-10']

dates = ['2005-01-03', '2005-03-15', '2006-03-02', '2006-07-20', '2007-09-24', '2008-09-17', '2010-04-14' ]
for date in dates:
    rate = 'pre'
    du = 'du'
    data, t, y = read_json(date, rate, du)

    curve, status = calibrate_nss_ols(t=t, y=y)# tau0=(1.0, 1.0))
    # print(f"\n----------\n DEFAULT {date}\nb0: {curve.beta0}\nb1: {curve.beta1}\nb2: {curve.beta2}\nb0: {curve.beta3}")
    plot_curve(curve, y, t, output_name=f'{date}_{rate}_{du}_nss__', date=date, rate=rate)

    curve, status = calibrate_nss_ols(t=t, y=y, tau0=(0.010108, 0.011155))
    print(f"\n----------\n ONE O ONE{date}\nb0: {curve.beta0}\nb1: {curve.beta1}\nb2: {curve.beta2}\nb0: {curve.beta3}")
    plot_curve(curve, y, t, output_name=f'{date}_{rate}_{du}_nss_11', date=date, rate=rate)

