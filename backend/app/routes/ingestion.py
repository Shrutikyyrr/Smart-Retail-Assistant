from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import sales_data
from app.utils import logger

router = APIRouter()



class SalesData(BaseModel):

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



@router.post("/ingest-data")
def ingest_data(data: SalesData):

    try:

        logger.info(
            "Sales data ingestion request received"
        )


        sales_data_card = data.dict()

        logger.info(
            "Sales data converted to dictionary"
        )



        result = sales_data.insert_one(
            sales_data_card
        )

        logger.info(
            f"MongoDB insert successful: "
            f"{result.inserted_id}"
        )



        return {

            "status": "success",

            "message":
                "Sales data stored successfully "
                "in MongoDB Atlas",

            "inserted_id":
                str(result.inserted_id)
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
            f"MongoDB Ingestion Error: "
            f"{str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to store sales data "
                "in MongoDB"
            )
        )