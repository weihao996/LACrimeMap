import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime as dt
import plotly.graph_objects as go
from dateutil.relativedelta import * 
from database import fetch_all_crime_as_df 

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)', 'rgb(240,240,240)']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define component functions
def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('MLEers', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/LACrimeMap/LACrimeMap'),
    ], className="row")


def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # Crime rates in Los Angeles
        ### Data Source
        LA Crime Rate analysis uses data from [Los Angeles Open Data](https://data.lacity.org/).
        The [data source](https://data.lacity.org/A-Safe-City/Arrest-Data-from-2010-to-Present/yru6-6re4) 
        **updates weekly**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

def static_stacked_trend_graph(stack=False):
    """
    Returns scatter line plot of all power sources and power load.
    If `stack` is `True`, the 4 power sources are stacked together to show the overall power
    production.
    """
    df = fetch_all_crime_as_df(allow_cached=True)
    if df is None:
        return go.Figure()
    tot = [(df[df['grp_description']==c].shape[0], i) for i, c in enumerate(desc)]
    tot.sort(reverse=True)
    tot = tot[:5]
    c = df.groupby(['grp_description','month']).count()
    #x = df['month'].unique()
    start = pd.Timestamp('2019-7-1')
    end = pd.Timestamp('2019-11-19')
    start = pd.Timestamp(dt(start.year, start.month, 1))
    end = pd.Timestamp(dt(end.year, end.month, 1))
    month_range_num = round(((end - start).days)/30)
    x_axis = [start + relativedelta(months=+i) for i in range(month_range_num + 1)]
    #x = df['month_string'].unique()
    crime = [desc[x[1]] for x in tot]
    fig = go.Figure()
    for i, s in enumerate(crime):
        count_array = c.loc[s]['rpt_id']
        count = [count_array[x] for x in x_axis]
        fig.add_trace(go.Scatter(x=x_axis, y=count, mode='lines', name=s,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup='stack' if stack else None))
    #fig.add_trace(go.Scatter(x=x, y=df['Load'], mode='lines', name='Load',
                             #line={'width': 2, 'color': 'orange'}))
    title = 'Crime incidences of each charge group'
    if stack:
        title += ' [Stacked]'

    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='Number of Crimes',
                      xaxis_title='Date')
    return fig



def what_if_description():
    """
    Returns description of "What-If" - the interactive component
    """
    return html.Div(children=[
        dcc.Markdown('''
        # " What If "
        So far, BPA has been relying on hydro power to balance the demand and supply of power. 
        Could our city survive an outage of hydro power and use up-scaled wind power as an
        alternative? Find below **what would happen with 2.5x wind power and no hydro power at 
        all**.   
        Feel free to try out more combinations with the sliders. For the clarity of demo code,
        only two sliders are included here. A fully-functioning What-If tool should support
        playing with other interesting aspects of the problem (e.g. instability of load).
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def what_if_tool():
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-figure')], className='nine columns'),

        html.Div(children=[
            html.H5("Crime Rates Time Frame", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.DatePickerRange(id='my-date-picker-range', min_date_allowed=dt(2018, 1, 1), max_date_allowed=dt(2019, 12, 13), initial_visible_month=dt(2019, 10, 1),
                start_date = dt(2018,12,1), end_date=dt(2019, 8, 1))
            ], style={'marginTop': '5rem', 'width':'40%'}),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '15%'}),
    ], className='row eleven columns')

def crime_map_description():
    """
    Returns the description of crime map.
    """
    return html.Div(children=[
        dcc.Markdown('''
        # " What If "
        crime heatmap
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")

def crime_map_tool():
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-crime')], className='ten columns'),

        html.Div(children=[
            html.H5("Crime Rates Time Frame", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.DatePickerRange(id='crime-date-picker-range', min_date_allowed=dt(2018, 1, 1), max_date_allowed=dt(2019, 12, 13), initial_visible_month=dt(2019, 10, 1),
                start_date = dt(2019,11,1), end_date=dt(2019, 11, 30))
            ], style={'marginTop': '5rem', 'width':'20%'}),
            html.Div(children=[
                dcc.Dropdown(
                id='crime-dropdown',
                options=[
                        {'label': 'Non-Violent Crimes', 'value': 'non_violent'},
                        {'label': 'Violent Crimes', 'value': 'violent'}],
                        value='non_violent')
            ], style={'marginTop': '5rem', 'width':'20%'}),
            html.Div(id='dd-output-container'),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '15%'}),
    ], className='row eleven columns')


def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Project Architecture
            This project uses MongoDB as the database. All data acquired are stored in raw form to the
            database (with de-duplication). An abstract layer is built in `database.py` so all queries
            can be done via function call. For a more complicated app, the layer will also be
            responsible for schema consistency. A `plot.ly` & `dash` app is serving this web page
            through. Actions on responsive components on the page is redirected to `app.py` which will
            then update certain components on the page.  
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                     className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''
        
        ''')
    ], className='row')


# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        description(),
        # dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
        dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=False)),
        what_if_description(),
        what_if_tool(),
        crime_map_description(),
        crime_map_tool(),
        architecture_summary(),
    ], className='row', id='content')


# set layout to a function which updates upon reloading
app.layout = dynamic_layout


# Defines the dependencies of interactive components

# @app.callback(
#     dash.dependencies.Output('output-container-date-picker-range', 'children'),
#     [dash.dependencies.Input('my-date-picker-range', 'start_date'),
#      dash.dependencies.Input('my-date-picker-range', 'end_date')])
# def update_output(start_date, end_date):
#     string_prefix = 'You have selected: '
#     if start_date is not None:
#         start_date = dt.strptime(start_date.split(' ')[0], '%Y-%m-%d')
#         start_date_string = start_date.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
#     if end_date is not None:
#         end_date = dt.strptime(end_date.split(' ')[0], '%Y-%m-%d')
#         end_date_string = end_date.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'End Date: ' + end_date_string
#     if len(string_prefix) == len('You have selected: '):
#         return 'Select a date to see it displayed here'
#     else:
#         return string_prefix

@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def what_if_handler(startdate, enddate):
    """Changes the display graph of crime rates"""
    df = fetch_all_crime_as_df(allow_cached=True)
    if df is None:
        return go.Figure()
    c = df.groupby(['grp_description','month']).count()
    crime = ['Miscellaneous Other Violations', 'Narcotic Drug Laws', 'Aggravated Assault', 'Driving Under Influence', 'Other Assaults']
    start = pd.Timestamp(startdate)
    end = pd.Timestamp(enddate)
    start = pd.Timestamp(dt(start.year, start.month, 1))
    end = pd.Timestamp(dt(end.year, end.month, 1))
    month_range_num = round(((end - start).days)/30)
    test_axis = [start + relativedelta(months=+i) for i in range(month_range_num + 1)]
    title = 'Crime counts of top five categories'
    fig = go.Figure()
    for i, s in enumerate(crime):
        count_array = c.loc[s]['rpt_id']
        count = [count_array[x] for x in test_axis]
        fig.add_trace(go.Scatter(x=test_axis, y=count, mode='lines', name=s,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup=False))
    fig.update_layout(template='plotly_dark', title=title,
                      plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='Number of crimes',
                      xaxis_title='Date')
    return fig  

@app.callback(
    dash.dependencies.Output('what-if-crime', 'figure'),
    [dash.dependencies.Input('crime-date-picker-range', 'start_date'),
     dash.dependencies.Input('crime-date-picker-range', 'end_date'),
     dash.dependencies.Input('crime-dropdown', 'value'),])
def crime_handler(startdate, enddate, crimetype):
    """Changes the display graph of crime rates"""
    df = fetch_all_crime_as_df(allow_cached=True)
    if df is None:
        return go.Figure()
    df.dropna(subset=['grp_description'],inplace=True)
    violent = ['Homicide','Aggravated Assault','Weapon (carry/poss)']
    df['crime_type'] = df['grp_description'].apply(lambda x:"violent" if x in violent else "non_violent")
    df['lat'] = pd.to_numeric(df['location_1'].apply(lambda x:x['latitude']))
    df['lon'] = pd.to_numeric(df['location_1'].apply(lambda x:x['longitude']))
    df_map = df[(df['arst_date'] <= enddate)&(df['arst_date'] >= startdate)&(df['crime_type']==crimetype)]
    title = 'Crime map'
    fig = px.scatter_mapbox(df_map, lat='lat', lon='lon', zoom=10, height=500, color='area_desc')
    
    fig.update_traces(marker=dict(size=12, opacity=0.5))
    fig.update_layout(mapbox_style="stamen-terrain")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},title=title)
    return fig  

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('crime-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)



if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')