import pandas as pd 
import numpy as np

def real(dt):
    url = r'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data=' + dt.strftime('%d/%m/%Y') + '&slcTaxa=DIC'
    html = pd.read_html(url) # read B3 data
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

    return data 

def nominal(dt):
    url = r'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data=' + dt.strftime('%d/%m/%Y') + '&slcTaxa=PRE'
    html = pd.read_html(url) # read B3 data
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

    return data 
