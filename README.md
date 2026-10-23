# AI-Enabled Tactical Telemetry Anomaly Detector

A real-time TCP socket simulation and machine learning pipeline built to ingest JSON tactical telemetry data and flag anomalies using an `Isolation Forest` model. Designed to bridge simulation backends with AI-driven monitoring interfaces.

## Features
- **Socket Streaming Server:** Multithreaded/TCP script generating structured mock telemetry packets (`speed`, `altitude`, `signal strength`).
- **Machine Learning Inference:** Utilizes `scikit-learn`'s Isolation Forest algorithm to process real-time incoming streams and flag environmental or operational outliers.
- **Low-Latency Architecture:** Designed for minimal overhead to feed inference loops back into game engines or HUD displays.

## Quickstart

1. Install dependencies:
   ```bash
   pip install scikit-learn numpy
