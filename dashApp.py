import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

CSV_PATH = './csv/csvUntil81123.csv'


def load_and_preprocess_data():
    df = pd.read_csv(CSV_PATH)
    df['datetime'] = pd.to_datetime(df['date'], dayfirst=True)
    return df


# Function to create the graph
def create_hours_graph(start_date, end_date, df):
    selected_data = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
    # selected_data = df[df['datetime'].dt.date == selected_date.date()]
    hourly_alert_counts = selected_data.groupby(selected_data['hour'])['city'].count().reset_index()
    hourly_alert_counts.columns = ['Hour', 'Number of Alerts']
    fig = px.bar(hourly_alert_counts, x='Hour', y='Number of Alerts', labels={'Number of Alerts': 'Number of Alerts'},
                 title=f'Number of Alerts per Hour on {start_date.date().day}.{start_date.date().month} - '
                       f'{end_date.date().day}.{end_date.date().month}', text='Number of Alerts')

    fig.update_xaxes(range=[-0.5, 23.5], tickmode='array', tickvals=list(range(24)))

    return fig


# Function to create the graph with all minutes displayed on the x-axis
def create_minute_graph(start_date, end_date, df):
    filtered_data = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
    minute_alert_counts = filtered_data.groupby(filtered_data['minutes'])['city'].count().reset_index()
    minute_alert_counts.columns = ['Minute', 'Number of Alerts']
    fig = px.bar(minute_alert_counts, x='Minute', y='Number of Alerts',
                 labels={'Number of Alerts': 'Number of Alerts'},
                 title=f'Number of Alerts per Minute between {start_date.date().day}.{start_date.date().month} - '
                       f'{end_date.date().day}.{end_date.date().month}', text='Number of Alerts')

    # Set fixed x-axis range from 0 to 59 (60 minutes) and show all numbers for minutes
    fig.update_xaxes(range=[-0.5, 59.5], tickmode='array', tickvals=list(range(60)))

    return fig


