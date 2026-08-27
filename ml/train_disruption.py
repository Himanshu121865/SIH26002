import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import joblib
import os


def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df["rainfall_1h"] = df.get("rainfall_1h", 0)
    df["rainfall_24h"] = df.get("rainfall_24h", 0)
    df["rainfall_7d"] = df.get("rainfall_7d", 0)
    df["slope_deg"] = df.get("slope_deg", 0)
    df["elevation_m"] = df.get("elevation_m", 0)
    df["road_surface"] = df.get("road_surface", 0)
    df["historical_landslides"] = df.get("historical_landslides", 0)
    df["soil_moisture"] = df.get("soil_moisture", 0)
    df["distance_to_river_km"] = df.get("distance_to_river_km", 100)
    return df


FEATURE_COLS = [
    "rainfall_1h", "rainfall_24h", "rainfall_7d",
    "slope_deg", "elevation_m", "road_surface",
    "historical_landslides", "soil_moisture", "distance_to_river_km",
]


def train(csv_path: str, output_path: str):
    df = load_data(csv_path)
    df = engineer_features(df)

    X = df[FEATURE_COLS]
    y = df["disruption_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    xgb_model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42,
    )
    xgb_model.fit(X_train, y_train)

    y_pred = xgb_model.predict(X_test)
    print("=== XGBoost Classification Report ===")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    rf_model = RandomForestClassifier(
        n_estimators=200, max_depth=10, random_state=42
    )
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    print("\n=== Random Forest Classification Report ===")
    print(classification_report(y_test, y_pred_rf))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump({"xgb": xgb_model, "rf": rf_model, "features": FEATURE_COLS}, output_path)
    print(f"\nModels saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to training CSV")
    parser.add_argument("--output", default="models/disruption_model.pkl")
    args = parser.parse_args()
    train(args.data, args.output)
