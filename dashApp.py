# import sqlite3
#
# import pandas as pd
# import plotly.express as px
# import dash
# from dash import dcc, html
#
# from AddingData import ROCKETS_TABLE_NAME, TERRORISTS_TABLE_NAME, AIRCRAFT_TABLE_NAME
#
# CSV_PATH = './csv/csvUpdated.csv'
# DB_PATH = '.\\csv\\newData\\alerts.db'
#
#
# def load_and_preprocess_data(CSV_Flag=False):
#     if CSV_Flag:
#         df = pd.read_csv(CSV_PATH)
#     else:
#         cnx = sqlite3.connect(DB_PATH)
#         df = pd.read_sql_query(f"SELECT * FROM {ROCKETS_TABLE_NAME}", cnx)
#     df['datetime'] = pd.to_datetime(df['dates'], dayfirst=True)
#     return df
#
#
# # Function to create the graph
# def create_hours_graph(start_date, end_date, df):
#     selected_data = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
#     # selected_data = df[df['datetime'].dt.date == selected_date.date()]
#     hourly_alert_counts = selected_data.groupby(selected_data['hour'])['city'].count().reset_index()
#     hourly_alert_counts.columns = ['Hour', 'Number of Alerts']
#     fig = px.bar(hourly_alert_counts, x='Hour', y='Number of Alerts', labels={'Number of Alerts': 'Number of Alerts'},
#                  title=f'Number of Alerts per Hour on {start_date.date().day}.{start_date.date().month} - '
#                        f'{end_date.date().day}.{end_date.date().month}', text='Number of Alerts')
#
#     fig.update_xaxes(range=[-0.5, 23.5], tickmode='array', tickvals=list(range(24)))
#
#     return fig
#
#
# # Function to create the graph with all minutes displayed on the x-axis
# def create_minute_graph(start_date, end_date, df):
#     filtered_data = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
#     minute_alert_counts = filtered_data.groupby(filtered_data['minutes'])['city'].count().reset_index()
#     minute_alert_counts.columns = ['Minute', 'Number of Alerts']
#     fig = px.bar(minute_alert_counts, x='Minute', y='Number of Alerts',
#                  labels={'Number of Alerts': 'Number of Alerts'},
#                  title=f'Number of Alerts per Minute between {start_date.date().day}.{start_date.date().month} - '
#                        f'{end_date.date().day}.{end_date.date().month}', text='Number of Alerts')
#
#     # Set fixed x-axis range from 0 to 59 (60 minutes) and show all numbers for minutes
#     fig.update_xaxes(range=[-0.5, 59.5], tickmode='array', tickvals=list(range(60)))
#
#     return fig
#
#
# def create_cities_graph(start_date, end_date, df, selected_cities):
#     filtered_data = df[(df['city'].isin(selected_cities)) &
#                        (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
#
#     date_alert_counts = filtered_data.groupby(filtered_data['datetime'].dt.date).size().reset_index(
#         name='Number of Alerts')
#
#     date_alert_counts.columns = ['Date', 'Number of Alerts']
#     fig = px.bar(date_alert_counts, x='Date', y='Number of Alerts',
#                  labels={'Number of Alerts': 'Number of Alerts'},
#                  title=f'Number of Alerts in selected cities between {start_date.date().day}.{start_date.date().month} - '
#                        f'{end_date.date().day}.{end_date.date().month}', text='Number of Alerts')
#
#     return fig
#
#
# # Function to create the Dash app
# def create_app():
#     app = dash.Dash(__name__)
#
#     df = load_and_preprocess_data()
#
#     city_options = [{'label': city, 'value': city} for city in df['city'].unique()]
#
#     app.layout = html.Div([
#         dcc.Tabs([
#             dcc.Tab(label='Alarms per Hour in a single day', children=[
#                 html.Div([
#                     html.Label('Select Start Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
#                     dcc.DatePickerSingle(
#                         id='start-date-picker',
#                         min_date_allowed=df['datetime'].min(),
#                         max_date_allowed=df['datetime'].max(),
#                         initial_visible_month=df['datetime'].min(),
#                         date=df['datetime'].min().date(),
#                         style={'margin-left': '10px'}
#                     ),
#                 ]),
#                 html.Div([
#                     html.Label('Select End Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
#                     dcc.DatePickerSingle(
#                         id='end-date-picker',
#                         min_date_allowed=df['datetime'].min(),
#                         max_date_allowed=df['datetime'].max(),
#                         initial_visible_month=df['datetime'].min(),
#                         date=df['datetime'].max().date(),
#                         style={'margin-left': '20px'}
#                     ),
#                 ]),
#                 html.Button('Update Graph', id='update-button', n_clicks=0, style={'margin-left': '10px',
#                                                                                    'font-size': '130%'}),
#                 html.Div(id='graph-container-hour')
#             ]),
#             dcc.Tab(label='Alarms per Minute in several dates ', children=[
#                 html.Div([
#                     html.Label('Select Start Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
#                     dcc.DatePickerSingle(
#                         id='start-date-picker-minute',
#                         min_date_allowed=df['datetime'].min(),
#                         max_date_allowed=df['datetime'].max(),
#                         initial_visible_month=df['datetime'].min(),
#                         date=df['datetime'].min().date(),
#                         style={'margin-left': '10px'}
#                     ),
#                 ]),
#                 html.Div([
#                     html.Label('Select End Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
#                     dcc.DatePickerSingle(
#                         id='end-date-picker-minute',
#                         min_date_allowed=df['datetime'].min(),
#                         max_date_allowed=df['datetime'].max(),
#                         initial_visible_month=df['datetime'].min(),
#                         date=df['datetime'].max().date(),
#                         style={'margin-left': '20px'}
#                     ),
#                 ]),
#                 html.Button('Update Graph', id='update-button-minute', n_clicks=0, style={'margin-left': '10px',
#                                                                                           'font-size': '130%'}),
#                 html.Div(id='graph-container-minute')
#             ]),
#             dcc.Tab(label='Alarms per city in several dates', children=[
#                 html.Div([
#                     html.Label('Select Start Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
#                     dcc.DatePickerSingle(
#                         id='start-date-picker-city',
#                         min_date_allowed=df['datetime'].min(),
#                         max_date_allowed=df['datetime'].max(),
#                         initial_visible_month=df['datetime'].min(),
#                         date=df['datetime'].min().date(),
#                         style={'margin-left': '10px'}
#                     ),
#                 ]),
#                 html.Div([
#                     html.Label('Select End Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
#                     dcc.DatePickerSingle(
#                         id='end-date-picker-city',
#                         min_date_allowed=df['datetime'].min(),
#                         max_date_allowed=df['datetime'].max(),
#                         initial_visible_month=df['datetime'].min(),
#                         date=df['datetime'].max().date(),
#                         style={'margin-left': '20px'}
#                     ),
#                 ]),
#                 html.Div([
#                     html.Label('Select Cities:',
#                                style={'font-weight': 'bold', 'font-size': '150%', 'margin-top': '20px'}),
#                     dcc.Dropdown(
#                         id='city-dropdown',
#                         options=city_options,
#                         multi=True,
#                         searchable=True,
#                         style={'width': '50%'}
#                     ),
#                 ]),
#                 html.Div([
#                     html.Button('Update Graph', id='update-button-city', n_clicks=0,
#                                 style={'margin-left': '10px', 'margin-top': '10px', 'font-size': '130%'}),
#                 ]),
#                 html.Div(id='graph-container-city')
#             ]),
#             dcc.Tab(label='Alarms in All Cities', children=[
#                 html.Div([
#                     html.Label('Select Start Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
#                     dcc.DatePickerSingle(
#                         id='start-date-picker-all-cities',
#                         min_date_allowed=df['datetime'].min(),
#                         max_date_allowed=df['datetime'].max(),
#                         initial_visible_month=df['datetime'].min(),
#                         date=df['datetime'].min().date(),
#                         style={'margin-left': '10px'}
#                     ),
#                 ]),
#                 html.Div([
#                     html.Label('Select End Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
#                     dcc.DatePickerSingle(
#                         id='end-date-picker-all-cities',
#                         min_date_allowed=df['datetime'].min(),
#                         max_date_allowed=df['datetime'].max(),
#                         initial_visible_month=df['datetime'].min(),
#                         date=df['datetime'].max().date(),
#                         style={'margin-left': '20px'}
#                     ),
#                 ]),
#                 html.Button('Update Graph', id='update-button-all-cities', n_clicks=0,
#                             style={'margin-left': '10px', 'font-size': '130%'}),
#                 html.Div(id='graph-container-all-cities')
#             ])
#         ])
#     ])
#
#     # Define the callback to update the graph based on user input
#     @app.callback(
#         dash.dependencies.Output('graph-container-hour', 'children'),
#         [dash.dependencies.Input('update-button', 'n_clicks')],
#         [dash.dependencies.State('start-date-picker', 'date'),
#          dash.dependencies.State('end-date-picker', 'date')]
#     )
#     def update_graph_callback(n_clicks, start_date, end_date):
#         if n_clicks > 0:
#             fig = create_hours_graph(pd.to_datetime(start_date), pd.to_datetime(end_date), df)
#             return dcc.Graph(figure=fig)
#
#     # Define callback for Minute-Level Graph tab
#     @app.callback(
#         dash.dependencies.Output('graph-container-minute', 'children'),
#         [dash.dependencies.Input('update-button-minute', 'n_clicks')],
#         [dash.dependencies.State('start-date-picker-minute', 'date'),
#          dash.dependencies.State('end-date-picker-minute', 'date')]
#     )
#     def update_minute_graph_callback(n_clicks, start_date, end_date):
#         if n_clicks > 0:
#             fig = create_minute_graph(pd.to_datetime(start_date), pd.to_datetime(end_date), df)
#             return dcc.Graph(figure=fig)
#
#     # Define callback for Date-Level Graph tab
#     @app.callback(
#         dash.dependencies.Output('graph-container-city', 'children'),
#         [dash.dependencies.Input('update-button-city', 'n_clicks')],
#         [dash.dependencies.State('city-dropdown', 'value'),
#          dash.dependencies.State('start-date-picker-city', 'date'),
#          dash.dependencies.State('end-date-picker-city', 'date')]
#     )
#     def update_date_graph_callback(n_clicks, selected_cities, start_date, end_date):
#         if n_clicks > 0:
#             fig = create_cities_graph(pd.to_datetime(start_date), pd.to_datetime(end_date), df, selected_cities)
#             return dcc.Graph(figure=fig)
#
#     # Define the callback to update the graph for the new tab
#     @app.callback(
#         dash.dependencies.Output('graph-container-all-cities', 'children'),
#         [dash.dependencies.Input('update-button-all-cities', 'n_clicks')],
#         [dash.dependencies.State('start-date-picker-all-cities', 'date'),
#          dash.dependencies.State('end-date-picker-all-cities', 'date')]
#     )
#     def update_all_cities_graph_callback(n_clicks, start_date, end_date):
#         start_date = pd.to_datetime(start_date)
#         end_date = pd.to_datetime(end_date)
#         if n_clicks > 0:
#             filtered_data = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
#
#             date_alert_counts = filtered_data.groupby(filtered_data['datetime'].dt.date).size().reset_index(
#                 name='Number of Alerts')
#
#             date_alert_counts.columns = ['Date', 'Number of Alerts']
#             fig = px.bar(date_alert_counts, x='Date', y='Number of Alerts',
#                          labels={'Number of Alerts': 'Number of Alerts'},
#                          title=f'Number of Alerts in all cities between {start_date.date().day}.{start_date.date().month} - '
#                                f'{end_date.date().day}.{end_date.date().month}', text='Number of Alerts')
#
#             return dcc.Graph(figure=fig)
#         else:
#             return None
#
#     return app
#
#
# def startApp():
#     app = create_app()
#     app.run_server(debug=True)


