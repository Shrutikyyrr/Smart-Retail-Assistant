from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.agents.document_agent import document_agent
from app.agents.analytics_agent import analytics_agent
from app.agents.expert_agent import expert_agent

from app.utils import logger

router = APIRouter()


# Request Schema
class AgentRequest(BaseModel):
    question: str
    input_data: Optional[Dict[str, Any]] = None


# Unified Multi-Agent Route
@router.post("/agent_chat")
def agent_chat(data: AgentRequest):

    try:

        logger.info(
            f"Received Agent Query: {data.question}"
        )

        question = data.question.lower()

        # ML Expert Agent
        if (
            "predict" in question
            or "forecast" in question
            or "future sales" in question
            or "revenue prediction" in question
        ):

            logger.info(
                "Selected Agent: ML Expert Agent"
            )

            if data.input_data:

                query = f"""
                Question:
                {data.question}

                ML Data:
                {data.input_data}
                """

            else:

                query = data.question

            response = expert_agent(query)

            selected_agent = "ML Expert Agent"

        # Analytics Agent
        elif (
            "analytics" in question
            or "sales trend" in question
            or "trend" in question
            or "anomaly" in question
            or "business insight" in question
            or "customer behavior" in question
        ):

            logger.info(
                "Selected Agent: Data Analyst Agent"
            )

            response = analytics_agent(
                data.question
            )

            selected_agent = (
                "Data Analyst Agent"
            )

        # Document Agent
        else:

            logger.info(
                "Selected Agent: Document Assistant Agent"
            )

            response = document_agent(
                data.question
            )

            selected_agent = (
                "Document Assistant Agent"
            )

        logger.info(
            f"Agent Response Generated Successfully"
        )

        return {
            "status": "success",
            "selected_agent": selected_agent,
            "question": data.question,
            "response": response
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
            f"Agent Route Error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )