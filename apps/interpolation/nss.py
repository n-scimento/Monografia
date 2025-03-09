import numpy as np
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
from pandas import DataFrame


def interpolate(data, date):
    if isinstance(data, DataFrame):
        df = data.loc[:,date]
        df = df.dropna(how='all')
        df = df.loc[df.index <= 3600]
        df = df[df != 0.0]
        t = np.array(df.index)
        y = np.array(df)
        try:
            curve, status = calibrate_nss_ols(t, y)
            return curve, y, t
        except np.linalg.LinAlgError as e:
            print(f"Interpolation failed: {e}")
            return None, y, t
            # print(f"\n---------------\nDF not fitted:\n{df}")

    # Todo: how to get the data?
    # Todo: how define the date?
    # Todo: what kind of data to accept? dict or df? check type and convert if the case