import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

BASE_LAT = 26.9124   # Example: Jaipur
BASE_LON = 75.7873

OUTPUT_PATH = "data/generated/gps_with_anomalies.csv"

def generate_tourist_path(tourist_id, steps=120):
    records = []
    lat, lon = BASE_LAT, BASE_LON
    timestamp = datetime.now()

    anomaly_type = random.choice(
        ["normal", "stop", "deviation", "signal_loss"]
    )

    for i in range(steps):
        if anomaly_type == "stop" and 40 < i < 70:
            speed = 0.0

        elif anomaly_type == "deviation" and i > 60:
            lat += np.random.uniform(0.01, 0.02)
            lon += np.random.uniform(0.01, 0.02)
            speed = np.random.uniform(15, 25)

        elif anomaly_type == "signal_loss" and i > 90:
            break

        else:
            lat += np.random.uniform(-0.0005, 0.0005)
            lon += np.random.uniform(-0.0005, 0.0005)
            speed = np.random.uniform(5, 20)

        records.append({
            "tourist_id": tourist_id,
            "timestamp": timestamp,
            "latitude": lat,
            "longitude": lon,
            "speed_kmph": round(speed, 2),
            "gps_accuracy_m": round(np.random.uniform(3, 10), 2)
        })

        timestamp += timedelta(minutes=5)

    return records


def main():
    os.makedirs("data/generated", exist_ok=True)

    all_records = []
    for i in range(50):  # 50 tourists
        all_records.extend(generate_tourist_path(f"T{i:03}"))

    df = pd.DataFrame(all_records)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ GPS data generated: {OUTPUT_PATH}")
    print(df.head())


if __name__ == "__main__":
    main()
