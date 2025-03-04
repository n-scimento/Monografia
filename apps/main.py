import pandas as pd
from apps.interpolation.nss import interpolate
from apps.database.bmf import BMF
from apps.data_managing.pkl import Pickle
from apps.plots.plot import plot_curve

bmf_pre_du = BMF(rate='PRE', du=True)
bmf_pre_dc = BMF(rate='PRE', du=True)
bmf_ipca_du = BMF(rate='DIC', du=True)
bmf_ipca_dc = BMF(rate='DIC', du=True)


pkl = Pickle()

date = '2025-02-24'
rate = ['PRE', 'IPCA']

for date in dates:
    df = pkl.load(name='df')
    curve, y, t = interpolate(df, date)
    plot_curve(curve, y, t, output_name=f'{}')
