import google.generativeai as genai
import os

# --- Configuration ---
# IMPORTANT: Set your Google API Key as an environment variable
# or replace "YOUR_API_KEY" with your actual key.
# It is highly recommended to use environment variables for security.


genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_sql_from_question(schema: str, question: str) -> str:
    """
    Uses the LLM to convert a natural language question into an SQL query.
    """
    prompt = f"""
    You are an expert SQL analyst. Based on the following database schema,
    write a single, executable SQL query to answer the user's question.
    Only return the SQL query and nothing else.

    **Database Schema:**
    {schema}

    **User Question:**
    "{question}"

    **SQL Query:**
    """
    try:
        response = model.generate_content(prompt)
        # Clean up the response to get only the SQL query
        sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
        return sql_query
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return "SELECT 'Error generating SQL query. Please check your API key and network.'"


def get_human_readable_answer(question: str, query_result: str) -> str:
    """
    Uses the LLM to convert the result of an SQL query into a human-readable response.
    """
    prompt = f"""
    You are a helpful AI assistant. You need to answer the user's question based on
    the data provided. The data is the result of an SQL query.

    **User's Original Question:**
    "{question}"

    **Data from Database:**
    {query_result}

    **Your Answer (in a clear, human-readable format):**
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating human-readable answer: {e}")
        return "Error interpreting the data. Could not generate a human-readable response."
