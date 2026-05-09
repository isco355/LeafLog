
import os
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import psycopg2
from flask import Flask

server = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "zigbee_db")
DB_USER = os.getenv("DB_USER", "zigbee_user")
DB_PASS = os.getenv("DB_PASSWORD", "zigbee_pass")


def fetch_data(hours: int = 24) -> pd.DataFrame:
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS,    url_base_pathname="/dashboard/"
    )
    df = pd.read_sql(f"""
        SELECT ts, device_name, soil_moisture, humidity,
            temperature, battery, linkquality, dry
        FROM sensor_readings
        WHERE ts >= NOW() - INTERVAL '{hours} hours'
        ORDER BY ts ASC
    """, conn)

    conn.close()
    return df

def createDash(server):
    app = dash.Dash(__name__,server=server)
    app.title = "🌱 Soil Sensor Monitor"

    app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px"}, children=[
        html.H1("🌱 Soil Sensor Dashboard", style={"textAlign": "center"}),
        html.Div([
            html.Label("Show last:"),
            dcc.Dropdown(
                id="hours-select",
                options=[{"label": f"{h}h", "value": h} for h in [1, 6, 24, 48]],
                value=24, clearable=False, style={"width": "120px", "display": "inline-block"}
            ),
        ], style={"textAlign": "center", "marginBottom": "10px"}),
        dcc.Interval(id="timer", interval=15_000, n_intervals=0),
        html.Div(id="last-update", style={"textAlign": "center", "color": "gray", "marginBottom": "20px"}),

        # Layout — 6 charts in a 2-column grid
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"}, children=[
            dcc.Graph(id="chart-soil"),
            dcc.Graph(id="chart-humidity"),
            dcc.Graph(id="chart-temp"),
            dcc.Graph(id="chart-battery"),
            dcc.Graph(id="chart-linkquality"),
            dcc.Graph(id="chart-dry"),
        ]),

    ])


    def line_figure(df, col, title, unit, color_map):
        fig = go.Figure()
        for device, grp in df.groupby("device_name"):
            grp = grp.dropna(subset=[col])
            fig.add_trace(go.Scatter(
                x=grp["ts"], y=grp[col],
                mode="lines+markers",
                name=device,
                line={"color": color_map.get(device)},
            ))
        fig.update_layout(
            title=f"{title}",
            xaxis_title="Time",
            yaxis_title=unit,
            template="plotly_white",
            legend_title="Device",
            margin={"t": 40},
        )
        return fig


    @app.callback(
        Output("chart-soil",         "figure"),
        Output("chart-humidity",     "figure"),
        Output("chart-temp",         "figure"),
        Output("chart-battery",      "figure"),
        Output("chart-linkquality",  "figure"),
        Output("chart-dry",          "figure"),
        Output("last-update",        "children"),
        Input("timer",               "n_intervals"),
        Input("hours-select",        "value"),
    )
    def refresh(_, hours):
        df = fetch_data(hours)
        if df.empty:
            empty = go.Figure()
            empty.update_layout(title="No data yet", template="plotly_white")
            return empty, empty, empty, empty, empty, empty, "No data received yet."

        devices   = df["device_name"].unique().tolist()
        palette   = ["#2ecc71", "#3498db", "#e74c3c", "#9b59b6", "#f39c12"]
        color_map = {d: palette[i % len(palette)] for i, d in enumerate(devices)}

        soil_fig  = line_figure(df, "soil_moisture", "Soil Moisture",  "%",   color_map)
        hum_fig   = line_figure(df, "humidity",      "Air Humidity",   "%",   color_map)
        temp_fig  = line_figure(df, "temperature",   "Temperature",    "°C",  color_map)
        bat_fig   = line_figure(df, "battery",       "Battery Level",  "%",   color_map)
        lq_fig    = line_figure(df, "linkquality",   "Link Quality",   "lqi", color_map)
        dry_fig   = line_figure(df, "dry",           "Dry Alert",      "",    color_map)

        last = pd.to_datetime(df["ts"]).max().strftime("%Y-%m-%d %H:%M:%S")
        return soil_fig, hum_fig, temp_fig, bat_fig, lq_fig, dry_fig, f"Last update: {last}"

    return app
