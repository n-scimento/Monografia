import numpy as np
# from nelson_siegel_svensson.calibrate import calibrate_ns_ols
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
# from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
from pandas import DataFrame


def interpolate(data, date):
    if isinstance(data, DataFrame):
        df = data.loc[:,date]
        df = df.dropna(how='all')
        t = np.array(df.index)
        y = np.array(df)
        curve, status = calibrate_nss_ols(t, y)  # starting value of 1.0 for the optimization of tau
        # assert status.success
        # print(curve)
        return curve

    #     print('Dataframe')
    #
    # if isinstance(data, dict):
    #     print('Dict')

    # Todo: how to get the data?
    # Todo: how define the date?
    # Todo: what kind of data to accept? dict or df? check type and convert if the case