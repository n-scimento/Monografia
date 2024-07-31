# -*- coding: utf-8 -*-
"""
Next steps:
    2D visualization
    Surface visualization
"""
#%%# Reading data and setting libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default='browser'


def dim_plot(df, start_date = None, end_date = None, lim = [0,15]):
    
    """
    Parameters
    ----------
    df : melted dataframe

    start_date : str, 'yyyy-mm-dd'
        By default it will use all the range.
    
    end_date : str, 'yyyy-mm-dd'
        By default it will use all the range. 
    
    lim : list with the limits of the Interest rate.
        The default is [0,15].

    Returns
    -------
    None.

    """
    
    if start_date != None:
        df = df.loc[start_date:end_date]
    
    df = df.reset_index().rename(columns={'index': 'Date'})
    df = df.melt(id_vars='Date', var_name='Maturity', value_name='Interest')

    trace = go.Scatter3d(
        x=df['Date'],
        y=df['Maturity'],
        z=df['Interest'],
        mode='markers',
        marker=dict(
            size= 1,
            color=df['Interest'],  
            colorscale='inferno',  
            cmin=lim[0],                    
            cmax=lim[1],
            opacity=0.7
        )
    )

    fig = go.Figure(data=[trace])

    fig.update_layout(scene=dict(
        xaxis_title='Date',
        yaxis_title='Maturity',
        zaxis=dict(title = 'Interest Rate', range = lim)
    ), title='Yield Curve 3D Scatter Plot')

    fig.show()
