#%%# Reading data and setting libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default='browser'

#%%# 3D plot
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

#%%# Flat plot 

def flat_plot(df, dates, plot_types):
    """plot_yield_curve
    Plot yield curves from a DataFrame using Plotly.

    Parameters:
    - df (pd.DataFrame): DataFrame with dates as the index and maturity of yield curves as columns.
    - dates (list of str): List of dates for which to plot the series. Each date must be in 'YYYY-MM-DD' format.
    - plot_types (list of str): List of plot types corresponding to each date. 
      Can be 'lines', 'markers', or 'lines+markers'.

    Returns:
    - None: Displays the plot using Plotly.
    """
    if len(dates) != len(plot_types):
        raise ValueError("Length of dates and plot_types must be the same.")
    
    traces = []
    for date, plot_type in zip(dates, plot_types):
        # Convert the date strings to pandas Timestamp objects
        date = pd.Timestamp(date)
        
        # Check if the date exists in the DataFrame
        if date not in df.index:
            raise ValueError(f"Date {date} not found in DataFrame index.")
        
        trace = go.Scatter(x=df.columns, y=df.loc[date], mode=plot_type, name=f'Series for {date}')
        traces.append(trace)
    
    # Create the layout
    layout = go.Layout(
        title='Yield Curve Plot',
        xaxis_title='Maturity',
        yaxis_title='Yield',
        legend_title='Series'
    )
    
    # Create the figure and show the plot
    fig = go.Figure(data=traces, layout=layout)
    fig.show()
