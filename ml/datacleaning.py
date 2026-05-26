import pandas as pd
import numpy as np

# DATA CLEANING

def clean_sales_data(
    raw_df: pd.DataFrame
) -> pd.DataFrame:

    df = raw_df.copy()

    # REMOVE MISSING VALUES

    df = df.dropna(subset=[
        "Date",
        "Quantity",
        "Price per Unit",
        "Total Amount"
    ])

    # CONVERT DATE COLUMN

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    # CONVERT NUMERIC COLUMNS

    numeric_columns = [

        "Age",

        "Quantity",

        "Price per Unit",

        "Total Amount",

        "Discount",

        "Holiday_Flag"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # REMOVE DUPLICATES

    df = df.drop_duplicates()

    # DATE FEATURES

    df["Weekday"] = (
        df["Date"].dt.weekday
    )

    df["Month"] = (
        df["Date"].dt.month
    )

    df["Year"] = (
        df["Date"].dt.year
    )

    df["Day"] = (
        df["Date"].dt.day
    )

    df["Quarter"] = (
        df["Date"].dt.quarter
    )

    # WEEKEND FLAG

    df["Weekend_Flag"] = (
        df["Weekday"] >= 5
    ).astype(int)

    return df


# ============================================
# FEATURE ENGINEERING
# ============================================

def feature_engineer(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    # ============================================
    # REVENUE PER ITEM
    # ============================================

    df["Revenue_Per_Item"] = (

        df["Total Amount"]

        / df["Quantity"]
    )

    # ============================================
    # DISCOUNTED PRICE
    # ============================================

    df["Discounted_Price"] = (

        df["Price per Unit"]

        * (1 - (df["Discount"] / 100))
    )

    # ============================================
    # HIGH DISCOUNT FLAG
    # ============================================

    df["High_Discount_Flag"] = (

        df["Discount"] >= 25
    ).astype(int)

    # ============================================
    # AGE GROUPS
    # ============================================

    df["Age_Group"] = pd.cut(

        df["Age"],

        bins=[0, 25, 40, 60, 100],

        labels=[
            "Young",
            "Adult",
            "Senior",
            "Old"
        ]
    )

    # ============================================
    # SALES CATEGORY
    # ============================================

    df["Sales_Category"] = pd.cut(

        df["Total Amount"],

        bins=[0, 200, 600, 1500, 5000],

        labels=[
            "Low",
            "Medium",
            "High",
            "Premium"
        ]
    )

    # ============================================
    # LAG FEATURES
    # ============================================

    df = df.sort_values("Date")

    df["Lag_1"] = (
        df["Total Amount"]
        .shift(1)
    )

    df["Lag_7"] = (
        df["Total Amount"]
        .shift(7)
    )

    # ============================================
    # ROLLING MEAN
    # ============================================

    df["Rolling_Mean_7"] = (

        df["Total Amount"]

        .rolling(window=7)

        .mean()
    )

    # ============================================
    # SALES TREND
    # ============================================

    df["Sales_Trend"] = (

        df["Lag_1"]

        - df["Lag_7"]
    )

    # ============================================
    # REMOVE NULLS FROM LAG FEATURES
    # ============================================

    df = df.dropna()

    return df