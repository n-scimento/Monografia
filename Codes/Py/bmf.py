import pandas as pd 
import numpy as np
import warnings 
warnings.filterwarnings("ignore")

#%%# Extração Swap Pré x IPCA
def _real(dt):
    """
    Parameters
    ----------
    dt : "dd/mm/yyyy"

    Returns
    -------
    data : yield curve for the given date
    """
    url = f'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data={dt}&slcTaxa=DIC'
    html = pd.read_html(url, encoding = 'latin1') # read B3 data
    data = None 

    if 'Não há dados para a data fornecida!' not in list(html[1].iloc[0]):
        data_list = [float(taxa) for taxa in list(html[1][0])[0].replace('Dias Corridos DI x IPCA 252(2) ', '').replace('Dias Corridos 252(2) ', '').replace(',', '.').split(' ')] # get data and cleaning it 
        n = 0 
        data = []

        while n + 2 < len(data_list):
            data.append(np.array(data_list[n: n + 2]).astype('float64')) # appending data (?)
            n += 2
        
        data = pd.DataFrame(data, columns = ['TenorsDays', 'bd252']) # data cleaning and formatting
        data['Date'] = [dt for n in range(len(data))]
        
        if(type(data) != type(None)):
            data = pd.pivot_table(data, values = 'bd252', index = 'Date', columns = ['TenorsDays']).sort_values(by = 'Date') # format new data with pivot table
            data.columns = data.columns.astype('float64') # format columns 
            data.index = data.index.astype('datetime64[ns]') # format index (rows)
            
    return data 

#%%# Extração Swap Pré X DI
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
    html = pd.read_html(url, encoding = 'latin1') # read B3 data
    data = None 

    if 'Não há dados para a data fornecida!' not in list(html[1].iloc[0]):
        data_list = list(html[1][0])[0].replace('Dias Corridos DI x pré 252(2)(4) 360(1) ', '').replace('Dias Corridos PRExDI 252(2)(4) 360(1) ', '').replace(',', '.').split(' ') # get data and cleaning it 
        n = 0 
        data = []

        while n + 3 < len(data_list):
            data.append(np.array(data_list[n: n + 3]).astype('float64')) # appending data (?)
            n += 3
        
        data = pd.DataFrame(data, columns = ['TenorsDays', 'bd252', 'act360']) # data cleaning and formatting
        data['Date'] = [dt for n in range(len(data))]
        
        if(type(data) != type(None)):
            data = pd.pivot_table(data, values = 'bd252', index = 'Date', columns = ['TenorsDays']).sort_values(by = 'Date') # format new data with pivot table
            data.columns = data.columns.astype('float64') # format columns 
            data.index = data.index.astype('datetime64[ns]') # format index (rows)
            
    return data 

#%%# Solicitação da curva Real para um dia ou para um período

def real(start_date, end_date=None): 

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
    
    date_list = pd.date_range(start = start_date, end = start_date if end_date is None else end_date)
    
    for dt in date_list:
        dt = dt.strftime('%d/%m/%Y')
        print(f'Extraindo negociações de Swap Pré X IPCA para o dia {dt}')
        
        df_rate = _real(dt) # request data based on date (dt)
        df = df_rate if not len(df) else pd.concat([df, df_rate]) # concat new data to the data frame 
        df = df.reindex(columns=sorted(list(df.columns))) # sort columns by tenure 
    return df 

#%%# Solicitação da curva Nominal para um dia ou para um período

def nominal(start_date, end_date=None): 

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
    
    date_list = pd.date_range(start = start_date, end = start_date if end_date is None else end_date)
    
    for dt in date_list:
        dt = dt.strftime('%d/%m/%Y')
        print(f'Extraindo negociações de Swap Pré X DI para o dia {dt}')
        
        df_rate = _nominal(dt) # request data based on date (dt)
        df = df_rate if not len(df) else pd.concat([df, df_rate]) # concat new data to the data frame 
        df = df.reindex(columns=sorted(list(df.columns))) # sort columns by tenure 
    return df

#%%# Update da base de dados 

