import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from src.database import DB_PATH

def execute_sql_query(query: str) -> str:
    """Executes a SQL read query on the business database and returns results as a string."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        if df.empty:
            return "Query returned no results."
        return df.to_string(index=False)
    except Exception as e:
        return f"Error executing query: {str(e)}"

def generate_revenue_chart() -> str:
    """Generates a bar chart of total revenue by product and saves it. Returns the file path."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT product, SUM(revenue) as total_revenue FROM sales GROUP BY product", conn)
        conn.close()

        plt.figure(figsize=(8, 4))
        plt.bar(df['product'], df['total_revenue'], color='skyblue')
        plt.title('Total Revenue by Product')
        plt.xlabel('Product')
        plt.ylabel('Revenue ($)')
        plt.tight_layout()
        
        static_dir = os.path.join(os.path.dirname(__file__), "../static")
        os.makedirs(static_dir, exist_ok=True)
        chart_path = os.path.join(static_dir, "revenue_chart.png")
        plt.savefig(chart_path)
        plt.close()
        
        return f"Chart successfully generated and saved to {chart_path}"
    except Exception as e:
        return f"Failed to generate chart: {str(e)}"

# A manifest explaining available tools to the LLM
TOOLS_MANIFEST = {
    "execute_sql_query": {
        "description": "Run a read-only SQL query on the sales database. Tables: sales (id, date, product, category, units_sold, revenue)",
        "func": execute_sql_query
    },
    "generate_revenue_chart": {
        "description": "Generates and saves a bar chart illustrating total revenue performance by product.",
        "func": generate_revenue_chart
    }
}