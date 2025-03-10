import numpy as np
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
from nelson_siegel_svensson.calibrate import betas_nss_ols
from pandas import DataFrame


def interpolate(data, date):
    if isinstance(data, DataFrame):
        df = data.loc[:, date]
        df = df.dropna(how='all')
        df = df.loc[df.index <= 3600]
        df = df[df != 0.0]
        t = np.array(df.index)
        y = np.array(df)
        try:
            # curve, status = calibrate_nss_ols(t, y)
            # aplicaria algoritmo genético aqui
            # primeiro rodaria para esse número e iria tentando outros
            curve, status = betas_nss_ols((2.0, 5.0), t, y)
            # TODO: https://medium.com/@polanitzer/nelson-siegel-svensson-in-python-estimating-the-spot-rate-curve-using-the-nelson-siegel-svensson-4753969e61c8
            return curve, y, t
        except np.linalg.LinAlgError as e:
            print(f"Interpolation failed: {e}")
            return None, y, t
            # print(f"\n---------------\nDF not fitted:\n{df}")

    # Todo: how to get the data?
    # Todo: how define the date?
    # Todo: what kind of data to accept? dict or df? check type and convert if the case
