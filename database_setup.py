from sqlalchemy import create_engine, inspect 
import pandas as pd
import os

# --- Configuration ---
DB_FILE = "ecommerce_data.db"
DATA_DIR = "data"
CSV_FILES = {
    "eligibility": "eligibility.csv",
    "ad_metrics": "ad_metrics.csv",
    "total_sales": "total_sales.csv"
}

# Create a connection to the SQLite database
# The file will be created if it doesn't exist
engine = create_engine(f"sqlite:///{DB_FILE}")

def setup_database():
    """
    Reads CSV files from the /data directory and loads them into SQLite tables.
    """
    print("Setting up database...")
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory '{DATA_DIR}' not found.")
        print("Please create it and add your CSV files.")
        return

    for table_name, file_name in CSV_FILES.items():
        file_path = os.path.join(DATA_DIR, file_name)
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                # Ensure column names are clean (no spaces, special chars)
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
                df.to_sql(table_name, engine, if_exists='replace', index=False)
                print(f"Successfully loaded {file_name} into '{table_name}' table.")
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
        else:
            print(f"Warning: {file_name} not found in {DATA_DIR}. Skipping.")
    print("Database setup complete.")

def get_db_schema():
    """
    Retrieves the schema of the database tables.
    This is crucial for the LLM to understand the data structure.
    """
    schema_info = ""
    # This line below uses the 'inspect' function you imported
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    for table_name in table_names:
        schema_info += f"Table '{table_name}':\n"
        columns = inspector.get_columns(table_name)
        for col in columns:
            schema_info += f"  - {col['name']} ({col['type']})\n"
    return schema_info

if __name__ == "__main__":
    setup_database()
    print("\nDatabase Schema:")
    print(get_db_schema())