from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.azure_services.text_analytics_service import (
    analyze_sentiment
)

from app.utils import logger

router = APIRouter()


class TextRequest(BaseModel):
    text: str


@router.post("/sentiment")
def sentiment_analysis(
    request: TextRequest
):

    try:

        logger.info(
            f"Sentiment Analysis Request: "
            f"{request.text}"
        )


        if not request.text.strip():

            logger.warning(
                "Empty text received"
            )

            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )



        result = analyze_sentiment(
            request.text
        )

        logger.info(
            "Sentiment analysis completed "
            "successfully"
        )



        if not result:

            logger.warning(
                "Empty sentiment response received"
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "Sentiment service "
                    "returned empty response"
                )
            )

    

        return {

            "status": "success",

            "text":
                request.text,

            "result":
                result
        }

    except ValueError as e:

        logger.error(
            f"Validation Error: {str(e)}"
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except HTTPException as http_error:

        raise http_error

    except Exception as e:

        logger.error(
            f"Sentiment Analysis Error: "
            f"{str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Sentiment Analysis Failed"
        )