# 🛍️ E-commerce AI Agent (GenAI Internship Task)

This project is a FastAPI-based AI agent that uses the **Google Gemini API** to understand natural language questions, convert them to SQL, and query an SQLite e-commerce database.

## 💡 Features
- Converts user questions to SQL using Gemini
- Executes SQL on local database
- Returns clean, human-readable answers
- 📈 Bonus: Generates charts for certain questions using Matplotlib

## ✅ Example Questions
- What is my total sales?
- Calculate the RoAS (Return on Ad Spend)
- Which product had the highest CPC?

## 🚀 Run the Project
1. Clone the repo:
```bash
git clone https://github.com/TasneemFarhana949/ecommerce-ai-agent.git
cd ecommerce-ai-agent
```
2. (Optional) Create & activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```
3.Install dependencies:
pip install -r requirements.txt

4.Set your Google Gemini API Key

$env:GOOGLE_API_KEY="your_api_key_here"    # Windows PowerShell
export GOOGLE_API_KEY="your_api_key_here"  # Mac/Linux or Git Bash
Get your key from https://aistudio.google.com/apikey

5.Run the app:
uvicorn main:app --reload

6.Test in Postman:
POST to http://127.0.0.1:8000/ask with:
json
{
  "question": "What is my total sales?"
}

📊 Chart Output (Bonus Feature)
Certain queries like RoAS or Total Sales generate charts.
These charts are returned in Base64 format in the API response and saved in the charts/ folder (if not ignored by .gitignore).

project structure :
ecommerce-ai-agent/
│
├── data/                  # CSV files
├── charts/                # Chart images (auto-generated)
├── main.py                # FastAPI app
├── llm_handler.py         # Gemini API logic
├── database_setup.py      # Converts CSV → SQLite
├── ecommerce_data.db      # SQLite DB (auto-generated)
├── requirements.txt       # Python dependencies
└── README.md              # You're reading it!

👩‍💻 Author
Tasneem Farhana
🔗 GitHub
