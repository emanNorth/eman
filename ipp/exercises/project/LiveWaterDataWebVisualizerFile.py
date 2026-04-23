
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
        'flow': "#2D8C53",
        'temp': "#dcc38e"
    }

    # Per-station flood risk thresholds (cfs)
    # Based on typical flood stage flow rates for each river
    FLOOD_THRESHOLDS = {
        'USGS-01646500': 25000,   # Potomac River - flood stage ~25,000 cfs
        'USGS-06730500': 800,     # Boulder Creek - flood stage ~800 cfs (smaller river)
        'USGS-02037500': 15000,   # James River - flood stage ~15,000 cfs
    }
    
    # Default threshold for unknown stations
    DEFAULT_FLOOD_THRESHOLD = 10000

    def __init__(self, host: str = '127.0.0.1', port: int = 8050):
        '''
        Initializes the visualizer.

        Creates Dash app and layout, sets storage for live and historical
        water data, and configures refresh rate for dashboard updates.

        Args:
            host (str): IP address of Dash server.
            port (int): Port number for Dash server.
        '''
        super().__init__()
        self.sort_mode = "site"
        self.host = host
        self.port = port
        self.dataLock = Lock()

        self.liveWaterDataTable: Dict[str, WaterData] = {}
        self.flowHistory: Dict[str, List[float]] = {}
        self.maxPoints = 20

        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.app.title = 'Live Water Data Dashboard'

        self._setupLayout()
        self._setupCallbacks()

    def _setupLayout(self):
        '''
        Builds the Dash application layout.

        Creates the main dashboard structure including:
        - Title header with flood alert indicator
        - Summary statistics cards
        - Sort buttons for data organization
        - Chart containers for visualizations
        - Auto-refresh interval component
        '''
        self.app.layout = html.Div(
            style={'backgroundColor': self.COLORS['background'],
                   'padding': '20px', 'minHeight': '100vh'},
            children=[
                # Title + Flood Alert Indicator together
                html.Div(
                    style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'marginBottom': '25px'
                    },
                    children=[
                        html.H1(
                            'Live Water Data Dashboard (USGS)',
                            style={'color': self.COLORS['text'], 'margin': '0'}
                        ),
                        html.Div(
                            id='risk-indicator',
                            children='FLOOD ALERT',
                            style={
                                'backgroundColor': 'gray',
                                'color': 'white',
                                'padding': '6px 12px',
                                'borderRadius': '4px',
                                'fontSize': '12px',
                                'fontWeight': 'bold',
                                'marginLeft': '15px',
                                'opacity': '0.4'
                            }
                        )
                    ]
                ),

                html.Div(id='stats-summary', style={'marginBottom': '20px'}),

                html.Div([
                    html.Button("Sort by Flow Rate", id="btn-flow"),
                    html.Button("Sort by Water Level", id="btn-level"),
                    html.Button("Sort by Temperature", id="btn-temp"),
                    html.Button("Sort by Site Name", id="btn-name"),
                ], style={'textAlign': 'center', 'marginBottom': '20px'}),

                html.Div(
                    id='charts-container',
                    style={'display': 'grid',
                           'gridTemplateColumns': 'repeat(2, 1fr)',
                           'gap': '20px'}
                ),

                dcc.Interval(id='interval', interval=2000, n_intervals=0)
            ]
        )

    def _setupCallbacks(self):
        '''
        Registers Dash callbacks for interactive dashboard updates.

        Handles:
        - Periodic data refresh via interval component
        - Sort button clicks to reorder data
        - Flood alert indicator state changes
        - Chart and summary regeneration
        '''
        @self.app.callback(
            Output('stats-summary', 'children'),
            Output('charts-container', 'children'),
            Output('risk-indicator', 'style'),
            Input('interval', 'n_intervals'),
            Input('btn-flow', 'n_clicks'),
            Input('btn-level', 'n_clicks'),
            Input('btn-temp', 'n_clicks'),
            Input('btn-name', 'n_clicks')
        )
        def updateDashboard(_, f, l, t, n):
            '''
            Updates all dashboard components on each interval tick or button click.

            Args:
                _: Interval tick count (unused).
                f: Flow button click count.
                l: Level button click count.
                t: Temperature button click count.
                n: Name button click count.

            Returns:
                tuple: (summary component, charts list, indicator style dict)
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

            # Default dim style for indicator (no flood risk)
            dim_style = {
                'backgroundColor': 'gray',
                'color': 'white',
                'padding': '6px 12px',
                'borderRadius': '4px',
                'fontSize': '12px',
                'fontWeight': 'bold',
                'marginLeft': '15px',
                'opacity': '0.4'
            }

            with self.dataLock:
                if not self.liveWaterDataTable:
                    empty = html.Div(
                        'Waiting for live water data...',
                        style={'textAlign': 'center',
                               'color': self.COLORS['text'],
                               'padding': '40px'}
                    )
                    return empty, [], dim_style

                waterList = list(self.liveWaterDataTable.values())

                if self.sort_mode == "flow":
                    waterList.sort(key=lambda w: w.flowRate_cfs, reverse=True)
                elif self.sort_mode == "level":
                    waterList.sort(key=lambda w: w.waterLevel_ft, reverse=True)
                elif self.sort_mode == "temp":
                    waterList.sort(key=lambda w: w.waterTemperature_c, reverse=True)
                else:
                    waterList.sort(key=lambda w: w.location.siteName)

                # Check if ANY station exceeds its flood threshold
                any_flood_risk = self._checkFloodRisk(waterList)

                # Set indicator style based on flood risk
                if any_flood_risk:
                    indicator_style = {
                        'backgroundColor': '#e74c3c',
                        'color': 'white',
                        'padding': '6px 12px',
                        'borderRadius': '4px',
                        'fontSize': '12px',
                        'fontWeight': 'bold',
                        'marginLeft': '15px',
                        'opacity': '1'
                    }
                else:
                    indicator_style = dim_style

                summary = self._createSummary(waterList)
                charts = self._createCharts(waterList)
                return summary, charts, indicator_style

    def _checkFloodRisk(self, waterList: List[WaterData]) -> bool:
        '''
        Checks if any station has flow rate exceeding its flood threshold.

        Each station has a specific threshold based on historical flood
        stage data. Unknown stations use a default threshold.

        Args:
            waterList (List[WaterData]): List of water data readings.

        Returns:
            bool: True if any station exceeds its flood threshold.
        '''
        for w in waterList:
            siteID = w.location.siteID
            threshold = self.FLOOD_THRESHOLDS.get(siteID, self.DEFAULT_FLOOD_THRESHOLD)
            if w.flowRate_cfs > threshold:
                return True
        return False

    def _getStationThreshold(self, siteID: str) -> float:
        '''
        Returns the flood threshold for a specific station.

        Args:
            siteID (str): The USGS station identifier.

        Returns:
            float: Flood threshold in cubic feet per second (cfs).
        '''
        return self.FLOOD_THRESHOLDS.get(siteID, self.DEFAULT_FLOOD_THRESHOLD)

    def _createSummary(self, waterList: List[WaterData]):
        '''
        Creates the summary statistics cards section.

        Displays aggregate metrics including:
        - Number of active stations
        - Average flow rate across all stations
        - Average water level across all stations
        - Average temperature across all stations

        Args:
            waterList (List[WaterData]): List of water data readings.

        Returns:
            html.Div: Dash component containing summary cards.
        '''
        avgLevel = sum(w.waterLevel_ft for w in waterList) / len(waterList)
        avgFlow = sum(w.flowRate_cfs for w in waterList) / len(waterList)
        avgTemp = sum(w.waterTemperature_c for w in waterList) / len(waterList)

        def card(label, value, color):
            '''
            Creates a single summary card component.

            Args:
                label (str): Card title text.
                value (str): Card value to display.
                color (str): Accent color for the card.

            Returns:
                html.Div: Styled card component.
            '''
            return html.Div(
                style={'backgroundColor': self.COLORS['card'],
                       'padding': '20px',
                       'borderRadius': '8px',
                       'borderLeft': f'4px solid {color}',
                       'textAlign': 'center'},
                children=[
                    html.H4(label, style={'color': self.COLORS['text'], 'marginBottom': '8px'}),
                    html.H2(value, style={'color': color})
                ]
            )

        return html.Div([
            html.Div(
                style={'display': 'grid',
                       'gridTemplateColumns': 'repeat(4, 1fr)',
                       'gap': '15px',
                       'marginBottom': '15px'},
                children=[
                    card('Stations', str(len(waterList)), self.COLORS['text']),
                    card('Avg Flow (cfs)', f'{avgFlow:.1f}', self.COLORS['flow']),
                    card('Avg Level (ft)', f'{avgLevel:.2f}', self.COLORS['level']),
                    card('Avg Temp (°C)', f'{avgTemp:.1f}', self.COLORS['temp']),
                ]
            ),
        ])

    def _createCharts(self, waterList: List[WaterData]):
        '''
        Creates all chart components for the dashboard.

        Generates:
        - Flow rate bar chart (with flood risk coloring)
        - Water level bar chart
        - Temperature bar chart
        - Flow rate time series line chart

        Args:
            waterList (List[WaterData]): List of water data readings.

        Returns:
            list: List of Dash Graph components.
        '''
        siteNames = [w.location.siteName for w in waterList]

        def makeBar(title, values, color):
            '''
            Creates a standard bar chart component.

            Args:
                title (str): Chart title.
                values (list): Y-axis values for each bar.
                color (str): Bar color.

            Returns:
                dcc.Graph: Plotly bar chart component.
            '''
            fig = go.Figure(go.Bar(
                x=siteNames,
                y=values,
                marker_color=color
            ))
            fig.update_layout(
                title=title,
                paper_bgcolor=self.COLORS['card'],
                plot_bgcolor=self.COLORS['card'],
                font=dict(color=self.COLORS['text'])
            )
            return dcc.Graph(figure=fig, config={'displayModeBar': False})

        levelChart = makeBar("Water Level (ft)", [w.waterLevel_ft for w in waterList], self.COLORS['level'])
        tempChart = makeBar("Temperature (°C)", [w.waterTemperature_c for w in waterList], self.COLORS['temp'])

        # Flow chart with conditional coloring based on flood risk
        flowValues = [w.flowRate_cfs for w in waterList]
        flowColors = []
        for w in waterList:
            threshold = self._getStationThreshold(w.location.siteID)
            if w.flowRate_cfs > threshold:
                flowColors.append('#e74c3c')  # Red for flood risk
            else:
                flowColors.append(self.COLORS['flow'])  # Normal green

        flowChart = go.Figure(go.Bar(
            x=siteNames,
            y=flowValues,
            marker_color=flowColors
        ))

        flowChart.update_layout(
            title="Flow Rate (cfs)",
            paper_bgcolor=self.COLORS['card'],
            plot_bgcolor=self.COLORS['card'],
            font=dict(color=self.COLORS['text'])
        )

        flowChart = dcc.Graph(figure=flowChart, config={'displayModeBar': False})

        timeSeriesChart = self._createFlowRateTimeSeries()
        return [flowChart, levelChart, tempChart, timeSeriesChart]

    def _processWaterData(self, waData: WaterData = None):
        '''
        Processes incoming water data from the listener pipeline.

        Stores the latest reading for each station and maintains
        a rolling history of flow rate values for time series display.

        Args:
            waData (WaterData): Incoming water data object.
        '''
        if not waData:
            return

        with self.dataLock:
            siteID = waData.location.siteID

            self.liveWaterDataTable[siteID] = waData

            if siteID not in self.flowHistory:
                self.flowHistory[siteID] = []

            self.flowHistory[siteID].append(waData.flowRate_cfs)

            if len(self.flowHistory[siteID]) > self.maxPoints:
                self.flowHistory[siteID] = self.flowHistory[siteID][-self.maxPoints:]

    def _createFlowRateTimeSeries(self):
        '''
        Creates the flow rate time series line chart.

        Displays historical flow rate readings for each station
        over the last N time steps, allowing trend visualization.

        Returns:
            dcc.Graph: Plotly line chart component.
        '''
        fig = go.Figure()

        colors = ['#2D8C53', '#3498db', '#e74c3c', '#f1c40f']

        for i, (siteID, readings) in enumerate(self.flowHistory.items()):
            if len(readings) < 2:
                continue

            if siteID not in self.liveWaterDataTable:
                continue

            siteName = self.liveWaterDataTable[siteID].location.siteName

            x_vals = list(range(len(readings)))

            fig.add_trace(go.Scatter(
                x=x_vals,
                y=readings,
                mode='lines+markers',
                name=siteName,
                line=dict(color=colors[i % len(colors)], width=2)
            ))

        fig.update_layout(
            title="Flow Rate Over Time (Time-Bound)",
            paper_bgcolor=self.COLORS['card'],
            plot_bgcolor=self.COLORS['card'],
            font=dict(color=self.COLORS['text']),
            xaxis_title="Time Steps",
            yaxis_title="Flow Rate (cfs)"
        )

        return dcc.Graph(figure=fig, config={'displayModeBar': False})

    def startVisualizer(self):
        '''
        Starts the Dash web server.

        Launches the dashboard on the configured host and port.
        This method blocks until the server is stopped.
        '''
        print(f"Dashboard running at http://{self.host}:{self.port}/")
        self.app.run(host=self.host, port=self.port, debug=False)


if __name__ == '__main__':
    visualizer = LiveWaterDataWebVisualizer()

    def simulateData():
        '''
        Simulates water data for testing the dashboard.

        Generates random readings for three stations with values
        that occasionally exceed flood thresholds to test alerts.
        '''
        stations = [
            ('USGS-01646500', 'Potomac River – Washington, DC'),
            ('USGS-06730500', 'Boulder Creek – Longmont, CO'),
            ('USGS-02037500', 'James River – Richmond, VA')
        ]

        while True:
            for siteID, name in stations:
                w = WaterData()
                w.location = WaterLocationData()
                w.location.siteID = siteID
                w.location.siteName = name
                
                # Simulate values that occasionally trigger flood alerts
                if siteID == 'USGS-01646500':
                    w.flowRate_cfs = random.uniform(5000, 30000)  # Potomac: threshold 25000
                elif siteID == 'USGS-06730500':
                    w.flowRate_cfs = random.uniform(100, 1000)    # Boulder: threshold 800
                else:
                    w.flowRate_cfs = random.uniform(3000, 18000)  # James: threshold 15000
                    
                w.waterLevel_ft = random.uniform(1, 15)
                w.waterTemperature_c = random.uniform(5, 25)
                visualizer.handleIncomingWaterData(w)
            time.sleep(2)

    Thread(target=simulateData, daemon=True).start()
    visualizer.startVisualizer()
