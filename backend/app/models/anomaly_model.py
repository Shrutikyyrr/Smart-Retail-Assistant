import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

import matplotlib.pyplot as plt
df = pd.read_csv(
    "/Users/shrutimishra/Downloads/updated_retail_sales_dataset.csv"
)

print("Dataset Loaded Successfully")

# CONVERT DATE

df["Date"] = pd.to_datetime(df["Date"])

# DATE FEATURES

df["Year"] = df["Date"].dt.year

df["Month"] = df["Date"].dt.month

df["Day"] = df["Date"].dt.day

df["Weekday"] = df["Date"].dt.weekday

# SELECT FEATURES FOR ANOMALY DETECTION

features = [

    "Age",

    "Quantity",

    "Price per Unit",

    "Total Amount",

    "Discount",

    "Holiday_Flag",

    "Month",

    "Weekday"
]

X = df[features]

# FEATURE SCALING

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ISOLATION FOREST MODEL

model = IsolationForest(

    n_estimators=200,

    contamination=0.03,

    random_state=42
)

# TRAIN MODEL

model.fit(X_scaled)

# PREDICT ANOMALIES

df["Anomaly"] = model.predict(X_scaled)

# NORMAL  ->  1
# ANOMALY -> -1

df["Anomaly"] = df["Anomaly"].map({

    1: 0,

    -1: 1
})

# COUNT ANOMALIES

anomaly_count = df["Anomaly"].sum()

print(f"\nTotal Anomalies Detected : {anomaly_count}")

# SHOW ANOMALIES

anomalies = df[df["Anomaly"] == 1]

print("\n===== ANOMALOUS RECORDS =====")

print(anomalies.head())

# SAVE ANOMALY DATASET

df.to_csv(

    "retail_sales_with_anomalies.csv",

    index=False
)

print("\nDataset Saved Successfully")

# VISUALIZATION

plt.figure(figsize=(12,6))

plt.scatter(

    df.index,

    df["Total Amount"],

    c=df["Anomaly"],

    cmap="coolwarm"
)

plt.xlabel("Transaction Index")

plt.ylabel("Total Amount")

plt.title("Retail Sales Anomaly Detection")

plt.show()

joblib.dump(
    model,
    "backend/app/models/anomaly_model.pkl"
)