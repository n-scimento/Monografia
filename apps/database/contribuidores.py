import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

root_path = 'data/bcb/'
def contr(table):

    df_raw = pd.read_csv(f"{root_path}{table}.csv")

    df_pivot = pd.pivot_table(df_raw, values='numeroRespondentes', columns='DataReferencia', index='Data')
    df_pivot.index = pd.to_datetime(df_pivot.index)

    df = pd.DataFrame(index=df_pivot.index, columns=['year', 't0', 't1', 't2', 't3'])
    df['year'] = df.index.year

    for i in range(4):
        year_col = df['year'] + i
        df[f't{i}'] = [
            df_pivot.loc[date, year] if year in df_pivot.columns else None
            for date, year in zip(df.index, year_col)
        ]

    df.drop('year', axis=1, inplace=True)

    df.to_csv(f'data/bcb/contr_{table}.csv')

    return df

df_ipca = contr('ipca_anual_raw')
df_selic = contr('selic_anual_raw')
df_pib = contr('pib_anual_raw')
df_usd = contr('usd_anual_raw')

groups = {
    'IPCA': {
        'df': df_ipca,
        'title': 'IPCA',
    },
    'SELIC': {
        'df': df_selic,
        'title': 'SELIC',
    },
    'USD': {
        'df': df_usd,
        'title': 'Câmbio',
    },
    'PIB': {
        'df': df_pib,
        'title': 'PIB',
    },
}

# Setup figure
n_groups = len(groups)
n_cols = 2
n_rows = (n_groups + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows), squeeze=False)
axes = axes.flatten()

# Plot
for idx, (group_name, attributes) in enumerate(groups.items()):
    ax = axes[idx]
    df = attributes['df']
    cols = ['t3', 't2', 't1', 't0']  # From most distant to most current forecast
    n_colors = len(cols)
    color_range = np.linspace(0.3, 1.0, n_colors)
    cmap = plt.colormaps['Blues']

    for i, (col, cval) in enumerate(zip(cols, color_range)):
        if col in df.columns:
            ax.plot(df.index, df[col], color=cmap(cval), label=col)



    ax.set_title(attributes['title'], fontsize=10)
    ax.grid(True)
    ax.legend(loc='best', fontsize=8)

# Remove unused axes
for j in range(idx + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.suptitle("Número de respondentes FOCUS por variável e ano", fontsize=14)

# Save
output_path =  "apps/var/plots_new/contr_focus.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.close()