import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import concurrent.futures
import time


class BMF:

    def __init__(self, rate='PRE', du=True):
        self.rate = rate
        self.du = du
        self.url_main = f'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': f'https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?&slcTaxa=',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www2.bmf.com.br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
        }

    def parse_html(self, soup):

        def parse_table(table_data):
            return {table_data[i]: table_data[i + 1 if self.du else 2] for i in range(0, len(table_data), 3)}

        rows_i = [float(item.get_text().replace(',', '.')) for item in soup.find_all('td', class_='tabelaConteudo1')]
        rows_ii = [float(item.get_text().replace(',', '.')) for item in soup.find_all('td', class_='tabelaConteudo2')]

        return {**parse_table(rows_i), **parse_table(rows_ii)}

    def get_date(self, date=datetime.now().strftime("%Y-%m-%d")):

        params = {
            'Data': datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y"),
            'slcTaxa': self.rate,
        }

        response = requests.get(
            self.url_main,
            headers=self.headers,
            params=params,
            timeout=10
        )

        print(date)

        soup = BeautifulSoup(response.content, 'html.parser')

        return {date: self.parse_html(soup)}

    def _generate_date_range(self, start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]

    def _fetch_date(self, date):
        while True:
            try:
                return self.get_date(date=date)

            except requests.exceptions.SSLError:
                time.sleep(10)

            except requests.exceptions.ConnectionError as e:
                if "NameResolutionError" in str(e) or "Failed to resolve" in str(e):
                    print(f"DNS resolution failed for {date}. Retrying...")
                    time.sleep(5)
                    continue
                else:
                    print(f"Connection error for {date}: {e}")
                    return {date: None}

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {date}: {e}")
                return {date: None}
            except ValueError:
                return {date: None}

    def get_range(self, start_date=None, end_date=datetime.now().strftime("%Y-%m-%d"), dates=None, max_workers=10):

        if not dates:
            dates = self._generate_date_range(start_date=start_date, end_date=end_date)

        data = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_date = {executor.submit(self._fetch_date, date): date for date in dates}

            for future in concurrent.futures.as_completed(future_to_date):
                obs = future.result()
                data.update(obs)

        return data

    def parse_dataframe(self, data):
        df = pd.DataFrame(data)
        df = df.sort_index(ascending=True)
        df = df.dropna(axis=1, how='all')
        df = df[sorted(df.columns, key=pd.to_datetime)]
        return df

    def get_dataframe(self, start_date=None, end_date=datetime.now().strftime("%Y-%m-%d"), dates=None, max_workers=10):
        return self.parse_dataframe(
            self.get_range(start_date=start_date, end_date=end_date, dates=dates, max_workers=max_workers))

    # Todo: Try genetic algorithm
    # Todo: just build the whole historic after having the interpolation code