import sqlite3
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from AddingData import ROCKETS_TABLE_NAME, TERRORISTS_TABLE_NAME, AIRCRAFT_TABLE_NAME

CSV_PATH = './csv/csvUpdated.csv'
DB_PATH = '.\\csv\\newData\\alerts.db'

# Function to load and preprocess data from the selected table
def load_and_preprocess_data(table_name, CSV_Flag=False):
    if CSV_Flag:
        df = pd.read_csv(CSV_PATH)
    else:
        cnx = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", cnx)
    df['datetime'] = pd.to_datetime(df['dates'], dayfirst=True)
    return df

# Function to create the graph for hours
def create_hours_graph(start_date, end_date, df):
    selected_data = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
    hourly_alert_counts = selected_data.groupby(selected_data['hour'])['city'].count().reset_index()
    hourly_alert_counts.columns = ['Hour', 'Number of Alerts']
    fig = px.bar(hourly_alert_counts, x='Hour', y='Number of Alerts',
                 title=f'Number of Alerts per Hour from {start_date.date()} to {end_date.date()}')
    fig.update_xaxes(range=[-0.5, 23.5], tickmode='array', tickvals=list(range(24)))
    return fig

# Function to create the graph for minutes
def create_minute_graph(start_date, end_date, df):
    filtered_data = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
    minute_alert_counts = filtered_data.groupby(filtered_data['minutes'])['city'].count().reset_index()
    minute_alert_counts.columns = ['Minute', 'Number of Alerts']
    fig = px.bar(minute_alert_counts, x='Minute', y='Number of Alerts',
                 title=f'Number of Alerts per Minute from {start_date.date()} to {end_date.date()}')
    fig.update_xaxes(range=[-0.5, 59.5], tickmode='array', tickvals=list(range(60)))
    return fig

