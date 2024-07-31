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
    Documentação: https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/documentacao
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui3#/
    https://dadosabertos.bcb.gov.br/dataset/expectativas-mercado/resource/dc8139ea-2555-48d7-9026-54e3b5d1815b?inner_span=True
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui2#/


"""

