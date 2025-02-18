import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")


# %%# Extração Swap Pré x IPCA
def _real(dt):
    """
    Parameters
    ----------
    dt : "dd/mm/yyyy"

    Returns
    -------
    data : yield curve for the given date
    """
    url = f'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data={dt}&slcTaxa=PRE'
    url = f'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data={dt}&slcTaxa=DIC'
    html = pd.read_html(url, encoding='latin1')  # read B3 data
    data = None
    print(f'- Extraindo negociações de Swap DI X IPCA para o dia {dt}')

    if 'Não há dados para a data fornecida!' not in list(html[1].iloc[0]):
        data_list = [float(taxa) for taxa in
                     list(html[1][0])[0].replace('Dias Corridos DI x IPCA 252(2) ', '').replace('Dias Corridos 252(2) ',
                                                                                                '').replace(',',
                                                                                                            '.').split(
                         ' ')]  # get data and cleaning it
        n = 0
        data = []

        while n + 2 < len(data_list):
            data.append(np.array(data_list[n: n + 2]).astype('float64'))  # appending data (?)
            n += 2

        data = pd.DataFrame(data, columns=['TenorsDays', 'bd252'])  # data cleaning and formatting
        data['Date'] = [dt for n in range(len(data))]

        if (type(data) != type(None)):
            data = pd.pivot_table(data, values='bd252', index='Date', columns=['TenorsDays']).sort_values(
                by='Date')  # format new data with pivot table
            data.columns = data.columns.astype('float64')  # format columns
            data.index = pd.to_datetime(data.index, format='%d/%m/%Y')
    return data


# %%# Extração Swap Pré X DI
def _nominal(dt):
    """
    Parameters
    ----------
    dt : "dd/mm/yyyy"

    Returns
    -------
    data : yield curve for the given date
    """
    url = f'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data={dt}&slcTaxa=PRE'
    html = pd.read_html(url, encoding='latin1')  # read B3 data
    data = None
    print(f'- Extraindo negociações de Swap DI X Pré para o dia {dt}')

    if 'Não há dados para a data fornecida!' not in list(html[1].iloc[0]):
        data_list = list(html[1][0])[0].replace('Dias Corridos DI x pré 252(2)(4) 360(1) ', '').replace(
            'Dias Corridos PRExDI 252(2)(4) 360(1) ', '').replace(',', '.').split(' ')  # get data and cleaning it
        n = 0
        data = []

        while n + 3 < len(data_list):
            data.append(np.array(data_list[n: n + 3]).astype('float64'))  # appending data (?)
            n += 3

        data = pd.DataFrame(data, columns=['TenorsDays', 'bd252', 'act360'])  # data cleaning and formatting
        data['Date'] = [dt for n in range(len(data))]
        if (type(data) != type(None)):
            data = pd.pivot_table(data, values='bd252', index='Date', columns=['TenorsDays']).sort_values(
                by='Date')  # format new data with pivot table
            data.columns = data.columns.astype('float64')  # format columns
            data.index = pd.to_datetime(data.index, format='%d/%m/%Y')
    return data


# %%# Solicitação da curva para um dia ou para um período

def _yield(function, start_date, end_date=None):
    """
    Parameters
    ----------
    start_date: "yyyy-mm-dd"
    end_date: "yyyy-mm-dd" (optional)
    
        
    Returns
    -------
    data: yield curve for the given date or range
    """

    df = []

    date_list = pd.date_range(start=start_date, end=start_date if end_date is None else end_date)

    for dt in date_list:

        dt = dt.strftime('%d/%m/%Y')
        df_rate = globals()[function](dt)
        df = df_rate if not len(df) else pd.concat([df, df_rate])

        if df is None:
            print(f'Nenhum dado disponível para {dt}')
            df = []
        else:
            df = df.reindex(columns=sorted(list(df.columns))) if not df.empty else df
    return df


# %%# Update da base de dados

def update():
    """
    It updates the swap's database until today, overwriting the used file.

    Returns
    -------
    df_nominal : pandas dataframe
        DI x Pré Swap negotiations 2005-01-01 until today.
    df_real : pandas dataframe.
        IPCA x Pré Swap negotiations 2005-01-01 until today.

    """
    df_real_hist = pd.read_csv(r'../../Data/BMF/ipca.csv', index_col=0)
    df_nominal_hist = pd.read_csv(r'../../Data/BMF/pre.csv', index_col=0)

    df_real_hist.columns = df_real_hist.columns.astype('float64')
    df_real_hist.index = df_real_hist.index.astype('datetime64[ns]')

    df_nominal_hist.columns = df_nominal_hist.columns.astype('float64')
    df_nominal_hist.index = df_nominal_hist.index.astype('datetime64[ns]')

    print(
        f'Atualizando a base de dados de {df_nominal_hist.iloc[-1].name.strftime("%Y-%m-%d")} até {pd.Timestamp.now().date().strftime("%Y-%m-%d")}')
    df_nominal_update = nominal(df_nominal_hist.iloc[-1].name.strftime('%Y-%m-%d'),
                                pd.Timestamp.now().date().strftime('%Y-%m-%d'))
    df_real_update = real(df_real_hist.iloc[-1].name.strftime('%Y-%m-%d'),
                          pd.Timestamp.now().date().strftime('%Y-%m-%d'))

    df_nominal = pd.concat([df_nominal_hist, df_nominal_update]).reset_index().drop_duplicates(subset='Date',
                                                                                               keep='first').set_index(
        'Date')
    df_real = pd.concat([df_real_hist, df_real_update]).reset_index().drop_duplicates(subset='Date',
                                                                                      keep='first').set_index('Date')

    print('Base atualizada! Salvação em andamento.')
    df_nominal.to_csv(r'./Data/BMF/pre.csv')
    df_real.to_csv(r'./Data/BMF/ipca.csv')

    return df_nominal, df_real


real = lambda start_date, end_date: _yield('_real', start_date, end_date)
nominal = lambda start_date, end_date: _yield('_nominal', start_date, end_date)
