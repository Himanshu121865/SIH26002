import joblib
import argparse
import pandas as pd
from sklearn.metrics import classification_report, mean_absolute_error


def evaluate_disruption(model_path: str, test_csv: str):
    bundle = joblib.load(model_path)
    df = pd.read_csv(test_csv)
    features = bundle["features"]
    X = df[features]
    y = df["disruption_label"]

    for name in ["xgb", "rf"]:
        model = bundle[name]
        y_pred = model.predict(X)
        print(f"\n=== {name} ===")
        print(classification_report(y, y_pred))


def evaluate_eta(model_path: str, test_csv: str):
    bundle = joblib.load(model_path)
    df = pd.read_csv(test_csv)
    X = df[bundle["features"]]
    y = df["travel_time_minutes"]
    X_scaled = bundle["scaler"].transform(X)
    y_pred = bundle["model"].predict(X_scaled)
    print(f"MAE: {mean_absolute_error(y, y_pred):.2f} min")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--test-data", required=True)
    parser.add_argument("--type", choices=["disruption", "eta"], default="disruption")
    args = parser.parse_args()

    if args.type == "disruption":
        evaluate_disruption(args.model, args.test_data)
    else:
        evaluate_eta(args.model, args.test_data)
