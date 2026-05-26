import json
import joblib
import pandas as pd

def init():

    global model

    model = joblib.load(
        "forecast_model.pkl"
    )

def run(raw_data):

    data = json.loads(raw_data)

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return {
        "forecast": prediction.tolist()
    }