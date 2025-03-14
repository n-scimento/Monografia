from apps.database.bmf import BMF
import numpy as np
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
import json
import os

start_date = '2005-01-01'
end_date = '2024-12-31'

dus = [True, False]
rates = ['PRE', 'DIC']


# %%# From Website
def build_base(rate, du):
    print(f'\n--------\n{rate} - {du}')
    path = f'data/bmf/{rate.lower()}/{'du' if du else 'dc'}/'
    files = os.listdir(path)
    files = [file for file in files if os.path.isfile(os.path.join(path, file))]
    dates_stored = [file[:10] for file in files]
    return BMF(rate=rate, du=du).get_dataframe(start_date=start_date, end_date=end_date, dates_stored=dates_stored)


build_base('PRE', True)
build_base('PRE', False)
build_base('DIC', True)

# %% Build Dataframe

rate = 'PRE'
du = True

path = f'data/bmf/{rate.lower()}/{'du' if du else 'dc'}/'
files = os.listdir(path)
files = [file for file in files if os.path.isfile(os.path.join(path, file))]

file = files[0]
with open(path + file, "r") as file:
    data = json.load(file)

key = list(data.keys())[0]
data_parsed = data[key]
data_sorted = dict(sorted(data_parsed.items(), key=lambda x: float(x[0])))

t = np.array(list(data_sorted.keys()))
y = np.array(list(data_sorted.values()))

curve, status = calibrate_nss_ols(t, y)
