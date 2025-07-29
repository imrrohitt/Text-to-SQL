import os
import time
import sqlite3
import vanna
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = ""

# Initialize Vanna with OpenAI's gpt-4o-mini and ChromaDB
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

vanna = MyVanna(config={'api_key': os.environ["OPENAI_API_KEY"], 'model': 'gpt-4o-mini'})

# Connect to SQLite
conn = sqlite3.connect('ecommerce.db')

# Train Vanna on the schema
schema_ddl = """
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    product_id TEXT,
    city TEXT,
    order_date DATETIME,
    quantity INTEGER
);

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT
);
"""
vanna.train(ddl=schema_ddl)

# Function to execute SQL with retry logic
def execute_with_retry(vanna, question, max_retries=3):
    attempt = 0
    last_error = None
    cursor = conn.cursor()
    while attempt < max_retries:
        try:
            # Generate SQL
            sql = vanna.generate_sql(question)
            print(f"Attempt {attempt + 1} - Generated SQL: {sql}")

            # Execute SQL
            cursor.execute(sql)
            results = cursor.fetchall()
            conn.commit()
            return results, sql
        except sqlite3.Error as e:
            last_error = str(e)
            print(f"Error executing query: {last_error}")
            attempt += 1
            if attempt < max_retries:
                # Refine query based on error
                refined_question = f"Fix this SQL query that failed with error '{last_error}': {sql}"
                sql = vanna.generate_sql(refined_question)
                print(f"Retrying with refined SQL: {sql}")
                time.sleep(1)  # Avoid rate limits
            else:
                raise Exception(f"Max retries reached. Could not generate executable SQL. Last error: {last_error}")
        finally:
            cursor.close()

# Test queries
questions = [
    "Show the top 10 products sold in Bangalore in the last 7 days.",
    "List users who made more than 3 purchases in a month."
]

for question in questions:
    print(f"\nQuestion: {question}")
    try:
        results, sql = execute_with_retry(vanna, question)
        print(f"Results: {results}")
    except Exception as e:
        print(f"Failed to execute: {e}")

# Close the database connection
conn.close()

# Optional: Launch a Flask UI for interactive testing
# from vanna.flask import VannaFlaskApp
# app = VannaFlaskApp(vanna)
# app.run()