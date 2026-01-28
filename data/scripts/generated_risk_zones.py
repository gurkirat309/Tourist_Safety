import pandas as pd
import numpy as np
import os

OUTPUT_PATH = "data/raw/area_risk.csv"

def main():
    os.makedirs("data/raw", exist_ok=True)

    zones = []

    for i in range(12):
        risk = np.random.uniform(0.2, 0.9)
        zones.append({
            "area_id": f"ZONE_{i}",
            "latitude": 26.9 + np.random.uniform(-0.05, 0.05),
            "longitude": 75.78 + np.random.uniform(-0.05, 0.05),
            "risk_score": round(risk, 2),
            "zone_type": "high" if risk > 0.7 else "moderate"
        })

    df = pd.DataFrame(zones)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ Area risk data generated: {OUTPUT_PATH}")
    print(df.head())


if __name__ == "__main__":
    main()
