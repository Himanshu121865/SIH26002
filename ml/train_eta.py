import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os


def load_data(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)


ETA_FEATURES = [
    "distance_km", "road_type_encoded", "slope_avg",
    "elevation_change", "weather_severity", "traffic_density",
    "num_stops", "surface_quality", "curvature_index",
]


def train(csv_path: str, output_path: str):
    df = load_data(csv_path)
    X = df[ETA_FEATURES]
    y = df["travel_time_minutes"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    from xgboost import XGBRegressor
    model = XGBRegressor(
        n_estimators=300, max_depth=8, learning_rate=0.05, random_state=42
    )
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"MAE: {mae:.2f} minutes")
    print(f"RMSE: {rmse:.2f} minutes")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(
        {"model": model, "scaler": scaler, "features": ETA_FEATURES},
        output_path,
    )
    print(f"ETA model saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", default="models/eta_model.pkl")
    args = parser.parse_args()
    train(args.data, args.output)
