# %%# Libraries
import os
os.system('pip install openpyxl')
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import os
import re

# %%# Loading Data
variables_list = ["beta1", "beta2", "beta3", "beta4", "tau1", "tau2",
                  "ipca_anual_current", "ipca_anual_1y", "ipca_anual_2y", "ipca_anual_3y",
                  "selic_anual_current", "selic_anual_1y", "selic_anual_2y", "selic_anual_3y",
                  "usd_anual_current", "usd_anual_1y", "usd_anual_2y", "usd_anual_3y",
                  "pib_anual_current", "pib_anual_1y", "pib_anual_2y", "pib_anual_3y"]

df = pd.read_excel('../../data/database.xlsx', index_col='Date')[variables_list]


def rename_column(col):
    # col = col.replace("ipca", "IPCA")
    # col = col.replace("selic", "SELIC")
    # col = col.replace("usd", "USDBRL")
    # col = col.replace("pib", "PIB")

    col = col.replace("anual_current", "ano_t0")
    col = re.sub(r"anual_(\d+)y", lambda m: f"ano_t{m.group(1)}", col)

    return col


df.columns = [rename_column(col) for col in df.columns]

# %%# Removendo 0 e observações vazias
cols_excluidas = ['beta1', 'beta2', 'beta3', 'beta4', 'tau1', 'tau2']
df.loc[:, ~df.columns.isin(cols_excluidas)] = df.loc[:, ~df.columns.isin(cols_excluidas)].mask(df == 0).ffill()

# %%# Plotting
# Definindo os grupos
groups = {
    'Nelson-Siegel Factors': {
        'cols': ["beta1", "beta2", "beta3", "beta4", "tau1", "tau2"],
        'y_label': 'Fatores de Nelson-Siegel',
        'line_color': 'Blues',  # Definir a cor do degradê
        'subtitle': 'Fatores modelados de acordo com a curva de rendimento',
        'marker': 'o',  # Bolinhas para a série temporal
    },
    'Expectativas IPCA': {
        'cols': [col for col in df.columns if col.startswith("ipca")],
        'y_label': 'Expectativas IPCA',
        'line_color': 'Greens',
        'subtitle': 'Expectativas para a inflação do IPCA',
        'marker': '-'  # Linha contínua
    },
    'Expectativas SELIC': {
        'cols': [col for col in df.columns if col.startswith("selic")],
        'y_label': 'Expectativas SELIC',
        'line_color': 'Reds',
        'subtitle': 'Expectativas para a taxa de juros SELIC',
        'marker': '-'  # Linha contínua
    },
    'Expectativas USD': {
        'cols': [col for col in df.columns if col.startswith("usd")],
        'y_label': 'Expectativas USD',
        'line_color': 'Oranges',
        'subtitle': 'Expectativas para o valor do USD',
        'marker': '-'  # Linha contínua
    },
    'Expectativas PIB': {
        'cols': [col for col in df.columns if col.startswith("pib")],
        'y_label': 'Expectativas PIB',
        'line_color': 'Purples',
        'subtitle': 'Expectativas para o Produto Interno Bruto',
        'marker': '-'  # Linha contínua
    },
}

# Função para plotar e salvar cada grupo
for group_name, attributes in groups.items():
    ax = plt.gca()  # Obter o eixo para customização

    # Se for o grupo 'Nelson-Siegel Factors', usar bolinhas
    if group_name == 'Nelson-Siegel Factors':
        for i, col in enumerate(attributes['cols']):
            ax.plot(df.index, df[col], marker=attributes['marker'], color=plt.cm.Blues(i / len(attributes['cols'])), label=col)
    else:
        # Caso contrário, fazer um degradê nas séries
        for i, col in enumerate(attributes['cols']):
            ax.plot(df.index, df[col], color=plt.cm.get_cmap(attributes['line_color'])(i / len(attributes['cols'])), label=col)

    plt.xlabel('Data')
    plt.ylabel(attributes['y_label'])  # Eixo Y personalizado
    plt.grid(True)
    plt.legend(loc='best')
    plt.tight_layout()

    # Adicionar subtítulo
    plt.figtext(0.5, 0.95, attributes['subtitle'], ha='center', va='top', fontsize=10, color='black')

    # Sanitize filename
    filename = group_name.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".png"
    filepath = os.path.join("plots_new", filename)
    plt.savefig(filepath)
    plt.close()