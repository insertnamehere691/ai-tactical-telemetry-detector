import json
import socket
import numpy as np
from sklearn.ensemble import IsolationForest

HOST = "127.0.0.1"
PORT = 65432


def run_detector():
  print("[*] Initializing AI Telemetry Anomaly Detector...")

  # Warm up the Isolation Forest model with normal baseline data
  # Features: [speed_mps, altitude_m, signal_strength_dbm]
  baseline_data = np.array([
      [20.0, 250.0, -55.0],
      [22.5, 255.0, -52.0],
      [18.0, 245.0, -58.0],
      [25.0, 260.0, -50.0],
      [19.5, 248.0, -56.0],
  ])

  model = IsolationForest(contamination=0.1, random_state=42)
  model.fit(baseline_data)

  print(
      "[*] Connecting to telemetry stream and running real-time AI"
      " inference..."
  )

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    buffer = ""

    while True:
      chunk = s.recv(1024).decode("utf-8")
      if not chunk:
        break
      buffer += chunk

      while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        if not line.strip():
          continue

        packet = json.loads(line)
        features = np.array([[
            packet["speed_mps"],
            packet["altitude_m"],
            packet["signal_strength_dbm"],
        ]])

        # Predict: 1 = Normal, -1 = Outlier / Anomaly
        prediction = model.predict(features)[0]

        if prediction == -1:
          print(
              f"[!] ANOMALY DETECTED! Unit: {packet['unit_id']} | Data:"
              f" {packet}"
          )
        else:
          print(
              f"[+] Nominal telemetry received from {packet['unit_id']} | Speed:"
              f" {packet['speed_mps']} m/s"
          )


if __name__ == "__main__":
  run_detector()
