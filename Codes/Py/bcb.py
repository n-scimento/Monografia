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

#%%# Code 
url = 'https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata'

response = requests.get(url + "/ExpectativasMercadoSelic")

df = pd.DataFrame(response.json()['value'])

df_pivot = pd.pivot_table(df, values = 'Mediana', columns = 'Reuniao', index = 'Data')

#%%# Bases ?$filter={} eq 'name'

url_selic_reuniao = "/ExpectativasMercadoSelic?$filter=Indicador eq 'Selic'"
url_selic_anual = "/ExpectativasMercadoAnuais?$filter=Indicador eq 'Selic'" # pegar última reunião de cada ano

url_pib_trimestral = "/ExpectativasMercadoTrimestrais?$filter=Indicador eq 'PIB Total'"
url_pib_anual = "/ExpectativasMercadoAnuais?$filter=Indicador eq 'PIB Total'"

url_usd_mensal = "/ExpectativaMercadoMensais?$filter=Indicador eq 'Câmbio'"
url_usd_anual = "/ExpectativasMercadoAnuais?$filter=Indicador eq 'Câmbio'"

url_ipca_mensal = "/ExpectativaMercadoMensais?$filter=Indicador eq 'IPCA'"
url_ipca_12 = "/ExpectativasMercadoInflacao12Meses?$filter=Indicador eq 'IPCA'"
url_ipca_anual = "/ExpectativasMercadoAnuais?$filter=Indicador eq 'IPCA'"

df_selic_reuniao = pd.DataFrame(requests.get(url + url_selic_reuniao).json()['value'])
df_pib_trimestral = pd.DataFrame(requests.get(url + url_pib_trimestral).json()['value'])
df_ipca_12 = pd.DataFrame(requests.get(url + url_ipca_12).json()['value'])

df_selic_anual = pd.DataFrame(requests.get(url + url_selic_anual).json()['value'])
df_pib_anual = pd.DataFrame(requests.get(url + url_pib_anual).json()['value'])
df_usd_anual = pd.DataFrame(requests.get(url + url_usd_anual).json()['value'])
df_ipca_anual = pd.DataFrame(requests.get(url + url_ipca_anual).json()['value'])

df_usd_mensal = pd.DataFrame(requests.get(url + url_usd_mensal).json()['value'])
df_ipca_mensal = pd.DataFrame(requests.get(url + url_ipca_mensal).json()['value'])

df_selic_reuniao.to_csv('./Data/BCB/selic_reuniao_raw.csv')
df_pib_trimestral.to_csv('./Data/BCB/pib_trimestral_raw.csv')
df_ipca_12.to_csv('./Data/BCB/ipca_12_raw.csv')


# Formatar

df_selic_anual.to_csv('./Data/BCB/selic_anual_raw.csv')
df_pib_anual.to_csv('./Data/BCB/pib_anual_raw.csv')
df_usd_anual.to_csv('./Data/BCB/usd_anual_raw.csv')
df_ipca_anual.to_csv('./Data/BCB/ipca_anual_raw.csv')

df_usd_mensal.to_csv('./Data/BCB/usd_mensal_raw.csv')
df_ipca_mensal.to_csv('./Data/BCB/ipca_mensal_raw.csv')