from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rag.vectordb import rag

from app.utils import logger

router = APIRouter()


class Query(BaseModel):
    question: str



@router.post("/search_docs")
def search_documents(data: Query):

    try:

        logger.info(
            f"RAG Search Request: "
            f"{data.question}"
        )



        if not data.question.strip():

            logger.warning(
                "Empty question received"
            )

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )



        response = rag(
            data.question
        )

        logger.info(
            "RAG response generated successfully"
        )



        if not response:

            logger.warning(
                "No response returned from RAG"
            )

            return {

                "status": "success",

                "response":
                    "No relevant documents found"
            }



        return {

            "status": "success",

            "question":
                data.question,

            "response":
                response
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
            f"RAG Search Error: "
            f"{str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="RAG Search Failed"
        )