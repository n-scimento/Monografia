# %%# Libraries
import os

os.system('pip install openpyxl')
os.system('pip install jinja2')
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import os
import re
import numpy as np

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


# %%# Plot NSS
scatter_cols = ['beta1', 'beta2', 'beta3', 'beta4', 'tau1', 'tau2']

n_plots = len(scatter_cols)
n_cols = 3  # Number of columns in subplot grid
n_rows = (n_plots + n_cols - 1) // n_cols

# Create figure and subplots
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows), squeeze=False)
axes = axes.flatten()

for i, col in enumerate(scatter_cols):
    ax = axes[i]
    ax.scatter(df.index, df[col], alpha=0.5, s=4, color='#08306b', edgecolor='#08306b')
    ax.set_title(col)
    ax.grid(True)

# Remove unused axes
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.suptitle("Parâmetros Nelson-Siegel-Svensson", fontsize=14)

# Save to file
output_path = os.path.join("plots_new", "nss-series.png")
plt.savefig(output_path, dpi=300)
plt.close()

#%%# Histogram
n_plots = len(scatter_cols)
n_cols = 3  # Number of columns in subplot grid
n_rows = (n_plots + n_cols - 1) // n_cols

# Create figure and subplots
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows), squeeze=False)
axes = axes.flatten()

for i, col in enumerate(scatter_cols):
    ax = axes[i]
    ax.hist(df[col].dropna(), bins=30, color='#08306b', edgecolor='#051a3a', alpha=1)
    ax.set_title(f"{col}")
    ax.grid(True)

# Remove unused axes
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.suptitle("Distribuição dos parâmetros Nelson-Siegel-Svensson", fontsize=14)

# Save to file
output_path = os.path.join("plots_new", "nss-histograms.png")
plt.savefig(output_path, dpi=300)
plt.close()

# %%# Plot FOCUS

groups = {
    'Expectativas IPCA': {
        'cols': [col for col in df.columns if col.startswith("ipca")],
        'title': 'IPCA',
        'y_label': 'Variação %',
    },
    'Expectativas SELIC': {
        'cols': [col for col in df.columns if col.startswith("selic")],
        'title': 'SELIC',
        'y_label': '% a.a.',
    },
    'Expectativas USD': {
        'cols': [col for col in df.columns if col.startswith("usd")],
        'title': 'Câmbio',
        'y_label': 'BRL/USD',
    },
    'Expectativas PIB': {
        'cols': [col for col in df.columns if col.startswith("pib")],
        'title': 'PIB',
        'y_label': 'Variação % sobre ano anterior',
    },
}

n_groups = len(groups)
n_cols = 2  # Número de colunas de subplots
n_rows = (n_groups + n_cols - 1) // n_cols  # Número de linhas necessário

# Criar figura e eixos
fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows), squeeze=False)
axes = axes.flatten()  # Flatten axes para acesso mais fácil

# Iterar pelos grupos e eixos
for idx, (group_name, attributes) in enumerate(groups.items()):
    ax = axes[idx]
    n_colors = len(attributes['cols'])
    color_range = np.linspace(0.3, 1.0, n_colors)  # Evita tons muito claros/escuros
    cmap = plt.colormaps['Blues']  # Forma moderna de acessar colormap

    for i, (col, cval) in enumerate(zip(reversed(attributes['cols']), color_range)):
        color = cmap(cval)
        ax.plot(
            df.index,
            df[col],
            color=color,
            label=col,
            linestyle='-'
        )

    ax.set_title(attributes['title'], fontsize=10)
    ax.set_ylabel(attributes['y_label'])
    ax.grid(True)
    ax.legend(loc='best', fontsize=8)

# Remover eixos extras (caso n_groups < n_rows * n_cols)
for j in range(idx + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.suptitle("Expectativas Econômicas - FOCUS", fontsize=14)

# Salvar a figura única
output_path = os.path.join("plots_new", "focus.png")
plt.savefig(output_path, dpi=300)
plt.close()


#%%# Tabela estats
summary_stats = df[scatter_cols].agg(['mean', 'std', 'median', 'min', 'max']).T
summary_stats = summary_stats.rename(columns={
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'median': 'Mediana',
    'min': 'Mínimo',
    'max': 'Máximo'
})

# Exibir ou salvar como CSV
print(summary_stats)

# Salvar como CSV
summary_stats.to_csv(os.path.join("plots_new", "nss_summary_stats.csv"))

summary_stats = summary_stats.round(4)

# Exportar como LaTeX
latex_output_path = os.path.join("plots_new", "nss_summary_stats.tex")
with open(latex_output_path, "w") as f:
    f.write(summary_stats.to_latex(index=True, caption="Estatísticas descritivas dos parâmetros NSS", label="tab:nss_stats", column_format="lccccc"))
