from fastapi import FastAPI
from app.routes.ingestion import router as ingest_router
from app.routes.forecast import router as forecast_router
from app.routes.anomaly import router as anomaly_router
from app.routes.agents import router as agent_router
from app.routes.rag import router as rag_router
from app.routes.azuresearch import router as search_router
from app.routes.text_analytics_routes import router as text_router
from app.routes.openai_routes import router as openai_router

app = FastAPI(
    title="Smart Retail Assistant API",
    version="1.0.0"
)

app.include_router(ingest_router)
app.include_router(forecast_router)
app.include_router(anomaly_router)
app.include_router(rag_router)
app.include_router(agent_router)
app.include_router(search_router)
app.include_router(text_router)
app.include_router(openai_router)


# Home Route
@app.get("/")
def home():

    return {
        "status": "success",
        "message": "Retail AI Backend Running Successfully"
    }