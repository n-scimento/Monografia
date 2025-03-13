import requests



headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.anbima.com.br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.anbima.com.br/informacoes/est-termo/default.asp',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=4',
}

data = {
    'escolha': '2',
    'Idioma': 'US',
    'saida': 'csv',
    'Dt_Ref_Ver': '20240118',
    'Dt_Ref': '17/01/2024',
}

response = requests.post('https://www.anbima.com.br/informacoes/est-termo/CZ.asp', headers=headers, data=data)

print(response.text)''