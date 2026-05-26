import pandas as pd

import numpy as np

import joblib

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.model_selection import TimeSeriesSplit

#load dataset

df = pd.read_csv(
    "/Users/shrutimishra/Downloads/updated_retail_sales_dataset.csv"
)

print("Dataset Loaded Successfully")

#date conversion

df["Date"] = pd.to_datetime(
    df["Date"]
)

#sort data

df = df.sort_values(
    "Date"
)

#weekday

df["Weekday"] = (
    df["Date"].dt.weekday
)

#weekend flag

df["Weekend_Flag"] = (
    df["Weekday"] >= 5
).astype(int)

#features

feature_columns = [

    "Transaction ID",

    "Age",

    "Quantity",

    "Price_per_Unit",

    "Year",

    "Month",

    "Day",

    "Weekday",

    "Weekend_Flag",

    "Calculated_Total",

    "Gender_Male",

    "Product_Category_Clothing",

    "Product_Category_Electronics",

    "Age_Group_Young",

    "Age_Group_Adult",

    "Age_Group_Senior",

    "Age_Group_Old",

    "Holiday_Flag",

    "Discount"
]

#input and target

X = df[feature_columns]

y = df["Total_Amount"]

#time series split

tscv = TimeSeriesSplit(
    n_splits=5
)

scores = []

#training the model

for train_index, test_index in tscv.split(X):

    X_train, X_test = (
        X.iloc[train_index],
        X.iloc[test_index]
    )

    y_train, y_test = (
        y.iloc[train_index],
        y.iloc[test_index]
    )

    #random forest regressor

    model = RandomForestRegressor(

        n_estimators=400,

        max_depth=15,

        min_samples_split=4,

        min_samples_leaf=2,

        max_features="sqrt",

        random_state=42,

        n_jobs=-1
    )

   #train

    model.fit(
        X_train,
        y_train
    )

   #predict

    predictions = model.predict(
        X_test
    )



    r2 = r2_score(
        y_test,
        predictions
    )

    scores.append(r2)


final_accuracy = np.mean(scores) * 100

mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = np.sqrt(mse)

#save the model

joblib.dump(
    model,
    "app/models/forecast_model.pkl"
)


print("\n========== MODEL RESULTS ==========")

print(
    f"Forecast Accuracy : "
    f"{final_accuracy:.2f}%"
)

print(f"MAE               : {mae}")

print(f"MSE               : {mse}")

print(f"RMSE              : {rmse}")

print(f"R2 Score          : {r2}")

print(
    "\nReduced Feature "
    "Random Forest Saved Successfully"
)