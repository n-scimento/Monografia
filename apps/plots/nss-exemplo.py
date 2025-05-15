import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

df = pd.read_excel('data/nss-2006-10-16.xlsx')

# Define groups with one series per chart


groups = {
    'Beta 1': {'col': 'beta1', 'title': 'Nível (β1)', 'y_label': '%'},
    'Beta 2': {'col': 'beta2', 'title': 'Decaimento (β2)', 'y_label': '%'},
    'Beta 3': {'col': 'beta3', 'title': 'Primeira Curvatura (β3)', 'y_label': '%'},
    'Beta 4': {'col': 'beta4', 'title': 'Segunda Curvatura (β4)', 'y_label': '%'},
    'Fit': {'col': 'Fit', 'title': 'Curva NSS', 'y_label': 'Taxa % a.a.'},
}

# Layout configuration
n_groups = len(groups)
n_cols = 2
n_rows = (n_groups + 1) // 2  # add 1 to ensure room for an extra wide row

fig = plt.figure(figsize=(14, 4 * n_rows))
gs = gridspec.GridSpec(n_rows, n_cols, figure=fig)

# Plot each group
axes = []
for idx, (name, attributes) in enumerate(groups.items()):
    row, col = divmod(idx, n_cols)

    # If it's the last chart and it would be alone in its row, span two columns
    if idx == n_groups - 1 and n_groups % 2 != 0:
        ax = fig.add_subplot(gs[row, :])  # span both columns
    else:
        ax = fig.add_subplot(gs[row, col])

    axes.append(ax)
    col_data = attributes['col']
    ax.plot(df['Maturity'], df[col_data] * 100, color='#08306b')
    ax.set_title(attributes['title'], fontsize=10)
    ax.set_ylabel(attributes['y_label'])
    ax.set_xlabel('Maturidade (anos)')
    ax.grid(True)
    ax.legend(loc='best', fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.suptitle("Curva Nelson-Siegel-Svensson - Decomposição por Componente", fontsize=14)

# Save the figure
output_path = "apps/var/plots_new/nss_decomposition.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.close()
