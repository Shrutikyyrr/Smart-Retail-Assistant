from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.azure_services.azure_openai_service import (
    generate_retail_insight
)

from app.utils import logger

router = APIRouter()



class QueryRequest(BaseModel):
    query: str



@router.post("/ask-ai")
def ask_ai(data: QueryRequest):

    try:

        logger.info(
            f"AI Request Received: "
            f"{data.query}"
        )


        result = generate_retail_insight(
            data.query
        )

        logger.info(
            "Azure OpenAI response generated "
            "successfully"
        )



        if not result:

            logger.warning(
                "Empty AI response received"
            )

            raise HTTPException(
                status_code=500,
                detail="AI returned empty response"
            )



        return {

            "status": "success",

            "query": data.query,

            "response": result
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
            f"Azure OpenAI Route Error: "
            f"{str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Azure AI Service Failed"
        )