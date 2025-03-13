import pandas as pd
from apps.interpolation.nss import interpolate
from apps.database.bmf import BMF
from apps.data_managing.pkl import Pickle
from apps.plots.plot import plot_curve

pkl = Pickle()

start_date = '2025-02-24'
end_date = '2025-02-28'

dus = [True, False]
rates = ['PRE', 'DIC']

for rate in rates:
    for du in dus:
        print(f'\n--------\n{rate} - Du:{du}')
        df = BMF(rate=rate, du=du).get_dataframe(start_date=start_date, end_date=end_date)
        pkl.save(name=f'{rate}_{'du' if du else 'dc'}', df=df)

        for date in df.columns:
            print(f'- {date}: starting')
            curve, y, t = interpolate(df, date)
            if curve:
                plot_curve(curve, y, t, output_name=f'{date}_{rate}_{'du' if du else 'dc'}')
                print(f' - {date}: done!')
            elif not curve:
                print(f'\n----------\n{date} | {rate} | {du}: {curve}')
                print(f'{y}\n----------\n')

                # TODO: algumas curvas não estão fittando; descobrir como passar os parametros
                # TODO: se conseguir passar os parametros, descobrir o metodogenetico (aquela library la)s
