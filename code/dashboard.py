import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000,key="refresh")

st.set_page_config(
    page_title="AirFogSim Dashboard",
    layout="wide"
)

st.title("🚗 AirFogSim Vehicle Fog Computing Dashboard")

# -----------------------------
# Dummy Data (Replace later)
# -----------------------------
if os.path.exists("snapshot.json"):

    with open("snapshot.json","r") as f:
        snapshot=json.load(f)

else:

    st.warning("Waiting for simulation...")

    st.stop()

vehicles=snapshot["vehicles"]

uavs=snapshot["uavs"]

rsus=[(r["x"],r["y"]) for r in snapshot["rsus"]]

# -----------------------------
# Top Information
# -----------------------------

c1,c2,c3 = st.columns(3)

with c1:
    st.subheader("Simulation")
    st.metric("Time", f"{snapshot['time']} s")
    st.metric("Step", snapshot["step"])
    st.metric("Episode", snapshot["episode"])

with c2:
    st.subheader("Environment")
    st.metric("Deployment", snapshot["deployment"])
    st.metric("Vehicles", snapshot["vehicle_count"])
    st.metric("UAVs", snapshot["uav_count"])

with c3:
    st.subheader("Performance")
    st.metric("Delay", f"{snapshot['simulation_delay']:.2f} s")

st.divider()

# -----------------------------
# Map
# -----------------------------

left,right = st.columns([2,1])

with left:

    st.subheader("Live Map")

    fig,ax = plt.subplots(figsize=(8,8))

    # Vehicles
    vx=[v["x"] for v in vehicles]
    vy=[v["y"] for v in vehicles]
    ax.scatter(vx,vy,c="blue",label="Vehicles",s=30)

    # UAVs
    ux=[u["x"] for u in uavs]
    uy=[u["y"] for u in uavs]
    ax.scatter(ux,uy,c="green",marker="^",label="UAV",s=80)

    # RSUs
    rx=[r[0] for r in rsus]
    ry=[r[1] for r in rsus]
    ax.scatter(rx,ry,c="red",marker="s",label="RSU",s=80)

    ax.set_xlim(0,2000)
    ax.set_ylim(0,2000)

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")

    ax.legend()

    st.pyplot(fig)

with right:

    st.subheader("Sample Vehicle")

    st.write(vehicles[0])

st.divider()

# -----------------------------
# Vehicle Table
# -----------------------------

st.subheader("Vehicle List")

df=pd.DataFrame(vehicles)

st.dataframe(df,use_container_width=True)

st.divider()

# -----------------------------
# Simulation Log
# -----------------------------

st.subheader("Simulation Log")

st.code("""
[22.0] Vehicles Updated
[22.0] UAV Updated
[22.0] Tasks Generated
[22.0] PPO Decision Completed
""")