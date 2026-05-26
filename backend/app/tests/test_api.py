
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_root():

    response = client.get("/")

    assert response.status_code in [200, 404]

def test_ask_ai():

    response = client.post(
        "/ask-ai",
        json={
            "query":
            "Give retail sales insights"
        }
    )

    assert response.status_code == 200

# TEST SENTIMENT ANALYSIS

def test_sentiment_analysis():

    response = client.post(
        "/sentiment",
        json={
            "text":
            "The product quality is amazing"
        }
    )

    assert response.status_code == 200

# TEST AZURE SEARCH

def test_azure_search():

    response = client.post(
        "/azure-search",
        json={
            "query":
            "retail sales trends"
        }
    )

    assert response.status_code == 200


# TEST RAG SEARCH

def test_rag_search():

    response = client.post(
        "/search_docs",
        json={
            "question":
            "Explain customer behavior"
        }
    )

    assert response.status_code == 200


# TEST FORECAST ROUTE

def test_forecast_sales():

    response = client.post(
        "/forecast",
        json={

            "Transaction_ID": "TXN1001",

            "Age": 30,

            "Quantity": 5,

            "Price_per_Unit": 120.5,

            "Year": 2025,
            "Month": 5,
            "Day": 25,

            "Weekday": 0,
            "Weekend_Flag": 1,

            "Calculated_Total": 602.5,

            "Gender_Male": 1,

            "Product_Category_Clothing": 1,
            "Product_Category_Electronics": 0,

            "Age_Group_Young": 0,
            "Age_Group_Adult": 1,
            "Age_Group_Senior": 0,
            "Age_Group_Old": 0,

            "Holiday_Flag": 0,

            "Discount": 10
        }
    )

    assert response.status_code == 200

# TEST ANOMALY DETECTION
# ============================================

def test_anomaly_detection():

    response = client.post(
        "/detect-anomaly",
        json={

            "Age": 34,

            "Quantity": 3,

            "Price_per_Unit": 50.0,

            "Total_Amount": 150.0,

            "Discount": 10.0,

            "Holiday_Flag": 1,

            "Month": 5,

            "Weekday": 5
        }
    )

    assert response.status_code == 200


# ============================================
# TEST DATA INGESTION
# ============================================

def test_ingest_data():

    response = client.post(
        "/ingest-data",
        json={

            "Transaction_ID": "TXN1001",

            "Age": 29,

            "Quantity": 3,

            "Price_per_Unit": 120.5,

            "Year": 2025,
            "Month": 5,
            "Day": 25,

            "Weekday": 0,
            "Weekend_Flag": 1,

            "Calculated_Total": 361.5,

            "Gender_Male": 1,

            "Product_Category_Clothing": 1,
            "Product_Category_Electronics": 0,

            "Age_Group_Young": 0,
            "Age_Group_Adult": 1,
            "Age_Group_Senior": 0,
            "Age_Group_Old": 0,

            "Holiday_Flag": 0,

            "Discount": 10
        }
    )

    assert response.status_code == 200


# ============================================
# TEST MULTI AGENT ROUTE
# ============================================

def test_agent_chat():

    response = client.post(
        "/agent_chat",
        json={
            "question":
            "Predict future sales"
        }
    )

    assert response.status_code == 200