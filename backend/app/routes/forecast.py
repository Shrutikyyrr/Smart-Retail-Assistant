from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import pandas as pd
import joblib

from app.utils import logger

router = APIRouter()


try:

    model = joblib.load(
        "app/models/forecast_model.pkl"
    )

    logger.info(
        "Forecast model loaded successfully"
    )

except Exception as e:

    logger.error(
        f"Model Loading Error: {str(e)}"
    )

    model = None



class Input(BaseModel):

    Transaction_ID: str

    Age: int

    Quantity: int

    Price_per_Unit: float

    Year: int
    Month: int
    Day: int

    Weekday: int
    Weekend_Flag: int

    Calculated_Total: float

    Gender_Male: int

    Product_Category_Clothing: int
    Product_Category_Electronics: int

    Age_Group_Young: int
    Age_Group_Adult: int
    Age_Group_Senior: int
    Age_Group_Old: int

    Holiday_Flag: int

    Discount: float



@router.post("/forecast")
def forecast_sales(data: Input):

    try:

        logger.info(
            "Forecast request received"
        )


        if model is None:

            logger.error(
                "Forecast model unavailable"
            )

            raise HTTPException(
                status_code=500,
                detail="Model unavailable"
            )


        data_dict = data.dict()

        logger.info(
            "Input data converted successfully"
        )


        try:

            transaction_numeric = int(
                data_dict["Transaction_ID"]
                .replace("TXN", "")
            )

        except Exception:

            logger.error(
                "Invalid Transaction ID format"
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    "Transaction_ID must "
                    "be like TXN1001"
                )
            )


        input_data = pd.DataFrame([{

            "Transaction ID":
                transaction_numeric,

            "Age":
                data_dict["Age"],

            "Quantity":
                data_dict["Quantity"],

            "Price_per_Unit":
                data_dict["Price_per_Unit"],

            "Year":
                data_dict["Year"],

            "Month":
                data_dict["Month"],

            "Day":
                data_dict["Day"],

            "Weekday":
                data_dict["Weekday"],

            "Weekend_Flag":
                data_dict["Weekend_Flag"],

            "Calculated_Total":
                data_dict["Calculated_Total"],

            "Gender_Male":
                data_dict["Gender_Male"],

            "Product_Category_Clothing":
                data_dict[
                    "Product_Category_Clothing"
                ],

            "Product_Category_Electronics":
                data_dict[
                    "Product_Category_Electronics"
                ],

            "Age_Group_Young":
                data_dict[
                    "Age_Group_Young"
                ],

            "Age_Group_Adult":
                data_dict[
                    "Age_Group_Adult"
                ],

            "Age_Group_Senior":
                data_dict[
                    "Age_Group_Senior"
                ],

            "Age_Group_Old":
                data_dict[
                    "Age_Group_Old"
                ],

            "Holiday_Flag":
                data_dict[
                    "Holiday_Flag"
                ],

            "Discount":
                data_dict["Discount"]

        }])

        logger.info(
            "Input dataframe created successfully"
        )


        prediction = model.predict(
            input_data
        )

        predicted_value = round(
            float(prediction[0]),
            2
        )

        logger.info(
            f"Forecast Prediction: "
            f"{predicted_value}"
        )


        return {

            "status": "success",

            "predicted_sales":
                predicted_value
        }

    except HTTPException as http_error:

        raise http_error

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
            f"Forecast Error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Forecast Prediction Failed"
        )