# Function to create the graph for selected cities
def create_cities_graph(start_date, end_date, df, selected_cities):
    filtered_data = df[(df['city'].isin(selected_cities)) &
                       (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
    date_alert_counts = filtered_data.groupby(filtered_data['datetime'].dt.date).size().reset_index(name='Number of Alerts')
    fig = px.bar(date_alert_counts, x='Date', y='Number of Alerts',
                 title=f'Number of Alerts in Selected Cities from {start_date.date()} to {end_date.date()}')
    return fig

# Function to create the Dash app
def getDropDown(idName):
    return dcc.Dropdown(
                        id=f'table-dropdown-{idName}',
                        options=[
                            {'label': 'Rockets', 'value': ROCKETS_TABLE_NAME},
                            {'label': 'Aircraft', 'value': AIRCRAFT_TABLE_NAME},
                            {'label': 'Terrorists', 'value': TERRORISTS_TABLE_NAME}
                        ],
                        multi=True,
                        value=[ROCKETS_TABLE_NAME],  # Default selection
                        style={'width': '50%'},
                        placeholder="Select Origin"
                    )


def getDFANdDates(start_date, end_date, selected_tables):
    # Load data from the selected tables
    dfs = []
    for table in selected_tables:
        cnx = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {table}", cnx)
        df['datetime'] = pd.to_datetime(df['dates'], dayfirst=True)
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    return start_date, end_date, combined_df


def create_app():
    app = dash.Dash(__name__)

    table_options = [
        {'label': 'Missiles', 'value': ROCKETS_TABLE_NAME},
        {'label': 'Aircraft', 'value': AIRCRAFT_TABLE_NAME},
        {'label': 'Terrorists', 'value': TERRORISTS_TABLE_NAME}
    ]

    app.layout = html.Div([
        dcc.Tabs([

            dcc.Tab(label='Alarms per Hour', children=[
                html.Div([
                    getDropDown('hour'),
                    html.Label('Select Start Date:'),
                    dcc.DatePickerSingle(id='start-date-picker-hour', date=pd.to_datetime('10-08-2023').date()),
                    html.Label('Select End Date:'),
                    dcc.DatePickerSingle(id='end-date-picker-hour', date=pd.to_datetime('today').date()),
                    html.Button('Update Graph', id='update-button-hour', n_clicks=0),
                    html.Div(id='graph-container-hour')
                ])
            ]),

            dcc.Tab(label='Alarms per Minute', children=[
                html.Div([
                    getDropDown('minute'),
                    html.Label('Select Start Date:'),
                    dcc.DatePickerSingle(id='start-date-picker-minute', date=pd.to_datetime('10-08-2023').date()),
                    html.Label('Select End Date:'),
                    dcc.DatePickerSingle(id='end-date-picker-minute', date=pd.to_datetime('today').date()),
                    html.Button('Update Graph', id='update-button-minute', n_clicks=0),
                    html.Div(id='graph-container-minute')
                ])
            ]),

            dcc.Tab(label='Alarms per City', children=[
                html.Div([
                    getDropDown('city'),
                    html.Label('Select Start Date:'),
                    dcc.DatePickerSingle(id='start-date-picker-city', date=pd.to_datetime('10-08-2023').date()),
                    html.Label('Select End Date:'),
                    dcc.DatePickerSingle(id='end-date-picker-city', date=pd.to_datetime('today').date()),
                    dcc.Dropdown(id='city-dropdown', multi=True, searchable=True, style={'width': '50%'}, placeholder="Select a city"),
                    html.Button('Update Graph', id='update-button-city', n_clicks=0),
                    html.Div(id='graph-container-city')
                ])
            ]),

            dcc.Tab(label='Alarms in All Cities', children=[
                html.Div([
                    getDropDown('all-cities'),
                    html.Label('Select Start Date:'),
                    dcc.DatePickerSingle(
                        id='start-date-picker-all-cities',
                        date=pd.to_datetime('10-08-2023').date()
                    ),
                    html.Label('Select End Date:'),
                    dcc.DatePickerSingle(
                        id='end-date-picker-all-cities',
                        date=pd.to_datetime('today').date()
                    ),
                    html.Button('Update Graph', id='update-button-all-cities', n_clicks=0),
                    html.Div(id='graph-container-all-cities')
                ])
            ])
        ])
    ])



    # Correct the callback for 'Alarms in All Cities' to load data inside the function
    @app.callback(
        dash.dependencies.Output('graph-container-all-cities', 'children'),
        [dash.dependencies.Input('update-button-all-cities', 'n_clicks')],
        [dash.dependencies.State('start-date-picker-all-cities', 'date'),
         dash.dependencies.State('end-date-picker-all-cities', 'date'),
         dash.dependencies.State('table-dropdown-all-cities', 'value')]
    )
    def update_all_cities_graph_callback(n_clicks, start_date, end_date, selected_tables):
        if n_clicks > 0 and selected_tables:
            start_date, end_date, combined_df = getDFANdDates(start_date, end_date, selected_tables)

            # Filter data within the selected date range
            filtered_data = combined_df[(combined_df['datetime'].dt.date >= start_date) &
                                        (combined_df['datetime'].dt.date <= end_date)]

            # Group by date and count the number of alerts
            date_alert_counts = filtered_data.groupby(filtered_data['datetime'].dt.date).size().reset_index(
                name='Number of Alerts')

            date_alert_counts.columns = ['Date', 'Number of Alerts']
            fig = px.bar(date_alert_counts, x='Date', y='Number of Alerts',
                         labels={'Number of Alerts': 'Number of Alerts'},
                         title=f'Number of Alerts in selected cities between {start_date.date().day}.{start_date.date().month} - '
                               f'{end_date.date().day}.{end_date.date().month}', text='Number of Alerts')

            return dcc.Graph(figure=fig)
        else:
            return None



    @app.callback(
        dash.dependencies.Output('graph-container-hour', 'children'),
        [dash.dependencies.Input('update-button-hour', 'n_clicks')],
        [dash.dependencies.State('start-date-picker-hour', 'date'),
         dash.dependencies.State('end-date-picker-hour', 'date'),
         dash.dependencies.State('table-dropdown-hour', 'value')]
    )
    def update_hour_graph_callback(n_clicks, start_date, end_date, selected_tables):
        if n_clicks > 0 and selected_tables:
            # Load data from the selected tables
            start_date, end_date, combined_df = getDFANdDates(start_date, end_date, selected_tables)

            # Filter data within the selected date range
            filtered_data = combined_df[(combined_df['datetime'].dt.date >= start_date) &
                                        (combined_df['datetime'].dt.date <= end_date)]

            # Group by hour and count alerts
            hourly_alert_counts = filtered_data.groupby(filtered_data['hour'])['city'].count().reset_index()
            hourly_alert_counts.columns = ['Hour', 'Number of Alerts']

            fig = px.bar(hourly_alert_counts, x='Hour', y='Number of Alerts',
                         title=f'Number of Alerts per Hour between {start_date.date()} - {end_date.date()}',
                         labels={'Number of Alerts': 'Number of Alerts'}, text='Number of Alerts')

            fig.update_xaxes(range=[-0.5, 23.5], tickmode='array', tickvals=list(range(24)))

            return dcc.Graph(figure=fig)
        else:
            return None




    # Callback to update the minute graph
    @app.callback(
        dash.dependencies.Output('graph-container-minute', 'children'),
        [dash.dependencies.Input('update-button-minute', 'n_clicks')],
        [dash.dependencies.State('start-date-picker-minute', 'date'),
         dash.dependencies.State('end-date-picker-minute', 'date'),
         dash.dependencies.State('table-dropdown-minute', 'value')]
    )
    def update_minute_graph_callback(n_clicks, start_date, end_date, selected_tables):
        if n_clicks > 0 and selected_tables:
            # Load data from the selected tables
            start_date, end_date, combined_df = getDFANdDates(start_date, end_date, selected_tables)

            # Filter data within the selected date range
            filtered_data = combined_df[(combined_df['datetime'].dt.date >= start_date) &
                                        (combined_df['datetime'].dt.date <= end_date)]

            # Group by minute and count alerts
            minute_alert_counts = filtered_data.groupby(filtered_data['minutes'])['city'].count().reset_index()
            minute_alert_counts.columns = ['Minute', 'Number of Alerts']

            fig = px.bar(minute_alert_counts, x='Minute', y='Number of Alerts',
                         title=f'Number of Alerts per Minute between {start_date.date()} - {end_date.date()}',
                         labels={'Number of Alerts': 'Number of Alerts'}, text='Number of Alerts')

            fig.update_xaxes(range=[-0.5, 59.5], tickmode='array', tickvals=list(range(60)))

            return dcc.Graph(figure=fig)
        else:
            return None



    @app.callback(
        dash.dependencies.Output('graph-container-city', 'children'),
        [dash.dependencies.Input('update-button-city', 'n_clicks')],
        [dash.dependencies.State('start-date-picker-city', 'date'),
         dash.dependencies.State('end-date-picker-city', 'date'),
         dash.dependencies.State('city-dropdown', 'value'),
         dash.dependencies.State('table-dropdown-city', 'value')]
    )
    def update_city_graph_callback(n_clicks, start_date, end_date, selected_cities, selected_tables):
        if n_clicks > 0 and selected_tables and selected_cities:
            # Load data from the selected tables
            start_date, end_date, combined_df = getDFANdDates(start_date, end_date, selected_tables)

            # Filter data within the selected date range and cities
            filtered_data = combined_df[(combined_df['city'].isin(selected_cities)) &
                                        (combined_df['datetime'].dt.date >= start_date) &
                                        (combined_df['datetime'].dt.date <= end_date)]

            # Group by date and count alerts
            date_alert_counts = filtered_data.groupby(filtered_data['datetime'].dt.date).size().reset_index(
                name='Number of Alerts')
            date_alert_counts.columns = ['Date', 'Number of Alerts']

            fig = px.bar(date_alert_counts, x='Date', y='Number of Alerts',
                         title=f'Number of Alerts in selected cities between {start_date.date()} - {end_date.date()}',
                         labels={'Number of Alerts': 'Number of Alerts'}, text='Number of Alerts')

            return dcc.Graph(figure=fig)
        else:
            return None

    #Callback to update the city dropdown based on selected table
    @app.callback(
        dash.dependencies.Output('city-dropdown', 'options'),
        [dash.dependencies.Input('table-dropdown-city', 'value')]
    )
    def update_city_dropdown_options(selected_tables):
        if not selected_tables:
            return []  # Return empty options if no tables are selected

        # Load data from selected tables and get unique cities
        dfs = []
        for table in selected_tables:
            cnx = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query(f"SELECT * FROM {table}", cnx)
            dfs.append(df)

        combined_df = pd.concat(dfs, ignore_index=True)
        unique_cities = combined_df['city'].unique()  # Get unique cities

        # Return options formatted for dropdown
        return [{'label': city, 'value': city} for city in unique_cities]

    return app

# Start the app
def startApp():
    app = create_app()
    app.run_server(debug=True)
