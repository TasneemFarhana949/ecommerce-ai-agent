from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
from datetime import datetime

from llm_handler import get_sql_from_question, get_human_readable_answer
from database_setup import get_db_schema

# Configuration
DB_FILE = "ecommerce_data.db"
CHARTS_DIR = "charts"

# Create charts folder if it doesn't exist
if not os.path.exists(CHARTS_DIR):
    os.makedirs(CHARTS_DIR)

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce Data AI Agent",
    description="An AI agent to answer questions about e-commerce data."
)

# Connect to the database
try:
    engine = create_engine(f"sqlite:///{DB_FILE}")
    db_schema = get_db_schema()
except Exception as e:
    print(f"FATAL: Could not connect to the database. Error: {e}")
    db_schema = "Error: Database not found."

# Request schema
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    question = request.question
    print(f"Received question: {question}")

    if not db_schema or "Error" in db_schema:
        raise HTTPException(status_code=500, detail="Database not configured.")

    # Step 1: Convert question to SQL
    sql_query = get_sql_from_question(db_schema, question)
    print(f"> SQL Query: {sql_query}")

    if "Error" in sql_query:
        raise HTTPException(status_code=500, detail=sql_query)

    # Step 2: Execute query
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
            print(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL execution error: {e}")

    # Step 3: Get human-readable answer
    readable_answer = get_human_readable_answer(question, df.to_string(index=False))

    # Step 4: Generate chart (optional)
    chart_base64 = None
    chart_filename = None
    try:
        value = df.iloc[0, 0]
        label = "Result"
        title = "Chart"

        if "roas" in question.lower():
            label = "ROAS"
            title = "Return on Ad Spend"
        elif "total sales" in question.lower():
            label = "Total Sales"
            title = "Total Sales Overview"
        elif "cpc" in question.lower():
            label = "CPC"
            title = "Cost Per Click"

        if isinstance(value, (int, float)):
            plt.figure()
            plt.bar([label], [value], color="skyblue")
            plt.title(title)
            plt.ylabel(label)

            # Save chart as PNG
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            chart_filename = f"{CHARTS_DIR}/{label.lower()}_{timestamp}.png"
            plt.savefig(chart_filename)

            # Encode chart to base64
            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            chart_base64 = base64.b64encode(buf.read()).decode("utf-8")
            buf.close()
            plt.close()
    except Exception as e:
        print("Chart generation failed:", e)

    # Step 5: Return response
    return {
        "question": question,
        "generated_sql_query": sql_query,
        "database_result": df.replace({pd.NA: None, float("nan"): None}).to_dict(orient="records"),
        "answer": readable_answer,
        "chart_image_base64": chart_base64,
        "chart_image_file": chart_filename  # Local file for demo/video
    }

@app.get("/")
def read_root():
    return {"message": "E-commerce AI Agent is ready. POST to /ask."}
