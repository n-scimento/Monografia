import numpy as np
from nelson_siegel_svensson.calibrate import betas_nss_ols
from apps.interpolation.nss_library.calibrate import calibrate_nss_ols
import json
import os
import pandas as pd
from apps.plots.plot import plot_curve


def read_json(date, rate, du):
    root_path = f"data/bmf/{rate}/{du}/"
    file_path = f"{date}_{rate}_{du}.json"

    with open(root_path + file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = data[date]
    data = {int(float(k)): v for k, v in sorted(data.items(), key=lambda item: int(float(item[0]))) if
            int(float(k)) <= 3600}

    t = np.array([int(float(k)) for k in data.keys()])
    y = np.array(list(data.values()))

    return data, t / 360, y / 100


def fit_yield(rate, du):
    yield_parameters = {}

    path = f'data/bmf/{rate.lower()}/{du}/'
    files = os.listdir(path)
    files = [file for file in files if os.path.isfile(os.path.join(path, file))]
    cutoff_date = '2009-05-27'
    dates = [date[:10] for date in files if date[:10] >= cutoff_date]

    for date, file in zip(dates, files):
        data, t, y = read_json(date, rate, du)

        print(f'\n-------\n{date}\n-------------------------------')

        def try_calibrate(method, t, y, start=None):
            if not start:
                curve, status = calibrate_nss_ols(t=t, y=y, method=method)
            else:
                curve, status = calibrate_nss_ols(t=t, y=y, method=method, tau0=start)
            if any(beta > 1.0 for beta in [curve.beta0, curve.beta1, curve.beta2, curve.beta3]):
                print(f"-- Parameters too high with {method}, ignoring this method: {curve}")
                return None, None, 1000000

            error = np.sum((curve(t) - y) ** 2)
            return curve, status, error

        methods = ["TNC", "COBYQA", "POWELL", "BFGS", "L-BFGS-B", "CG", "SLSQP"]
        best_curve, best_status, best_error = None, None, 1000000

        for method in methods:
            try:
                curve, status, error = try_calibrate(method, t, y)
                if curve is not None and error < best_error:
                    best_curve, best_status, best_error = curve, status, error
            except np.linalg.LinAlgError:
                print(f"-- {method} failed due to LinAlgError, skipping this method.")

        if best_curve is None:

            for method in methods:

                try:

                    curve, status, error = try_calibrate(method, t, y, start=(1.0, 1.0))
                    if curve is not None and error < best_error:
                        best_curve, best_status, best_error = curve, status, error

                except np.linalg.LinAlgError:
                    print(f"-- {method} failed due to LinAlgError, skipping this method.")

                if best_curve is None:
                    raise ValueError("All methods failed or had invalid parameters.")


        curve = best_curve
        # def try_calibrate(method, t, y):
        #     curve, status = calibrate_nss_ols(t=t, y=y, method=method)
        #
        #     if any(beta < -1.0 or beta > 1.0 for beta in [curve.beta0, curve.beta1, curve.beta2, curve.beta3]):
        #         print(f"-- Parameters too high with {method}, moving to the next method: {curve}")
        #         return None, None
        #
        #     return curve, status
        #
        # methods = ["TNC", "COBYQA", "POWELL", "BFGS", "L-BFGS-B", "CG", "SLSQP"]
        # curve, status = None, None
        #
        # for method in methods:
        #     try:
        #         curve, status = try_calibrate(method, t, y)
        #         if curve is not None:
        #             break
        #     except np.linalg.LinAlgError:
        #         print(f"-- {method} failed due to LinAlgError, trying the next method.")
        #
        # if curve is None:
        #     raise ValueError("All methods failed.")

        plot_curve(curve, y, t, output_name=f'{date}_nss_{rate}_{du}', date=date, rate=rate)

        params = {
            'b0': float(curve.beta0),
            'b1': float(curve.beta1),
            'b2': float(curve.beta2),
            'b3': float(curve.beta3),
            't1': float(curve.tau1),
            't2': float(curve.tau2),
        }
        yield_parameters[date] = params

        root_path = f"data/yield/nss/{rate}/{du}_comparative/"
        file_path = f"{date}_{rate}_{du}.json"

        with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
            json.dump(params, json_file, ensure_ascii=False, indent=4)
            print(f'Saved at: {(root_path + file_path).lower()}')

        print(f' - {date}: done!')

    # root_path = f"data/yield/"
    # file_path = f"{rate}_{du}.json"
    #
    # with open((root_path + file_path).lower(), 'w', encoding='utf-8') as json_file:
    #     json.dump(yield_parameters, json_file, ensure_ascii=False, indent=4)
    #     print(f'Saved at: {(root_path + file_path).lower()}')
    return

rate = 'pre'
du = 'du'
yield_1 = fit_yield(rate, du)

path = f"data/yield/nss/{rate}/{du}_fixed/"
files = os.listdir(path)
files = [file for file in files if os.path.isfile(os.path.join(path, file))]

df_list = []
for file in files:
    file_path = os.path.join(path, file)
    with open(file_path, "r") as f:
        data = json.load(f)  # Load the JSON file
        df_list.append(pd.DataFrame([data]))  # Convert to DataFrame and append

df = pd.concat(df_list, ignore_index=True)
df.to_csv('nss_parameters_comparative.csv')
# %% Testes

dates = ['2022-04-11']
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
    print(f"\n----------------------------\n{method}")
    betas0 = []
    betas1 = []
    betas2 = []
    betas3 = []
    thetas1 = []
    thetas2 = []
    try:
        for date in dates:
            rate = 'pre'
            du = 'du'
            data, t, y = read_json(date, rate, du)
            curve, status = betas_nss_ols(t=t, y=y , )#, method=method)
            betas0.append(round(curve.beta0,2))
            betas1.append(round(curve.beta1,2))
            betas2.append(round(curve.beta2,2))
            betas3.append(round(curve.beta3,2))
            thetas1.append(round(curve.tau1,2))
            thetas2.append(round(curve.tau2,2))
            plot_curve(curve, y, t, output_name=f'ERROR_FIXING_{date}_{rate}_{du}_nss_{method}_', date=date, rate=rate)
    except:

        pass

    print(f"Beta 0 {betas0}")
    print(f"Beta 1 {betas1}")
    print(f"Beta 2 {betas2}")
    print(f"Beta 3 {betas3}")
    print(f"Theta 1 {thetas1}")
    print(f"Theta 2 {thetas2}")

date = '2022-04-11'
data, t, y = read_json(date, rate, du)
curve, status = calibrate_nss_ols(t=t, y=y, method='TNC') #, method=method)