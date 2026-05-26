from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.azure_services.search_service import (
    search_documents
)

from app.utils import logger

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/azure-search")
def azure_search_route(
    request: SearchRequest
):

    try:

        logger.info(
            f"Azure Search Request: "
            f"{request.query}"
        )

        # Perform Azure Search
        results = search_documents(
            request.query
        )

        logger.info(
            "Azure Search completed successfully"
        )

        # Check empty results
        if not results:

            logger.warning(
                "No search results found"
            )

            return {
                "status": "success",
                "query": request.query,
                "results": [],
                "message":
                "No matching documents found"
            }

        logger.info(
            f"Total Results Found: "
            f"{len(results)}"
        )

        return {

            "status": "success",

            "query": request.query,

            "results": results
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
            f"Azure Search Route Error: "
            f"{str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Azure Search Failed"
        )