import numpy as np
from nelson_siegel_svensson.calibrate import calibrate_ns_ols
from nelson_siegel_svensson.calibrate import betas_nss_ols
from pandas import DataFrame


def interpolate(data, date):
    if isinstance(data, DataFrame):
        df = data.loc[:, date]
        df = df.dropna(how='all')
        df = df.loc[df.index <= 3600]
        df = df.loc[df.index > 1]
        df = df[df != 0.0]
        t = np.array(df.index)
        y = np.array(df)

        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                curve, status = calibrate_ns_ols(t, y)
                return curve, y, t
            except np.linalg.LinAlgError as e:
                print(f"{date} Attempt {attempt + 1} failed: {e}")
                if attempt == max_attempts - 1:
                    print(f"{date} Interpolation failed after 3 attempts.")
                    print(f'\n\n\n\n--------------------\n{y}\n\n\n')
                    return None, y, t

    # Todo: how to get the data?
    # Todo: how define the date?
    # Todo: what kind of data to accept? dict or df? check type and convert if the case
