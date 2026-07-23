import json
import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import pandas as pd

SNAPSHOT_FILE = "snapshot.json"
RSU_RADIUS = 300

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY]
)

app.title = "AirFogSim Dashboard"

server = app.server

def load_snapshot():

    if not os.path.exists(SNAPSHOT_FILE):
        return None

    try:

        with open(SNAPSHOT_FILE, "r") as f:
            return json.load(f)

    except Exception:

        return None

def empty_figure():

    fig = go.Figure()

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#111111",
        plot_bgcolor="#111111",

        xaxis=dict(visible=False),
        yaxis=dict(visible=False),

        annotations=[

            dict(

                text="Waiting for Simulation...",

                x=0.5,
                y=0.5,

                showarrow=False,

                font=dict(size=28)

            )

        ]

    )

    return fig

app.layout = dbc.Container(

    [

        html.H2(
            "🚗 AirFogSim Digital Twin Dashboard",
            className="text-center mt-3 mb-4"
        ),

        dcc.Interval(

            id="interval",

            interval=1000,

            n_intervals=0

        ),

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H5("Simulation Time"),

                                html.H3(id="time-card")

                            ]

                        )

                    ),

                    width=3

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H5("Vehicles"),

                                html.H3(id="vehicle-card")

                            ]

                        )

                    ),

                    width=3

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H5("UAVs"),

                                html.H3(id="uav-card")

                            ]

                        )

                    ),

                    width=3

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H5("Delay"),

                                html.H3(id="delay-card")

                            ]

                        )

                    ),

                    width=3

                )

            ],

            className="mb-3"

        ),

        dbc.Row(

            [

                dbc.Col(

                    dcc.Graph(

                        id="map",

                        figure=empty_figure(),

                        style={"height": "700px"},

                        config={

                            "displaylogo": False,

                            "scrollZoom": True

                        }

                    ),

                    width=9

                ),

                dbc.Col(

                    html.Div(

                        id="sidebar"

                    ),

                    width=3

                )

            ]

        ),

        html.Hr(),

        html.H4("Vehicle Information"),

        html.Div(id="vehicle-table")

    ],

    fluid=True

)

def build_map(snapshot):

    vehicles = snapshot.get("vehicles", [])
    uavs = snapshot.get("uavs", [])
    rsus = snapshot.get("rsus", [])

    rsu_lookup = {
        r["id"]: r
        for r in rsus
    }

    fig = go.Figure()

    # -------------------------------------------------------
    # RSU Coverage
    # -------------------------------------------------------

    for rsu in rsus:

        fig.add_shape(

            type="circle",

            xref="x",
            yref="y",

            x0=rsu["x"] - RSU_RADIUS,
            y0=rsu["y"] - RSU_RADIUS,

            x1=rsu["x"] + RSU_RADIUS,
            y1=rsu["y"] + RSU_RADIUS,

            line=dict(
                color="rgba(239,68,68,0.35)",
                width=2
            ),

            fillcolor="rgba(239,68,68,0.05)"
        )

    # -------------------------------------------------------
    # Vehicle → RSU Links
    # -------------------------------------------------------

    for vehicle in vehicles:

        rsu = rsu_lookup.get(vehicle.get("nearest_rsu"))

        if rsu is None:
            continue

        fig.add_trace(

            go.Scatter(

                x=[vehicle["x"], rsu["x"]],
                y=[vehicle["y"], rsu["y"]],

                mode="lines",

                line=dict(
                    color="rgba(255,255,255,0.25)",
                    width=1
                ),

                hoverinfo="skip",

                showlegend=False

            )

        )

    # -------------------------------------------------------
    # Vehicles
    # -------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=[v["x"] for v in vehicles],
            y=[v["y"] for v in vehicles],
            mode="markers",
            name="Vehicles",
            marker=dict(
                size=8,
                color="#3B82F6"
            )
        )
    )


    fig.add_trace(
        go.Scatter(
            x=[u["x"] for u in uavs],
            y=[u["y"] for u in uavs],
            mode="markers",
            name="UAVs",
            marker=dict(
                size=14,
                color="#10B981",
                symbol="triangle-up"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[r["x"] for r in rsus],
            y=[r["y"] for r in rsus],
            mode="markers",
            name="RSUs",
            marker=dict(
                size=18,
                color="#EF4444",
                symbol="square"
            )
        )
    )

   
    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#111111",
        plot_bgcolor="#111111",

        height=700,

        uirevision="constant",

        xaxis=dict(
            title="X Position (m)",
            showgrid=True,
            gridcolor="#333333",
            autorange=True
        ),

        yaxis=dict(
            title="Y Position (m)",
            showgrid=True,
            gridcolor="#333333",
            autorange=True,
            scaleanchor="x"
        ),

        legend=dict(
            orientation="h",
            y=1.02
        ),

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )

    )

    return fig

@app.callback(
    Output("time-card", "children"),
    Output("vehicle-card", "children"),
    Output("uav-card", "children"),
    Output("delay-card", "children"),
    Output("map", "figure"),
    Input("interval", "n_intervals")
)
def update_cards(_):

    snapshot = load_snapshot()

    if snapshot is None:

        return (
            "--",
            "--",
            "--",
            "--"
        )

    vehicles = snapshot.get("vehicles", [])
    uavs = snapshot.get("uavs", [])

    return (
        f"{snapshot['time']:.1f} s",
        str(len(vehicles)),
        str(len(uavs)),
        f"{snapshot['simulation_delay']:.2f} s",
        build_map(snapshot)
    )


if __name__ == "__main__":
    app.run(debug=True)