from apps.database.bmf import BMF

start_date = '2005-01-01'
end_date = '2024-12-31'

dus = [True, False]
rates = ['PRE', 'DIC']

# for rate in rates:
#     for du in dus:
#         print(f'\n--------\n{rate} - Du:{du}')
#         df = BMF(rate=rate, du=du).get_dataframe(start_date=start_date, end_date=end_date)

print(f'\n--------\nPRE - DU')
df = BMF(rate='PRE', du=True).get_dataframe(start_date=start_date, end_date=end_date)

print(f'\n--------\nPRE - DC')
df = BMF(rate='PRE', du=False).get_dataframe(start_date=start_date, end_date=end_date)

print(f'\n--------\nDIC - DU')
df = BMF(rate='DIC', du=True).get_dataframe(start_date=start_date, end_date=end_date)

print(f'\n--------\nDIC - DC')
df = BMF(rate='DIC', du=False).get_dataframe(start_date=start_date, end_date=end_date)