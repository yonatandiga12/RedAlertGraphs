import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

CSV_PATH = './csv/csvUntil41123.csv'


def load_and_preprocess_data():
    df = pd.read_csv(CSV_PATH)
    df['datetime'] = pd.to_datetime(df['date'], dayfirst=True)
    return df

# Function to create the graph
def create_graph(selected_date, df):
    selected_data = df[df['datetime'].dt.date == selected_date.date()]
    hourly_alert_counts = selected_data.groupby(selected_data['hour'])['city'].count().reset_index()
    hourly_alert_counts.columns = ['Hour', 'Number of Alerts']
    fig = px.bar(hourly_alert_counts, x='Hour', y='Number of Alerts', labels={'Number of Alerts': 'Number of Alerts'},
                 title=f'Number of Alerts per Hour on {selected_date.date().day}.{selected_date.date().month}')

    fig.update_xaxes(range=[-0.5, 23.5], tickmode='array', tickvals=list(range(24)))

    return fig



# Function to create the Dash app
def create_app():
    app = dash.Dash(__name__)

    df = load_and_preprocess_data()

    # Define the layout of the app
    # app.layout = html.Div([
    #     html.Label('Select Date:'),
    #     dcc.DatePickerSingle(
    #         id='date-picker',
    #         min_date_allowed=df['datetime'].min(),
    #         max_date_allowed=df['datetime'].max(),
    #         initial_visible_month=df['datetime'].min(),
    #         date=df['datetime'].min().date()
    #     ),
    #     html.Button('Update Graph', id='update-button', n_clicks=0),
    #     html.Div(id='graph-container')
    # ])

    app.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Alarms per Hour in a single day', children=[
                html.Label('Select Date to display:', style={'font-weight': 'bold', 'font-size': '150%'}),
                dcc.DatePickerSingle(
                    id='date-picker',
                    min_date_allowed=df['datetime'].min(),
                    max_date_allowed=df['datetime'].max(),
                    initial_visible_month=df['datetime'].min(),
                    date=df['datetime'].min().date(),
                    style={'margin-left': '10px'}
                ),
                html.Button('Update Graph', id='update-button', n_clicks=0, style={'margin-left': '10px',
                                                                                   'font-size': '130%'}),
                html.Div(id='graph-container')
            ]),
            dcc.Tab(label='Alarms per Minute in several Dates/all dates (I need to choose.)', children=[
                html.Label('Select Date for Tab 2:'),
                # dcc.DatePickerSingle(
                #     id='date-picker-tab2',
                #     min_date_allowed=df['datetime'].min(),
                #     max_date_allowed=df['datetime'].max(),
                #     initial_visible_month=df['datetime'].min(),
                #     date=df['datetime'].min().date()
                # ),
                # html.Button('Update Graph', id='update-button-tab2', n_clicks=0),
                # html.Div(id='graph-container-tab2')
            ]),
        ])
    ])



    # Define the callback to update the graph based on user input
    @app.callback(
        dash.dependencies.Output('graph-container', 'children'),
        [dash.dependencies.Input('update-button', 'n_clicks')],
        [dash.dependencies.State('date-picker', 'date')]
    )
    def update_graph_callback(n_clicks, selected_date):
        if n_clicks > 0:
            fig = create_graph(pd.to_datetime(selected_date), df)
            return dcc.Graph(figure=fig)

    return app


def startApp():
    app = create_app()
    app.run_server(debug=True)
