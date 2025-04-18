import numpy as np
from nelson_siegel_svensson.calibrate import betas_nss_ols
from apps.interpolation.nss_library.calibrate import calibrate_nss_ols
from apps.interpolation.nss_library.nss import NelsonSiegelSvenssonCurve
import json
import os
import pandas as pd
from apps.plots.plot import plot_curve


def get_closest_keys(data):
    target_keys = [30, 60, 90, 180, 360, 720, 1080, 1440, 1800, 3600]
    closest_keys = {}
    for target in target_keys:
        closest_key = min(data.keys(), key=lambda x: abs(x - target))
        closest_keys[target] = data[closest_key]
    return closest_keys


def read_json(date, rate, du):
    root_path = f"data/bmf/{rate}/{du}/"
    file_path = f"{date}_{rate}_{du}.json"

    with open(root_path + file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = data[date]
    data = {int(float(k)): v for k, v in sorted(data.items(), key=lambda item: int(float(item[0]))) if
            int(float(k)) <= 3600}

    # Get the closest keys to the target keys
    closest_data = get_closest_keys(data)

    t = np.array(list(closest_data.keys()))
    y = np.array(list(closest_data.values()))

    return data, t / 360, y / 100


def fit_yield(rate, du):
    yield_parameters = {}

    path = f'data/bmf/{rate.lower()}/{du}/'
    files = os.listdir(path)
    files = [file for file in files if os.path.isfile(os.path.join(path, file))]
    cutoff_date = '2000-12-12'
    dates = [date[:10] for date in files if date[:10] >= cutoff_date]

    for date, file in zip(dates, files):
        data, t, y = read_json(date, rate, du)

        print(f'\n-------\n{date}\n-------------------------------')

        def try_calibrate(method, t, y, start=None):
            if not start:
                curve, status = calibrate_nss_ols(t=t, y=y, method=method)
            else:
                curve, status = calibrate_nss_ols(t=t, y=y, method=method, tau0=start)

            if status.success and all(
                    -1.0 <= beta <= 1.0 for beta in [curve.beta0, curve.beta1, curve.beta2, curve.beta3]) and all(
                    -20.0 <= tau <= 20.0 for tau in [curve.tau1, curve.tau2]):
                error = np.sum((curve(t) - y) ** 2)
                return curve, status, error
            else:
                return None, None, 1000000

        methods = [
            'Nelder-Mead',
            'Powell',
            'CG',
            'BFGS',
            'L-BFGS-B',
            'TNC',
            'COBYLA',
            'COBYQA',
            'SLSQP',
            'trust-constr',
        ]

        best_curve, best_status, best_error = None, None, 1000000

        for method in methods:
            try:
                curve, status, error = try_calibrate(method, t, y)
                if curve is not None and error < best_error:
                    best_curve, best_status, best_error = curve, status, error
            except (np.linalg.LinAlgError, ValueError):
                print(f"-- {method} failed due to LinAlgError, skipping this method.")

        if best_curve is None:
            for method in methods:
                try:
                    curve, status, error = try_calibrate(method, t, y, start=(2.0, 5.0))
                    if curve is not None and error < best_error:
                        best_curve, best_status, best_error = curve, status, error
                except np.linalg.LinAlgError:
                    print(f"-- {method} failed due to LinAlgError, skipping this method.")

            if best_curve is None:
                raise ValueError("All methods failed or had invalid parameters.")

        curve = best_curve

        plot_curve(curve, y, t, output_name=f'{date}_nss_{rate}_{du}', date=date, rate=rate, folder='menos_e_mais')

        params = {
            'b0': float(curve.beta0),
            'b1': float(curve.beta1),
            'b2': float(curve.beta2),
            'b3': float(curve.beta3),
            't1': float(curve.tau1),
            't2': float(curve.tau2),
        }
        yield_parameters[date] = params

        root_path = f"data/yield/nss/{rate}/{du}/"
        file_path = f"{date}_{rate}_{du}.json"

        with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
            json.dump(params, json_file, ensure_ascii=False, indent=4)
            print(f'Saved at: {(root_path + file_path).lower()}')

        print(f' - {date}: done!')

    return


rate = 'pre'
du = 'du'
# yield_1 = fit_yield(rate, du)

path = f"./data/yield/nss/{rate}/{du}"
files = os.listdir(path)
files = [file for file in files if os.path.isfile(os.path.join(path, file))]

df_list = {}
for file in files:
    file_path = os.path.join(path, file)
    with open(file_path, "r") as f:
        data = json.load(f)
        df_list[file[:10]] = data  # Convert to DataFrame and append

pd.DataFrame(df_list).to_csv('nss_parameters.csv')


#%%# MQO: load observations, load
rate = 'pre'
du = 'du'

path_nss = f"./data/yield/nss/{rate}/{du}"
files_nss = os.listdir(path_nss)
files_nss = [file for file in files_nss if os.path.isfile(os.path.join(path, file))]
df_list = {}

path_bmf = f'data/bmf/{rate.lower()}/{du}/'
files_bmf = os.listdir(path_bmf)
files_bmf = [file for file in files_bmf if os.path.isfile(os.path.join(path, file))]

for date, file in zip(files_bmf, files_nss):

    file_path = os.path.join(path, file)
    data, t, y = read_json(date, rate, du)

    with open(file_path, "r") as f:
        data = json.load(f)
        df_list[file[:10]] = data  # Convert to DataFrame and append

pd.DataFrame(df_list).to_csv('nss_parameters.csv')

yield_parameters = {}

path = f'data/bmf/{rate.lower()}/{du}/'
files = os.listdir(path)
files = [file for file in files if os.path.isfile(os.path.join(path, file))]
cutoff_date = '2000-12-12'
dates = [date[:10] for date in files if date[:10] >= cutoff_date]

for date, file in zip(dates, files):
    data, t, y = read_json(date, rate, du)

# %%#
rate = 'pre'
du = 'du'
date = '2005-01-07'
data, t, y = read_json(date, rate, du)

methods = [
    'Nelder-Mead', 'Powell',
    'CG',
    'BFGS',
    'Newton-CG',
    'L-BFGS-B',
    'TNC',
    'COBYLA',
    'COBYQA',
    'SLSQP',
    'trust-constr',
    'dogleg',
    'trust-ncg',
    'trust-exact',
    'trust-krylov',
]
for method in methods:
    try:
        curve, status = calibrate_nss_ols(t=t, y=y, method=method, tau0=(2.0, 5.0))

        if status.success and all(
                -1.0 <= beta <= 1.0 for beta in [curve.beta0, curve.beta1, curve.beta2, curve.beta3]) and all(
            -20.0 <= tau <= 20.0 for tau in [curve.tau1, curve.tau2]):
            plot_curve(curve, y, t, output_name=f'ERROR_FIXING_{date}_{rate}_{du}_nss_{method}_', date=date, rate=rate)
            print(f"\n----------\n{method}: {status.success}")
            print(curve)
            print(np.sum((curve(t) - y) ** 2))
            print(f"---------------\n")
    except:
        pass
