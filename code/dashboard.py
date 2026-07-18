import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ----------------------------------------------------
# Auto Refresh
# ----------------------------------------------------
st_autorefresh(interval=1000, key="refresh")

st.set_page_config(
    page_title="AirFogSim Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 AirFogSim Vehicle Fog Computing Dashboard")

# ----------------------------------------------------
# Read Live Snapshot
# ----------------------------------------------------

if not os.path.exists("snapshot.json"):
    st.warning("Waiting for simulation...")
    st.stop()

with open("snapshot.json", "r") as f:
    snapshot = json.load(f)

vehicles = snapshot.get("vehicles", [])
uavs = snapshot.get("uavs", [])
rsus = snapshot.get("rsus", [])

# ----------------------------------------------------
# Top Dashboard Cards
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("⏱ Simulation Time", f"{snapshot['time']:.1f} s")

with col2:
    st.metric("🚗 Vehicles", len(vehicles))

with col3:
    st.metric("🛸 UAVs", len(uavs))

with col4:
    st.metric("⚡ Delay", f"{snapshot['simulation_delay']:.2f} s")

st.divider()

# ----------------------------------------------------
# Layout
# ----------------------------------------------------

left, right = st.columns([3, 1])

# ====================================================
# LEFT SIDE
# ====================================================

with left:

    st.subheader("🌍 AirFogSim Digital Twin")

    fig = go.Figure()

    # ---------------------------------------
    # Vehicles
    # ---------------------------------------

    if len(vehicles) > 0:

        fig.add_trace(

            go.Scatter(

                x=[v["x"] for v in vehicles],
                y=[v["y"] for v in vehicles],

                mode="markers",

                name="Vehicles",

                marker=dict(
                    size=8,
                    color="#3B82F6",
                    symbol="circle"
                ),

                customdata=[
                    [v["id"], v["speed"], v["angle"]]
                    for v in vehicles
                ],

                hovertemplate=
                "<b>Vehicle %{customdata[0]}</b><br>"
                "Speed: %{customdata[1]:.2f} m/s<br>"
                "Angle: %{customdata[2]:.1f}°<br>"
                "X: %{x:.1f}<br>"
                "Y: %{y:.1f}<extra></extra>"

            )

        )

    # ---------------------------------------
    # UAVs
    # ---------------------------------------

    if len(uavs) > 0:

        fig.add_trace(

            go.Scatter(

                x=[u["x"] for u in uavs],
                y=[u["y"] for u in uavs],

                mode="markers",

                name="UAV",

                marker=dict(
                    size=14,
                    color="#10B981",
                    symbol="triangle-up"
                ),

                text=[
                    f"""
                    UAV {u['id']}
                    """
                    for u in uavs
                ],

                hoverinfo="text"

            )

        )

    # ---------------------------------------
    # RSUs
    # ---------------------------------------

    if len(rsus) > 0:

        fig.add_trace(

            go.Scatter(

                x=[r["x"] for r in rsus],
                y=[r["y"] for r in rsus],

                mode="markers",

                name="RSU",

                marker=dict(
                    size=18,
                    color="#EF4444",
                    symbol="square"
                ),

                text=[
                    f"RSU {r['id']}"
                    for r in rsus
                ],

                hoverinfo="text"

            )

        )

    # ---------------------------------------
    # Layout
    # ---------------------------------------

    fig.update_layout(

        template="plotly_dark",

        height=700,

        paper_bgcolor="#111111",

        plot_bgcolor="#111111",

        xaxis=dict(
            title="X Position (m)",
            showgrid=True,
            gridcolor="#333333"
        ),

        yaxis=dict(
            title="Y Position (m)",
            showgrid=True,
            gridcolor="#333333",
            scaleanchor="x"
        ),

        legend=dict(
            orientation="h",
            y=1.05
        ),

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )

    )

    if vehicles:

        xs = [v["x"] for v in vehicles]
        ys = [v["y"] for v in vehicles]

        padding = 100

        fig.update_xaxes(
            range=[min(xs)-padding, max(xs)+padding]
        )

        fig.update_yaxes(
            range=[min(ys)-padding, max(ys)+padding]
        )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "scrollZoom": True
        }
    )

# ====================================================
# RIGHT PANEL
# ====================================================

with right:

    st.subheader("📊 Simulation")

    st.metric("Iteration", snapshot["iteration"])
    st.metric("Episode", snapshot["episode"])
    st.metric("Step", snapshot["step"])
    st.metric("Deployment", snapshot["deployment"])

    st.divider()

    st.subheader("🚗 Sample Vehicle")

    if len(vehicles):

        v = max(
            vehicles,
            key=lambda x: x["speed"]
        )

        st.write(f"**Vehicle ID:** {v['id']}")
        st.write(f"**Speed:** {v['speed']:.2f} m/s")
        st.write(f"**X:** {v['x']:.2f}")
        st.write(f"**Y:** {v['y']:.2f}")
        st.write(f"**Angle:** {v['angle']:.2f}")

    st.divider()

    st.subheader("📈 Statistics")

    avg_speed = 0

    if len(vehicles):

        avg_speed = sum(v["speed"] for v in vehicles) / len(vehicles)

    st.metric("Average Speed", f"{avg_speed:.2f} m/s")

    st.metric(
        "Vehicle Density",
        f"{len(vehicles)} Active"
    )

    fps = 1 / max(snapshot["simulation_delay"], 1e-6)

    st.metric(
        "Dashboard FPS",
        f"{fps:.1f}"
    )

# ----------------------------------------------------
# Vehicle Table
# ----------------------------------------------------

st.divider()

st.subheader("🚘 Vehicle Information")

if len(vehicles):

    df = pd.DataFrame(vehicles)

    df = df.sort_values("speed", ascending=False)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.divider()

st.caption(
    "AirFogSim Digital Twin | SUMO | PPO | Plotly | Real-Time Visualization"
)