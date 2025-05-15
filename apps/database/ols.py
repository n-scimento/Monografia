import numpy as np
import json
import pandas as pd
import os
import matplotlib.pyplot as plt
from apps.interpolation.nss_library.calibrate import *

def read_raw(date, rate, du):
    raw_path = f"data/bmf/{rate}/{du}/"
    file_path = f"{date}_{rate}_{du}.json"

    yield_path = f"data/yield/nss/{rate}/{du}/"

    with open(raw_path + file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(yield_path + file_path, "r", encoding="utf-8") as f:
        parameters = json.load(f)

    data = data[date]
    data = {int(float(k)): v for k, v in sorted(data.items(), key=lambda item: int(float(item[0]))) if
            int(float(k)) <= 3600}

    t = np.array(list(data.keys()))
    y = np.array(list(data.values()))

    return data, t / 360, y / 100, parameters

rate = 'pre'
du = 'du'

path = f'data/bmf/{rate.lower()}/{du}/'
files = os.listdir(path)
files = [file for file in files if os.path.isfile(os.path.join(path, file))]
cutoff_date = '2000-12-12'
dates = [date[:10] for date in files if date[:10] >= cutoff_date]


errors = []
for date in dates: # for date in dates:
    data, t, y, parameters = read_raw(date, rate, du)

    if t.shape == y.shape:
        curve = NelsonSiegelSvenssonCurve(beta0=parameters['b0'], beta1=parameters['b1'],
                                          beta2=parameters['b2'], beta3=parameters['b3'],
                                          tau1=parameters['t1'],  tau2=parameters['t2'])
        r = np.sum((curve(t) - y) ** 2)
        errors.append({date: r})
        print(f"{date}: {r}")

flattened = {list(error.keys())[0]: list(error.values())[0] for error in errors}
df = pd.DataFrame.from_dict(flattened, orient='index', columns=['value'])
df.index = pd.to_datetime(df.index)
df.index.name = 'date'
df.to_excel('apps/var/errors.xlsx')

q1 = df['value'].quantile(0.10)
q3 = df['value'].quantile(0.90)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Filter data to remove outliers
df_filtered = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]

# Plot histogram and boxplot as subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histogram (filtered)
axes[0].hist(df_filtered['value'], bins=30, color='#08306b', edgecolor='#051a3a', alpha=1)
axes[0].set_title("Histograma")
axes[0].set_ylabel("Frequência")
axes[0].grid(True)

# Boxplot (filtered)
axes[1].boxplot(df_filtered['value'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='#08306b', color='black'),
                medianprops=dict(color='black'),
                whiskerprops=dict(color='black'),
                capprops=dict(color='black'),
                flierprops=dict(marker='o', color='red', alpha=0))  # Hide outliers
axes[1].set_title("Boxplot")
axes[1].set_xticks([])
axes[1].grid(True)

# Save plot
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.suptitle("Mínimos Quadrados Ordinários", fontsize=14)
output_path = os.path.join("apps/var/plots_new", "nss-error-distribution-filtered.png")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.close()

    #
    # plt.figure(figsize=(8, 5))
    # plt.plot(t, y, 'o', label='Observed yields')
    # plt.plot(t, curve(t), '-', label='Fitted curve (NSS)')
    # plt.xlabel('Maturity (t)')
    # plt.ylabel('Yield')
    # plt.title('Nelson-Siegel-Svensson Curve Fit')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    #
    # # Save plot as PNG
    # plt.savefig("nss_curve_fit.png", dpi=300)
    # plt.close()  # Close to prevent display in some environments