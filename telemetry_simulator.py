import json
import random
import socket
import time

HOST = "127.0.0.1"
PORT = 65432


def generate_telemetry_packet():
  # Simulating tactical sensor telemetry for simulation/AR HUD
  packet = {
      "timestamp": time.time(),
      "unit_id": "UNIT-ALPHA-01",
      "speed_mps": round(random.uniform(10.0, 35.0), 2),
      "altitude_m": round(random.uniform(100.0, 500.0), 2),
      "signal_strength_dbm": round(random.uniform(-75.0, -40.0), 2),
      "status": "NOMINAL",
  }

  # Occasionally inject an anomaly (sudden speed/altitude spike)
  if random.random() < 0.1:
    packet["speed_mps"] = round(random.uniform(90.0, 150.0), 2)
    packet["status"] = "ANOMALY_DETECTED"

  return packet


def run_server():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"[*] Telemetry Simulator Server running on {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
      print(f"[+] Connected by client: {addr}")
      while True:
        packet = generate_telemetry_packet()
        data = json.dumps(packet) + "\n"
        conn.sendall(data.encode("utf-8"))
        time.sleep(1.0)


if __name__ == "__main__":
  run_server()
