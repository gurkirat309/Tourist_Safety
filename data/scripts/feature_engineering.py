import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

GPS_PATH = "data/generated/gps_with_anomalies.csv"
RISK_PATH = "data/raw/area_risk.csv"
OUTPUT_PATH = "data/generated/tourist_features.csv"


# Haversine distance (km)
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c


def compute_features():
    gps = pd.read_csv(GPS_PATH, parse_dates=["timestamp"])
    risk = pd.read_csv(RISK_PATH)

    features = []

    for tourist_id, df in gps.groupby("tourist_id"):
        df = df.sort_values("timestamp")

        # Speed features
        avg_speed = df["speed_kmph"].mean()
        speed_var = df["speed_kmph"].var()

        # Distance
        total_distance = 0
        for i in range(1, len(df)):
            total_distance += haversine(
                df.iloc[i-1]["latitude"],
                df.iloc[i-1]["longitude"],
                df.iloc[i]["latitude"],
                df.iloc[i]["longitude"]
            )

        # Stop duration (speed == 0)
        stop_minutes = (df["speed_kmph"] == 0).sum() * 5

        # Night travel (8 PM – 6 AM)
        night_moves = df["timestamp"].dt.hour.between(20, 23) | df["timestamp"].dt.hour.between(0, 6)
        night_ratio = night_moves.mean()

        # Area risk (nearest zone approximation)
        avg_risk = risk["risk_score"].mean()

        features.append({
            "tourist_id": tourist_id,
            "avg_speed": round(avg_speed, 2),
            "speed_variance": round(speed_var, 2),
            "total_distance_km": round(total_distance, 2),
            "stop_duration_minutes": stop_minutes,
            "gps_points_count": len(df),
            "avg_area_risk": round(avg_risk, 2),
            "night_travel_ratio": round(night_ratio, 2)
        })

    feature_df = pd.DataFrame(features)
    feature_df.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ Feature table generated: {OUTPUT_PATH}")
    print(feature_df.head())


if __name__ == "__main__":
    compute_features()
