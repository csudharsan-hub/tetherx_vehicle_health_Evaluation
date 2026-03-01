# Smart Vehicle Health Evaluation System

This repository contains a Python-based simulation that generates random vehicle data, evaluates health rules, and displays results in both console and Streamlit dashboard formats. It also includes a simple machine learning pipeline.

## Contents

- `vehicle_health.py` - Core simulator and health evaluation engine. Prints values to the console every second.
- `vehicle_health_streamlit.py` - Streamlit dashboard demonstrating real-time metrics and history chart.
- `vehicle_health_ml.py` - Workflow that generates a dataset, trains a Decision Tree classifier, and evaluates it.

## Features

- **Random data generation**: Parameters are generated within realistic ranges and vary slightly each second.
- **Health rules**:
  - Engine temperature > 110°C ⇒ Critical
  - Battery voltage < 11.5 V ⇒ Warning
  - RPM > 5000 ⇒ Warning
  - Fuel level < 10% ⇒ Warning
  - Multiple warnings or a critical condition ⇒ Critical status
- **Health score**: Starts at 100, deducts based on thresholds; classified as Healthy (80–100), Warning (50–79), or Critical (<50).
- **Modular design**: Functions `generate_vehicle_data`, `evaluate_health`, `calculate_health_score`, and `main` keep logic organized.
- **Streamlit dashboard**: Live-view with metrics and a line chart of recent numeric values.
- **Machine learning example**: Train a classifier on generated data to predict health status.

## Setup & Usage

1. **Clone the repo or download files**

2. **Install dependencies** (optional):
   ```bash
   pip install streamlit scikit-learn pandas
   ```

to run each component:

- **Console simulator**:
  ```bash
  python vehicle_health.py
  ```

- **Streamlit dashboard**:
  ```bash
  streamlit run vehicle_health_streamlit.py
  ```

- **ML pipeline**:
  ```bash
  python vehicle_health_ml.py
  ```

## Extending the project

- Convert the Streamlit app to include gauges, maps, or controls.
- Replace random data generator with real telemetry sources.
- Use the ML model to make future predictions and integrate it into the dashboard.
- Add logging, alerts (email/SMS), or deploy as a web service.

## License

This project is provided for educational/demo purposes. No license specified. Feel free to modify.
