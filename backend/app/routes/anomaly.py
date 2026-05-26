from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import pandas as pd
import joblib
from pathlib import Path

from app.utils import logger

router = APIRouter()

MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "anomaly_model.pkl"
)

# Load model safely
try:

    model = joblib.load(MODEL_PATH)

    logger.info(
        "Anomaly detection model loaded successfully"
    )

except Exception as e:

    logger.error(
        f"Model Loading Error: {str(e)}"
    )

    model = None


class AnomalyInput(BaseModel):

    Age: int = Field(..., examples=[34])

    Quantity: int = Field(..., examples=[3])

    Price_per_Unit: float = Field(
        ..., examples=[50.0]
    )

    Total_Amount: float = Field(
        ..., examples=[150.0]
    )

    Discount: float = Field(
        ..., examples=[10.0]
    )

    Holiday_Flag: int = Field(
        ..., ge=0, le=1, examples=[1]
    )

    Month: int = Field(
        ..., ge=1, le=12, examples=[5]
    )

    Weekday: int = Field(
        ..., ge=0, le=6, examples=[5]
    )


@router.post("/detect-anomaly")
def detect_anomaly(data: AnomalyInput):

    try:

        logger.info(
            "Anomaly detection request received"
        )

        # Check model loaded
        if model is None:

            logger.error(
                "Model not loaded"
            )

            raise HTTPException(
                status_code=500,
                detail="Model unavailable"
            )

        input_data = pd.DataFrame([{

            "Age": data.Age,

            "Quantity": data.Quantity,

            "Price_per_Unit": (
                data.Price_per_Unit
            ),

            "Total_Amount": (
                data.Total_Amount
            ),

            "Discount": data.Discount,

            "Holiday_Flag": (
                data.Holiday_Flag
            ),

            "Month": data.Month,

            "Weekday": data.Weekday
        }])

        logger.info(
            "Input data prepared successfully"
        )

        prediction = model.predict(
            input_data
        )

        # Isolation Forest
        # -1 = anomaly
        #  1 = normal

        result = (
            "Anomaly Detected"
            if prediction[0] == -1
            else "Normal Transaction"
        )

        logger.info(
            f"Prediction Result: {result}"
        )

        return {

            "status": "success",

            "prediction": result
        }

    except ValueError as e:

        logger.error(
            f"Validation Error: {str(e)}"
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        logger.error(
            f"Anomaly Detection Error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )