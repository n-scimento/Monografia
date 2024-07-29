"""
import sys         
sys.path.append('D:/projects/base/app/modules') 

see more at https://realpython.com/python-import/ or https://www.geeksforgeeks.org/python-import-module-outside-directory/
"""
import os

folder_name = 'Py'
for root, dirs, files in os.walk(os.getcwd()):
    if folder_name in dirs:
        new_path = os.path.join(root, folder_name)
        os.chdir(new_path)

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd 
from bmf import real, nominal, update




#%%# Function
def visu3d(df, start_date, end_date):
    nominal = df.loc[start_date:end_date]
    nominal = nominal.reset_index().rename(columns={'index': 'Date'})
    df_long = nominal.melt(id_vars='Date', var_name='Maturity', value_name='Interest')

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

