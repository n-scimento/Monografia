#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 17:15:20 2024

@author: nascimento
"""

import requests
import pandas as pd 
import threading

#%%# Função de update

class bcb():
    
    def __init__(self):
       
        self.url = 'https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata'
        
        self.data  = [
        ['selic_reuniao', self.url + "/ExpectativasMercadoSelic?$filter=Indicador eq 'Selic'",  'Reuniao'],
        ['pib_trimestral', self.url + "/ExpectativasMercadoTrimestrais?$filter=Indicador eq 'PIB Total'", 'DataReferencia'],
        ['ipca_12', self.url + "/ExpectativasMercadoInflacao12Meses?$filter=Indicador eq 'IPCA'", 'Indicador'],
        ['selic_anual', self.url + "/ExpectativasMercadoAnuais?$filter=Indicador eq 'Selic'" , 'DataReferencia'],
        ['pib_anual', self.url + "/ExpectativasMercadoAnuais?$filter=Indicador eq 'PIB Total'", 'DataReferencia'],
        ['usd_anual', self.url + "/ExpectativasMercadoAnuais?$filter=Indicador eq 'Câmbio'", 'DataReferencia'],
        ['ipca_anual', self.url + "/ExpectativasMercadoAnuais?$filter=Indicador eq 'IPCA'", 'DataReferencia'],
        ['ipca_mensal', self.url + "/ExpectativaMercadoMensais?$filter=Indicador eq 'IPCA'", 'DataReferencia'],
        ['usd_mensal', self.url + "/ExpectativaMercadoMensais?$filter=Indicador eq 'Câmbio'", 'DataReferencia'],
        ]
        
    def _data_request(self, name, url, columns):
        
        print(f'\nBaixando: {name}')
        df_raw = pd.DataFrame(requests.get(url).json()['value'])
        
        print(f'- Baixado: {name}\n- Salvando: {name}')
        df_raw.to_csv(f'./Data/BCB/{name}_raw.csv')
        
        print(f'- Formatando: {name}')
        
        if name == 'selic_reuniao':
            def reuniao(value):
                parts = value.split('/')
                return f"{parts[1]}-{parts[0][1:]}"
            df_raw['Reuniao'] = df_raw['Reuniao'].apply(reuniao)
        else:
            pass
        
        df =  pd.pivot_table(df_raw, values = 'Mediana', columns = columns, index = 'Data')
        df.index = pd.to_datetime(df.index)
        
        print(f'- Salvando formatado: {name}')
        df.to_csv(f'./Data/BCB/{name}.csv')
        
        return df
        
    def bcb_update(self, data_list = slice(0,9)):
        """
        It will update all the BCB's databases if none argument is passed.
        
        The argument can be a list or a slice, in which items correspond to:
            0. Selic por reunião
            1. PIB trimestral
            2. IPCA em 12 meses
            3. Selic anual
            4. PIB anual
            5. Câmbio anual
            6. IPCA anual
            7. IPCA mensal
            8. Câmbio mensal
        
        Return: a list of dataframes with the formatted data. 
        """
        
        df_list = []
        
        if isinstance(data_list, slice):
            selected_data = self.data[data_list]
        elif isinstance(data_list, list):
            selected_data = [self.data[i] for i in data_list]
        else:
            raise ValueError("data_list must be a slice or a list of indices.")
            
        print('\nAtualizando as seguintes tabelas:')
        for arguments in selected_data:
            print(f'- {arguments[0]}')
    
        for arguments in selected_data:
            try:
                df = self._data_request(*arguments)
                df_list.append(df)
                
            except Exception as e:
                print(f'ERROR {arguments[0]}: {e}\n')
        
        return df_list
    
    #%%# BCB load
    
    def bcb_load(self, data_list = slice(0,9)):
        """
        It will load all BCB's databases (csv files) if none argument is passed.
        
        The argument can be a list or a slice, in which items correspond to:
            0. Selic por reunião
            1. PIB trimestral
            2. IPCA em 12 meses
            3. Selic anual
            4. PIB anual
            5. Câmbio anual
            6. IPCA anual
            7. IPCA mensal
            8. Câmbio mensal
        
        Return: a list of dataframes with the formatted data. 
        """
        
        df_list = []
        data = [sublist[0] for sublist in self.data]
        
        if isinstance(data_list, slice):
            selected_data = data[data_list]
        elif isinstance(data_list, list):
            selected_data = [data[i] for i in data_list]
        
        print('\nLoading data:')
        
        for table in selected_data:
            try:
                print(f'- {table}')
                df = pd.read_csv(f'./Data/BCB/{table}.csv')
                df_list.append(df)
                print(' - feito')
            except Exception as e:
                print(f'ERROR {table}: {e}\n')
            
        return df_list
    
    #%%# BCB thread update
    
    def bcb_update_thread(self):
        """
        It will update all the BCB's database with multi threading for a better performance.
        
        Return: none.
        """
        
        threads = []
        
  
        for arguments in self.data:
            t = threading.Thread(target=self._data_request, args=(*arguments,))
            t.start()
            threads.append(t)  
        
        for t in threads:
            t.join()