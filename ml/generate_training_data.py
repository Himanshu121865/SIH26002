import numpy as np
import pandas as pd
import os


def generate_ner_disruption_data(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    data = {
        "rainfall_1h": np.random.exponential(2, n_samples).clip(0, 80),
        "rainfall_24h": np.random.exponential(15, n_samples).clip(0, 300),
        "rainfall_7d": np.random.exponential(60, n_samples).clip(0, 800),
        "slope_deg": np.random.uniform(5, 45, n_samples),
        "elevation_m": np.random.uniform(50, 3500, n_samples),
        "road_surface": np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.5, 0.2]),
        "historical_landslides": np.random.poisson(1.5, n_samples),
        "soil_moisture": np.random.beta(2, 5, n_samples),
        "distance_to_river_km": np.random.exponential(3, n_samples).clip(0.1, 50),
        "is_monsoon": np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        "road_quality_index": np.random.uniform(0.2, 1.0, n_samples),
        "nearby_settlement_count": np.random.poisson(3, n_samples),
        "month": np.random.randint(1, 13, n_samples),
        "hour_of_day": np.random.randint(0, 24, n_samples),
    }

    df = pd.DataFrame(data)

    risk = (
        0.35 * (df["rainfall_24h"] > 50).astype(float)
        + 0.25 * (df["slope_deg"] > 25).astype(float)
        + 0.15 * (df["rainfall_7d"] > 150).astype(float)
        + 0.10 * (df["soil_moisture"] > 0.6).astype(float)
        + 0.08 * (df["historical_landslides"] > 2).astype(float)
        + 0.07 * (df["distance_to_river_km"] < 1).astype(float)
        + np.random.normal(0, 0.1, n_samples)
    )

    df["disruption_label"] = (risk > 0.45).astype(int)

    return df


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_ner_disruption_data(5000)
    df.to_csv("data/ner_disruption_training.csv", index=False)
    print(f"Generated {len(df)} samples")
    print(f"Disruption rate: {df['disruption_label'].mean():.1%}")
    print(df.describe())
