# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%# Reading data and setting libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default='browser'

df_real_raw = pd.read_csv('//home//nascimento//Documents//Monografia//Data//BMF//Raw//ipca.csv', index_col = 0)
df_nominal_raw = pd.read_csv('//home//nascimento//Documents//Monografia//Data//BMF//Raw//pre.csv', index_col = 0)

start_date = '2020-01-01'
end_date = '2023-12-31'

nominal = df_nominal_raw.loc[start_date:end_date]

nominal = nominal.reset_index().rename(columns={'index': 'Date'})

df_long = nominal.melt(id_vars='Date', var_name='Maturity', value_name='Interest')

#%%# Plotting it scattered

trace = go.Scatter3d(
    x=df_long['Date'],
    y=df_long['Maturity'],
    z=df_long['Interest'],
    mode='markers',
    marker=dict(
        size= 1,
        color=df_long['Interest'],  # Set color to interest
        colorscale='inferno',  
        cmin=0,                     # Set the minimum value for the colorscale
        cmax=15,
        opacity=0.7
    )
)

# Create a figure
fig = go.Figure(data=[trace])

# Update layout
fig.update_layout(scene=dict(
    xaxis_title='Date',
    yaxis_title='Maturity',
    zaxis=dict(title = 'Interest Rate', range = [0,15])
), title='Yield Curve 3D Scatter Plot')

# Show the figure in the browser
fig.show()

#%%# Plotting it as a surface - we need full data to do it 

pivot_df = df_long.pivot(index='Maturity', columns='Date', values='Interest')

# Create mesh grid for plotting
x = pivot_df.columns
y = pivot_df.index
z = pivot_df.values

# Create a surface plot
trace = go.Surface(
    x=x,
    y=y,
    z=z,
    colorscale='inferno',
    cmin=0,     # Set the minimum value for the colorscale
    cmax=10     # Set the maximum value for the colorscale
)

# Create a figure
fig = go.Figure(data=[trace])

# Update layout with max z-axis limit
fig.update_layout(
    scene=dict(
        xaxis_title='Date',
        yaxis_title='Maturity',
        zaxis=dict(
            title='Interest Rate',
            range=[0, 10]  # Set the range for the z-axis
        )
    ),
    title='Yield Curve 3D Surface Plot'
)

# Show the figure in the browser
fig.show()


