# Programming in Python - An Introduction: Lab Module 10 - Proposal

### Description

USGS Real-Time Water Monitoring System

This project is a real time water monitoring and visualization system built in Python. It connects to the U.S. Geological Survey (USGS) National Water Information System (NWIS) API to retrieve live river and stream data from USGS sensors, processes and structures the incoming sensor readings, and presents them through both a desktop GUI and a live web dashboard.

The system focuses on transforming raw environmental sensor data into structured, interactive, and understandable insights through data parsing, scheduling, sorting, and visualization.


## What - The Problem 

Problem Statement
Rivers are dynamic systems. Water levels and flow rates shift constantly in response to rainfall, snowmelt, dam releases, and seasonal patterns. The U.S. Geological Survey operates thousands of monitoring stations that publish sensor readings in real time, but raw JSON data from an API is difficult to interpret without tooling.

Key challenges include:
Rivers are unpredictable
- Dynamic updates: Conditions change frequently and require live monitoring
- Detection lag: Rising water levels may go unnoticed until conditions become dangerous
Raw data is unreadable
- Data complexity: USGS returns structured GeoJSON that must be parsed into usable values
- Lack of real time structure: Raw readings must be continuously polled and organized
- Multi station comparison: Understanding regional trends requires aggregating multiple locations
Consequences are serious
- Flooding causes
- Early detection saves lives and property

This project addresses these issues by building a complete pipeline from data retrieval to visualization.

## Why - Who Cares? 

There are few things i find compelling about solving this problem: 

- Real world consequence:
Extreme weather and water related events have become increasingly significant in the United States. According to NOAA’s National Centers for Environmental Information (NCEI), the year 2024 included 27 billion dollar weather and climate disasters, resulting in approximately $182.7 billion in damages and widespread impacts across the country.
These events included hurricanes, flooding, droughts, wildfires, and severe storms.
Over time, NOAA data shows a clear upward trend in both the frequency and cost of extreme weather events, highlighting the importance of systems that improve environmental visibility, data accessibility and provide early warning even minutes of lead time can trigger evacuations, protect infrastructure, and save lives.

This project is deals with a very real issue and motivated by the need for tools that help:
Monitor environmental changes in real time
Organize raw sensor data into usable formats
Support better understanding of water system behavior across multiple regions

- The data is Rich, continuous. USGS stations report every 15 minutes, 24/7, across thousands of locations. This makes working with time series data, polling architectures, and streaming visualization much more accessible and insightful.

- Technical breadth:
The project required integrating multiple disciplines: HTTP client design, JSON parsing, state management, concurrent scheduling, and interactive visualization. 

- Tangible output
Dashboard shows real rivers updating in real time

• Sources:
Smith, Adam B. “2024: An Active Year of U.S. Billion-Dollar Weather and Climate Disasters.” Climate.gov, National Oceanic and Atmospheric Administration (NOAA), 10 Jan. 2025, https://www.climate.gov/news-features/blogs/beyond-data/2024-active-year-us-billion-dollar-weather-and-climate-disasters


## How - Expected Technical Approach

┌──────────────────────────────────────────────┐
│        External Data Source                  │
│        USGS NWIS API                         │
└──────────────────────┬───────────────────────┘
                       │
                 HTTPS (REST API)
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        CDA LAYER (Data Acquisition)          │
│  • WaterServiceManager                       │
│  • APScheduler (scheduled polling)           │
│  • WaterServiceConnector (HTTP client)       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        GDA LAYER (Data Processing)           │
│  • WaterDataParser / NWIS Parser             │
│  • Data validation & transformation          │
│  • Sorting (SimpleBubbleSort)                │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        DATA STORAGE                          │
│  • In memory WaterData list                  │
│  • Flow history buffer                       │
│  • JSON raw data cache                       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        APPLICATION / UI LAYER                │
│  • Dash + Plotly Dashboard                   │
│  • Tkinter GUI                               │
│  • LiveWaterDataWebVisualizer                │
└──────────────────────────────────────────────┘

The system is designed using a layered architecture that separates data acquisition, processing, storage, and visualization. The CDA (Cloud Data Acquisition) layer is responsible for retrieving real time water data from the USGS NWIS API using HTTPS REST requests. This is handled by the WaterServiceManager, which schedules periodic data collection using APScheduler and communicates with the external service through the WaterServiceConnector.

The GDA (General Data Analytics) layer processes the raw data into structured WaterData objects using the NWIS specific parser. This layer performs validation, transformation, and sorting of water measurements such as flow rate, water level, and temperature. The processed data is stored in memory and optionally cached in JSON format. Finally, the application layer visualizes the data using a Dash/Plotly dashboard and a Tkinter interface, allowing real-time monitoring and user interaction with the system.

## Results - Expected Outcomes 

If my project is successful, the system will provide a fully functional real time water monitoring dashboard that continuously displays uptodate environmental data from multiple USGS monitoring stations. Users will be able to observe live changes in flow rate, water level, and temperature as new measurements are retrieved at regular intervals. The system will present this information clearly through interactive visualizations, making it easy to compare conditions across different locations.

In addition, the dashboard will allow users to interact with the data by sorting stations based on different metrics such as flow rate, water level, temperature, or site name. This will enable quick identification of highest or lowest values without modifying the underlying data.

EOF.
