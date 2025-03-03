import os
os.system('pip install matplotlib')
os.system('pip install nelson-siegel-svensson')

#%%#

from apps.interpolation.nss import interpolate
from apps.database.bmf import BMF
from apps.data_managing.pkl import Pickle

pkl = Pickle()
bmf = BMF(rate='PRE', du=True)

df = pkl.load(name='df')