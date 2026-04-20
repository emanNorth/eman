import time
import random
from threading import Thread, Lock
from typing import Dict, List

import dash
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

from ipp.exercises.project.WaterDataFile import WaterData
from ipp.exercises.project.WaterLocationDataFile import WaterLocationData
from ipp.exercises.project.WaterDataListenerFile import WaterDataListener


class LiveWaterDataWebVisualizer(WaterDataListener):
    '''
    A live visualizer for water monitoring data using Dash + Plotly.

    Displays aggregated and per station readings for:
    - Flow rate (cfs)
    - Water level (ft)
    - Water temperature (°C)

    Includes both bar charts (value bound) and a time series line chart (time bound)
    that updates automatically as new data arrives.
    '''
    COLORS = {
        'background': '#1a1a2e',
        'card': '#16213e',
        'text': '#ffffff',
        'level': '#3498db',
        'flow': '#2ecc71',
        'temp': '#e74c3c'
    }

    def __init__(self, host: str = '127.0.0.1', port: int = 8050):
        '''
        Initializes the visualizer.

        - Creates Dash app and layout
        - Sets storage for live and historical water data
        - Configures refresh rate for dashboard updates

        Args:
            host (str): IP address of Dash server
            port (int): Port number for Dash server
        '''
        super().__init__()
        self.sort_mode = "site"
        self.host = host
        self.port = port
        self.dataLock = Lock()
        

        # latest readings per station
        self.liveWaterDataTable: Dict[str, WaterData] = {}
        # time-bound flow history per station
        self.flowHistory: Dict[str, List[float]] = {}
        self.maxPoints = 20  # number of data points kept per station

        # Dash app setup
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.app.title = 'Live Water Data Dashboard'

        self._setupLayout()
        self._setupCallbacks()

    def _setupLayout(self):
        '''
        Defines the layout of the web dashboard.
        '''
        self.app.layout = html.Div(
            style={'backgroundColor': self.COLORS['background'],
                   'padding': '20px', 'minHeight': '100vh'},
            children=[
                html.H1(
                    'Live Water Data Dashboard (USGS)',
                    style={'color': self.COLORS['text'],
                           'textAlign': 'center',
                           'marginBottom': '25px'}
                ),

                html.Div(id='stats-summary', style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Button("Sort by Flow Rate", id="btn-flow"),
                    html.Button("Sort by Water Level", id="btn-level"),
                    html.Button("Sort by Temperature", id="btn-temp"),
                    html.Button("Sort by Site Name", id="btn-name"),], 
                         style={'textAlign': 'center', 'marginBottom': '20px'}),
                
                html.Div(
                    id='charts-container',
                    style={'display': 'grid',
                           'gridTemplateColumns': 'repeat(2, 1fr)',
                           'gap': '20px'}
                ),

                # 2-second update interval
                dcc.Interval(id='interval', interval=2000, n_intervals=0)
            ]
        )

    def _setupCallbacks(self):
        '''
        Connects dynamic update events to the dashboard.
        '''
        @self.app.callback(
            Output('stats-summary', 'children'),
            Output('charts-container', 'children'),
            Input('interval', 'n_intervals'),
            Input('btn-flow', 'n_clicks'),
            Input('btn-level', 'n_clicks'),
            Input('btn-temp', 'n_clicks'),
            Input('btn-name', 'n_clicks')
        )
        
        def updateDashboard(_, f, l, t, n):
            '''
            Refreshes the summary and chart data.
            '''
            ctx = dash.callback_context
            if ctx.triggered:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

                if button_id == "btn-flow":
                    self.sort_mode = "flow"
                elif button_id == "btn-level":
                    self.sort_mode = "level"
                elif button_id == "btn-temp":
                    self.sort_mode = "temp"
                elif button_id == "btn-name":
                    self.sort_mode = "site"
                    
            with self.dataLock:
                if not self.liveWaterDataTable:
                    empty = html.Div(
                        'Waiting for live water data...',
                        style={'textAlign': 'center',
                               'color': self.COLORS['text'],
                               'padding': '40px'})
                    return empty, []

                waterList = list(self.liveWaterDataTable.values())
                if self.sort_mode == "flow":
                    waterList.sort(key=lambda w: w.flowRate_cfs, reverse=True)
                elif self.sort_mode == "level":
                    waterList.sort(key=lambda w: w.waterLevel_ft, reverse=True)
                elif self.sort_mode == "temp":
                    waterList.sort(key=lambda w: w.waterTemperature_c, reverse=True)
                else:
                    waterList.sort(key=lambda w: w.location.siteName)
                
                summary = self._createSummary(waterList)
                charts = self._createCharts(waterList)
                return summary, charts
       

    def _createSummary(self, waterList: List[WaterData]):
        '''
        Builds average summary statistics.

        Args:
            waterList (List[WaterData]): current water data per site
        '''
        avgLevel = sum(w.waterLevel_ft for w in waterList) / len(waterList)
        avgFlow = sum(w.flowRate_cfs for w in waterList) / len(waterList)
        avgTemp = sum(w.waterTemperature_c for w in waterList) / len(waterList)

        def card(label, value, color):
            return html.Div(
                style={'backgroundColor': self.COLORS['card'],
                       'padding': '20px',
                       'borderRadius': '8px',
                       'borderLeft': f'4px solid {color}',
                       'textAlign': 'center'},
                children=[
                    html.H4(label, style={'color': self.COLORS['text'],
                                          'marginBottom': '8px'}),
                    html.H2(value, style={'color': color})
                ]
            )

        return html.Div(
            style={'display': 'grid',
                   'gridTemplateColumns': 'repeat(4, 1fr)',
                   'gap': '15px'},
            children=[
                card('Stations', str(len(waterList)), self.COLORS['text']),
                card('Avg Flow (cfs)', f'{avgFlow:.1f}', self.COLORS['flow']),
                card('Avg Level (ft)', f'{avgLevel:.2f}', self.COLORS['level']),
                card('Avg Temp (°C)', f'{avgTemp:.1f}', self.COLORS['temp'])
            ]
        )

    def _createCharts(self, waterList: List[WaterData]):
        '''
        Builds full set of visual charts.

        Returns:
            list: chart components for dashboard.
        '''
        siteNames = [w.location.siteName for w in waterList]

        def makeBar(title, values, color):
            fig = go.Figure(
                go.Bar(
                    x=siteNames,
                    y=values,
                    marker_color=color,
                    hovertemplate='<b>%{x}</b><br>%{y:.2f}<extra></extra>'
                )
            )
            fig.update_layout(
                title=title,
                xaxis_title="Monitoring Station",
                yaxis_title="Value",
                paper_bgcolor=self.COLORS['card'],
                plot_bgcolor=self.COLORS['card'],
                font=dict(color=self.COLORS['text']),
                margin=dict(t=50, b=80)
            )
            return dcc.Graph(figure=fig, config={'displayModeBar': False})

        # Create value-bound charts
        flowChart = makeBar('Flow Rate (cfs)', [w.flowRate_cfs for w in waterList], self.COLORS['flow'])
        levelChart = makeBar('Water Level (ft)', [w.waterLevel_ft for w in waterList], self.COLORS['level'])
        tempChart = makeBar('Water Temperature (°C)', [w.waterTemperature_c for w in waterList], self.COLORS['temp'])

        # Create time-bound flow rate chart
        timeSeries = self._createFlowRateTimeSeries()

        return [flowChart, levelChart, tempChart, timeSeries]

    def _createFlowRateTimeSeries(self):
        '''
        Builds a time series line chart showing recent flow rate per station.
        '''
        fig = go.Figure()
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f']

        for i, (siteID, readings) in enumerate(self.flowHistory.items()):
            if len(readings) < 2:
                continue
            x_vals = list(range(1, len(readings) + 1))
            siteName = self.liveWaterDataTable[siteID].location.siteName
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=readings,
                mode='lines+markers',
                line=dict(color=colors[i % len(colors)], width=2),
                name=siteName,
                hovertemplate=f'<b>{siteName}</b><br>Reading %{{x}}<br>Flow %{{y:.2f}} cfs<extra></extra>'
            ))

        fig.update_layout(
            title='Flow Rate Over Time (Time‑Bound)',
            xaxis_title='Recent Readings',
            yaxis_title='Flow Rate (cfs)',
            paper_bgcolor=self.COLORS['card'],
            plot_bgcolor=self.COLORS['card'],
            font=dict(color=self.COLORS['text']),
            margin=dict(t=60, b=60)
        )
        return dcc.Graph(figure=fig, config={'displayModeBar': False})


    def _processWaterData(self, waData: WaterData = None):
        '''
        Receives new WaterData from manager or simulation
        and updates both current readings and time history.
        '''
        if not waData:
            return
        with self.dataLock:
            self.liveWaterDataTable[waData.location.siteID] = waData
    

            if waData.location.siteID not in self.flowHistory:
                self.flowHistory[waData.location.siteID] = []
            self.flowHistory[waData.location.siteID].append(waData.flowRate_cfs)
            # Keep only most recent N points
            if len(self.flowHistory[waData.location.siteID]) > self.maxPoints:
                self.flowHistory[waData.location.siteID] = self.flowHistory[waData.location.siteID][-self.maxPoints:]

    def startVisualizer(self):
        '''
        Starts the Dash web dashboard.
        '''
        print(f'\nDashboard running at http://{self.host}:{self.port}/')
        print('Press CTRL+C to stop\n')
        self.app.run(host=self.host, port=self.port,
                     debug=False, use_reloader=False)



if __name__ == '__main__':
    '''
    Simple test run to demonstrate live updates.

    Generates fake water records for three stations and visualizes
    both their instantaneous and historical values.
    '''
    visualizer = LiveWaterDataWebVisualizer()

    def simulateData():
        stations = [
            ('USGS-01646500', 'Potomac River – Washington, DC'),
            ('USGS-11455420', 'Sacramento River – CA'),
            ('USGS-09380000', 'Colorado River – AZ')
        ]

        while True:
            for siteID, name in stations:
                w = WaterData()
                w.location = WaterLocationData()
                w.location.siteID = siteID
                w.location.siteName = name
                w.flowRate_cfs = random.uniform(200, 5000)
                w.waterLevel_ft = random.uniform(1, 15)
                w.waterTemperature_c = random.uniform(5, 25)
                visualizer.handleIncomingWaterData(w)
            time.sleep(2)

    Thread(target=simulateData, daemon=True).start()
    visualizer.startVisualizer()