def create_cities_graph(start_date, end_date, df, selected_cities):
    filtered_data = df[(df['city'].isin(selected_cities)) &
                       (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]

    date_alert_counts = filtered_data.groupby(filtered_data['datetime'].dt.date).size().reset_index(name='Number of Alerts')

    date_alert_counts.columns = ['Date', 'Number of Alerts']
    fig = px.bar(date_alert_counts, x='Date', y='Number of Alerts',
                 labels={'Number of Alerts': 'Number of Alerts'},
                 title=f'Number of Alerts in selected cities between {start_date.date().day}.{start_date.date().month} - '
                       f'{end_date.date().day}.{end_date.date().month}', text='Number of Alerts')

    return fig


# Function to create the Dash app
def create_app():
    app = dash.Dash(__name__)

    df = load_and_preprocess_data()

    city_options = [{'label': city, 'value': city} for city in df['city'].unique()]

    app.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Alarms per Hour in a single day', children=[
                html.Div([
                    html.Label('Select Start Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
                    dcc.DatePickerSingle(
                        id='start-date-picker',
                        min_date_allowed=df['datetime'].min(),
                        max_date_allowed=df['datetime'].max(),
                        initial_visible_month=df['datetime'].min(),
                        date=df['datetime'].min().date(),
                        style={'margin-left': '10px'}
                    ),
                ]),
                html.Div([
                    html.Label('Select End Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
                    dcc.DatePickerSingle(
                        id='end-date-picker',
                        min_date_allowed=df['datetime'].min(),
                        max_date_allowed=df['datetime'].max(),
                        initial_visible_month=df['datetime'].min(),
                        date=df['datetime'].max().date(),
                        style={'margin-left': '20px'}
                    ),
                ]),
                html.Button('Update Graph', id='update-button', n_clicks=0, style={'margin-left': '10px',
                                                                                   'font-size': '130%'}),
                html.Div(id='graph-container-hour')
            ]),
            dcc.Tab(label='Alarms per Minute in several dates ', children=[
                html.Div([
                    html.Label('Select Start Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
                    dcc.DatePickerSingle(
                        id='start-date-picker-minute',
                        min_date_allowed=df['datetime'].min(),
                        max_date_allowed=df['datetime'].max(),
                        initial_visible_month=df['datetime'].min(),
                        date=df['datetime'].min().date(),
                        style={'margin-left': '10px'}
                    ),
                ]),
                html.Div([
                    html.Label('Select End Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
                    dcc.DatePickerSingle(
                        id='end-date-picker-minute',
                        min_date_allowed=df['datetime'].min(),
                        max_date_allowed=df['datetime'].max(),
                        initial_visible_month=df['datetime'].min(),
                        date=df['datetime'].max().date(),
                        style={'margin-left': '20px'}
                    ),
                ]),
                html.Button('Update Graph', id='update-button-minute', n_clicks=0, style={'margin-left': '10px',
                                                                                          'font-size': '130%'}),
                html.Div(id='graph-container-minute')
            ]),
            dcc.Tab(label='Alarms per city in several dates', children=[
                html.Div([
                    html.Label('Select Start Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
                    dcc.DatePickerSingle(
                        id='start-date-picker-city',
                        min_date_allowed=df['datetime'].min(),
                        max_date_allowed=df['datetime'].max(),
                        initial_visible_month=df['datetime'].min(),
                        date=df['datetime'].min().date(),
                        style={'margin-left': '10px'}
                    ),
                ]),
                html.Div([
                    html.Label('Select End Date:', style={'font-weight': 'bold', 'font-size': '150%'}),
                    dcc.DatePickerSingle(
                        id='end-date-picker-city',
                        min_date_allowed=df['datetime'].min(),
                        max_date_allowed=df['datetime'].max(),
                        initial_visible_month=df['datetime'].min(),
                        date=df['datetime'].max().date(),
                        style={'margin-left': '20px'}
                    ),
                ]),
                html.Div([
                    html.Label('Select Cities:',
                               style={'font-weight': 'bold', 'font-size': '150%', 'margin-top': '20px'}),
                    dcc.Dropdown(
                        id='city-dropdown',
                        options=city_options,
                        multi=True,
                        searchable=True,
                        style={'width': '50%'}
                    ),
                ]),
                html.Div([
                    html.Button('Update Graph', id='update-button-city', n_clicks=0,
                                style={'margin-left': '10px', 'margin-top': '10px', 'font-size': '130%'}),
                ]),
                html.Div(id='graph-container-city')
            ]),
        ])
    ])

    # Define the callback to update the graph based on user input
    @app.callback(
        dash.dependencies.Output('graph-container-hour', 'children'),
        [dash.dependencies.Input('update-button', 'n_clicks')],
        [dash.dependencies.State('start-date-picker', 'date'),
         dash.dependencies.State('end-date-picker', 'date')]
    )
    def update_graph_callback(n_clicks, start_date, end_date):
        if n_clicks > 0:
            fig = create_hours_graph(pd.to_datetime(start_date), pd.to_datetime(end_date), df)
            return dcc.Graph(figure=fig)

    # Define callback for Minute-Level Graph tab
    @app.callback(
        dash.dependencies.Output('graph-container-minute', 'children'),
        [dash.dependencies.Input('update-button-minute', 'n_clicks')],
        [dash.dependencies.State('start-date-picker-minute', 'date'),
         dash.dependencies.State('end-date-picker-minute', 'date')]
    )
    def update_minute_graph_callback(n_clicks, start_date, end_date):
        if n_clicks > 0:
            fig = create_minute_graph(pd.to_datetime(start_date), pd.to_datetime(end_date), df)
            return dcc.Graph(figure=fig)

    # Define callback for Date-Level Graph tab
    @app.callback(
        dash.dependencies.Output('graph-container-city', 'children'),
        [dash.dependencies.Input('update-button-city', 'n_clicks')],
        [dash.dependencies.State('city-dropdown', 'value'),
         dash.dependencies.State('start-date-picker-city', 'date'),
         dash.dependencies.State('end-date-picker-city', 'date')]
    )
    def update_date_graph_callback(n_clicks, selected_cities, start_date, end_date):
        if n_clicks > 0:

            fig = create_cities_graph(pd.to_datetime(start_date), pd.to_datetime(end_date), df, selected_cities)
            return dcc.Graph(figure=fig)


    return app


def startApp():
    app = create_app()
    app.run_server(debug=True)
