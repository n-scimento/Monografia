#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%# To-do

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


"""

#%%# Libraries 
import requests 
import pandas as pd

    
#%%# 

def bcb():
    
    url = 'https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata'
    
    url_selic_reuniao = "/ExpectativasMercadoSelic?$filter=Indicador eq 'Selic'"
    url_selic_anual = "/ExpectativasMercadoAnuais?$filter=Indicador eq 'Selic'" # pegar última reunião de cada ano
    
    url_pib_trimestral = "/ExpectativasMercadoTrimestrais?$filter=Indicador eq 'PIB Total'"
    url_pib_anual = "/ExpectativasMercadoAnuais?$filter=Indicador eq 'PIB Total'"
    
    url_usd_mensal = "/ExpectativaMercadoMensais?$filter=Indicador eq 'Câmbio'"
    url_usd_anual = "/ExpectativasMercadoAnuais?$filter=Indicador eq 'Câmbio'"
    
    url_ipca_mensal = "/ExpectativaMercadoMensais?$filter=Indicador eq 'IPCA'"
    url_ipca_12 = "/ExpectativasMercadoInflacao12Meses?$filter=Indicador eq 'IPCA'"
    url_ipca_anual = "/ExpectativasMercadoAnuais?$filter=Indicador eq 'IPCA'"
    
    #%%# API 
    
    print('\nDownload dos dados:')
    df_selic_reuniao_raw = pd.DataFrame(requests.get(url + url_selic_reuniao).json()['value'])
    print('\n- Selic por reunião baixado!')
    
    df_pib_trimestral_raw = pd.DataFrame(requests.get(url + url_pib_trimestral).json()['value'])
    print('\n- PIB trimestral baixado!')
    
    df_ipca_12_raw = pd.DataFrame(requests.get(url + url_ipca_12).json()['value'])
    print('\n- IPCA 12 meses baixado!')
    
    print('\nDados anuais:')
    df_selic_anual_raw = pd.DataFrame(requests.get(url + url_selic_anual).json()['value'])
    print('\n- SELIC anual baixado!')
    
    df_pib_anual_raw = pd.DataFrame(requests.get(url + url_pib_anual).json()['value'])
    print('\n- PIB anual baixado!')
    
    df_usd_anual_raw = pd.DataFrame(requests.get(url + url_usd_anual).json()['value'])
    print('\n- Câmbio anual baixado!')
    
    df_ipca_anual_raw = pd.DataFrame(requests.get(url + url_ipca_anual).json()['value'])
    print('\n- IPCA anual baixado!')
    
    print('\nDados mensais:')
    df_usd_mensal_raw = pd.DataFrame(requests.get(url + url_usd_mensal).json()['value'])
    print('\n- Câmbio mensal baixado!')
    
    df_ipca_mensal_raw = pd.DataFrame(requests.get(url + url_ipca_mensal).json()['value'])
    print('\n- IPCA mensal baixado!')
    
    def reuniao(value):
        parts = value.split('/')
        return f"{parts[1]}-{parts[0][1:]}"
    
    df_selic_reuniao_raw['Reuniao'] = df_selic_reuniao_raw['Reuniao'].apply(reuniao)
    
    #%%# Save raw
    
    print('\nSalvando arquivos sem formatação')
    df_selic_reuniao_raw.to_csv('./Data/BCB/selic_reuniao_raw.csv')
    df_pib_trimestral_raw.to_csv('./Data/BCB/pib_trimestral_raw.csv')
    df_ipca_12_raw.to_csv('./Data/BCB/ipca_12_raw.csv')
    
    df_selic_anual_raw.to_csv('./Data/BCB/selic_anual_raw.csv')
    df_pib_anual_raw.to_csv('./Data/BCB/pib_anual_raw.csv')
    df_usd_anual_raw.to_csv('./Data/BCB/usd_anual_raw.csv')
    df_ipca_anual_raw.to_csv('./Data/BCB/ipca_anual_raw.csv')
    
    df_usd_mensal_raw.to_csv('./Data/BCB/usd_mensal_raw.csv')
    df_ipca_mensal_raw.to_csv('./Data/BCB/ipca_mensal_raw.csv')
    
    #%%# Format 
    
    print('\nFormatando dados')
    df_selic_reuniao =  pd.pivot_table(df_selic_reuniao_raw, values = 'Mediana', columns = 'Reuniao', index = 'Data')
    df_selic_reuniao.index = pd.to_datetime(df_selic_reuniao.index)
    
    df_pib_trimestral = pd.pivot_table(df_pib_trimestral_raw, values = 'Mediana', columns = 'DataReferencia', index = 'Data')
    df_pib_trimestral.index = pd.to_datetime(df_pib_trimestral.index)
    
    df_ipca_12 = pd.pivot_table(df_ipca_12_raw, values = 'Mediana', columns = 'Indicador', index = 'Data')
    df_ipca_12.index = pd.to_datetime(df_ipca_12.index)
    
    df_selic_anual = pd.pivot_table(df_selic_anual_raw, values = 'Mediana', columns = 'DataReferencia', index = 'Data')
    df_selic_anual.index = pd.to_datetime(df_selic_anual.index)
    
    df_pib_anual = pd.pivot_table(df_pib_anual_raw, values = 'Mediana', columns = 'DataReferencia', index = 'Data')
    df_pib_anual.index = pd.to_datetime(df_pib_anual.index)
    
    df_usd_anual = pd.pivot_table(df_usd_anual_raw, values = 'Mediana', columns = 'DataReferencia', index = 'Data')
    df_usd_anual.index = pd.to_datetime(df_usd_anual.index)
    
    df_ipca_anual = pd.pivot_table(df_ipca_anual_raw, values = 'Mediana', columns = 'DataReferencia', index = 'Data')
    df_ipca_anual.index = pd.to_datetime(df_ipca_anual.index)
    
    df_ipca_mensal = pd.pivot_table(df_ipca_mensal_raw, values = 'Mediana', columns = 'DataReferencia', index = 'Data')
    df_ipca_mensal.index = pd.to_datetime(df_ipca_mensal.index)
    
    df_usd_mensal = pd.pivot_table(df_usd_mensal_raw, values = 'Mediana', columns = 'DataReferencia', index = 'Data')
    df_usd_mensal.index = pd.to_datetime(df_usd_mensal.index)
    
    #%%# Save
    
    print('\nSalvando dados formatados')
    df_selic_reuniao.to_csv('./Data/BCB/selic_reuniao.csv')
    df_pib_trimestral.to_csv('./Data/BCB/pib_trimestral.csv')
    df_ipca_12.to_csv('./Data/BCB/ipca_12.csv')
    
    df_selic_anual.to_csv('./Data/BCB/selic_anual.csv')
    df_pib_anual.to_csv('./Data/BCB/pib_anual.csv')
    df_usd_anual.to_csv('./Data/BCB/usd_anual.csv')
    df_ipca_anual.to_csv('./Data/BCB/ipca_anual.csv')
    
    df_usd_mensal.to_csv('./Data/BCB/usd_mensal.csv')
    df_ipca_mensal.to_csv('./Data/BCB/ipca_mensal.csv')
    
    return df_selic_reuniao, df_pib_trimestral, df_ipca_12, df_selic_anual, df_pib_anual, df_usd_anual, df_ipca_anual, df_usd_mensal, df_ipca_mensal


def bcb_read():
    df_selic_reuniao = pd.read_csv('./Data/BCB/selic_reuniao.csv')
    df_pib_trimestral = pd.read_csv('./Data/BCB/pib_trimestral.csv')
    df_ipca_12 = pd.read_csv('./Data/BCB/ipca_12.csv')
    
    df_selic_anual = pd.read_csv('./Data/BCB/selic_anual.csv')
    df_pib_anual = pd.read_csv('./Data/BCB/pib_anual.csv')
    df_usd_anual = pd.read_csv('./Data/BCB/usd_anual.csv')
    df_ipca_anual = pd.read_csv('./Data/BCB/ipca_anual.csv')
    
    df_usd_mensal = pd.read_csv('./Data/BCB/usd_mensal.csv')
    df_ipca_mensal = pd.read_csv('./Data/BCB/ipca_mensal.csv')
    
    return df_selic_reuniao, df_pib_trimestral, df_ipca_12, df_selic_anual, df_pib_anual, df_usd_anual, df_ipca_anual, df_usd_mensal, df_ipca_mensal
