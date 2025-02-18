import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


class BMF:

    def __init__(self):
        self.url_main = f'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp'

    def parse(self, soup):
        def parse_table(table_data):
            return {table_data[i]: [table_data[i + 1], table_data[i + 2]] for i in range(0, len(table_data), 3)}

        rows_i = [float(item.get_text().replace(',', '.')) for item in soup.find_all('td', class_='tabelaConteudo1')]
        rows_ii = [float(item.get_text().replace(',', '.')) for item in soup.find_all('td', class_='tabelaConteudo2')]

        return {**parse_table(rows_i), **parse_table(rows_ii)}

    def get(self, rate='PRE', date=datetime.now().strftime('%d/%m/%Y')):
        params = {
            'Data': date,
            'slcTaxa': rate,
        }

        response = requests.get(
            self.url_main,
            params=params)

        soup = BeautifulSoup(response.content, 'html.parser')

        return self.parse(soup)

        # Todo: puxar em DU e DC? Abrir escolha?
        # Todo: como parsear para mais de um dia?
