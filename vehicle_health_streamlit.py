"""Streamlit dashboard for Smart Vehicle Health Evaluation

Run with: streamlit run vehicle_health_streamlit.py

This starter template reuses the data generation and evaluation
functions from vehicle_health.py. It displays live-updating
metrics and a simple line chart of recent values.

You'll need to install streamlit before running:
    pip install streamlit

The dashboard uses Streamlit's session_state to hold recent
measurements and updates once per second.
"""
import random
import time
import streamlit as st
from collections import deque

# --- reuse logic from vehicle_health.py (could also import) ---

def generate_vehicle_data(prev_data=None):
    if prev_data is None:
        return {
            'engine_temp': random.uniform(70, 120),
            'battery': random.uniform(11.0, 14.5),
            'rpm': random.uniform(800, 6000),
            'speed': random.uniform(0, 120),
            'fuel': random.uniform(0, 100),
        }
    return {
        'engine_temp': min(120, max(70, prev_data['engine_temp'] + random.uniform(-2, 2))),
        'battery': min(14.5, max(11.0, prev_data['battery'] + random.uniform(-0.1, 0.1))),
        'rpm': min(6000, max(800, prev_data['rpm'] + random.uniform(-100, 100))),
        'speed': min(120, max(0, prev_data['speed'] + random.uniform(-5, 5))),
        'fuel': min(100, max(0, prev_data['fuel'] + random.uniform(-1, 1))),
    }

def evaluate_health(data):
    critical = False
    warnings = 0
    if data['engine_temp'] > 110:
        critical = True
    if data['battery'] < 11.5:
        warnings += 1
    if data['rpm'] > 5000:
        warnings += 1
    if data['fuel'] < 10:
        warnings += 1
    if critical or warnings >= 2:
        return 'Critical'
    if warnings == 1:
        return 'Warning'
    return 'Healthy'

def calculate_health_score(data):
    score = 100
    if data['engine_temp'] > 105:
        score -= 20
    if data['battery'] < 11.5:
        score -= 15
    if data['rpm'] > 5000:
        score -= 10
    if data['fuel'] < 10:
        score -= 5
    return max(0, score)
# -------------------------------------------------------------

st.title("🚗 Smart Vehicle Health Dashboard")

# initialize session state queues for each measurement
if 'history' not in st.session_state:
    st.session_state.history = deque(maxlen=60)  # last minute
    st.session_state.prev = None

latest = st.empty()
import pandas as pd

chart = st.empty()

# main loop inside Streamlit
while True:
    data = generate_vehicle_data(st.session_state.prev)
    st.session_state.prev = data
    score = calculate_health_score(data)
    status = evaluate_health(data)

    st.session_state.history.append({**data, 'score': score, 'status': status})

    # display metrics
    latest.markdown(
        f"""
        **Engine Temp:** {data['engine_temp']:.1f} °C  
        **Battery:** {data['battery']:.2f} V  
        **RPM:** {int(data['rpm'])}  
        **Speed:** {data['speed']:.1f} km/h  
        **Fuel:** {data['fuel']:.1f} %  
        **Health Score:** {score}  
        **Health Status:** {status}  
        """
    )

    # chart recent numeric values only
    df = pd.DataFrame(st.session_state.history)
    # select only the numeric columns (drop status which is string)
    numeric_cols = ['engine_temp', 'battery', 'rpm', 'speed', 'fuel', 'score']
    chart.line_chart(df[numeric_cols])

    time.sleep(1)  # update every second
