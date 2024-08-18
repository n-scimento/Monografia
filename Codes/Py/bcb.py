#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Jul 31 00:17:17 2024

@author: nascimento

---
Planos:
    Construir a base
        Formatar a base para o formato da curva de juros! (index = data, column = maturity (período da previsçao), dados = valores)
    Criar as funções
        Função para puxar um dado de um período específico
        Atualizador da base de dados: TODOS OS DADOS 
    
Base: https://www3.bcb.gov.br/expectativas2/#/consultaSeriesEstatisticas


Dados:
    IPCA
    PIB
    FX
    SELIC
    
Links:
    Documentação: 
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/documentacao
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui3#/
    https://dadosabertos.bcb.gov.br/dataset/expectativas-mercado/resource/dc8139ea-2555-48d7-9026-54e3b5d1815b?inner_span=True
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui2#/


Facilitar atualização:
    Quebrar o download de dados por períodos: construir base até 2024 e a partir daí puxar até os dias de hoje. 
    Como? adicionando um argumento vazio no texto do URL, que só será preenchido quando passarmos o parametro
    
    Filtro para data: 
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoSelic?$filter=baseCalculo%20eq%200%20and%20Data%20ge%20%272010-01-01%27%20and%20Data%20lt%20%272024-01-01%27

"""
#%%# Libraries

import requests
import pandas as pd 
import threading

#%%# Função de download

class bcb():
    
    def __init__(self):
       
        self.url = 'https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata'
        
        self.data  = [
        ['selic_reuniao', self.url + "/ExpectativasMercadoSelic?$filter=baseCalculo eq 0",  'Reuniao'],
        ['pib_trimestral', self.url + "/ExpectativasMercadoTrimestrais?$filter=Indicador eq 'PIB Total'"],
        ['ipca_12', self.url + "/ExpectativasMercadoInflacao12Meses?$filter=Indicador eq 'IPCA'", 'Indicador'],
        ['selic_anual', self.url + "/ExpectativasMercadoAnuais?$filter=Indicador eq 'Selic'" ],
        ['pib_anual', self.url + "/ExpectativasMercadoAnuais?$filter=Indicador eq 'PIB Total'"],
        ['usd_anual', self.url + "/ExpectativasMercadoAnuais?$filter=Indicador eq 'Câmbio'"],
        ['ipca_anual', self.url + "/ExpectativasMercadoAnuais?$filter=Indicador eq 'IPCA'"],
        ['ipca_mensal', self.url + "/ExpectativaMercadoMensais?$filter=Indicador eq 'IPCA' and baseCalculo eq 0"],
        ['usd_mensal', self.url + "/ExpectativaMercadoMensais?$filter=Indicador eq 'Câmbio'"],
        ]
        
    def _data_request(self, name, url, columns = 'DataReferencia'):
        
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
        
    def bcb_download(self, data_list = slice(0,9)):
        """
        It will download all the BCB's databases if none argument is passed.
        
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
            
        print('\nBaixando as seguintes tabelas:')
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
                df = pd.read_csv(f'./Data/BCB/{table}.csv', index_col = 0 )
                df_list.append(df)
                print(' - feito')
            except Exception as e:
                print(f'ERROR {table}: {e}\n')
            
        return df_list
    
    #%%# BCB thread download
    
    def bcb_download_thread(self):
        """
        It will download all the BCB's database with multi threading for a better performance.
        
        Return: none.
        """
        
        threads = []
  
        for arguments in self.data:
            t = threading.Thread(target=self._data_request, args=(*arguments,))
            t.start()
            threads.append(t)  
        
        for t in threads:
            t.join()

# #%%# BCB Update
#     def bcb_update(self, data_list = slice(0,9)):
#        """
#        It will download all the BCB's databases if none argument is passed.
       
#        The argument can be a list or a slice, in which items correspond to:
#            0. Selic por reunião
#            1. PIB trimestral
#            2. IPCA em 12 meses
#            3. Selic anual
#            4. PIB anual
#            5. Câmbio anual
#            6. IPCA anual
#            7. IPCA mensal
#            8. Câmbio mensal
       
#        Return: a list of dataframes with the formatted data. 
#        """
       
#        df_list = []
       
#        if isinstance(data_list, slice):
#            selected_data = self.data[data_list]
#        elif isinstance(data_list, list):
#            selected_data = [self.data[i] for i in data_list]
#        else:
#            raise ValueError("data_list must be a slice or a list of indices.")
           
#        print('\nAtualizando as seguintes tabelas:')
#        for arguments in selected_data:
#            print(f'- {arguments[0]}')
   
#        for arguments in selected_data:
       
#            df = pd.read_csv(f'./Data/BCB/{arguments[0]}.csv', index_col = 0 )
           
#            start_date = df.iloc[-1].name.strftime('%Y-%m-%d')
#            end_date = pd.Timestamp.now().date().strftime('%Y-%m-%d')
           
#            try:
#                df = self._data_request(arguments[0], arguments[1] , arguments[2] if arguments[2] else None)
#                df_list.append(df)
               
#            except Exception as e:
#                print(f'ERROR {arguments[0]}: {e}\n')
       
#        return df_list
