# genai-bi-dashboard
LangChain + Streamlit + Plotly + SQLite

## Overview
This project is an AI-driven analytics dashboard that allows users to query business data in natural language and get results instantly in interactive charts and tables.

It combines:

LangChain for converting questions to SQL queries.

SQLite as a lightweight database backend.

Streamlit for an easy-to-use web app interface.

Plotly for interactive data visualizations.

🚀 Features
Ask questions in plain English (e.g., "Show total sales by region for last quarter")

AI automatically generates SQL queries based on your dataset schema.

Interactive visualizations (bar, line, pie, scatter plots) generated automatically.

SQLite backend with pre-loaded sample dataset — works locally out-of-the-box.

No complex setup — just pip install and run.

📂 Project Structure
bash
Copy
Edit
📦 ai-bi-dashboard
 ┣ 📂 data
 ┃ ┗ sample.db             # SQLite database with sample sales data
 ┣ 📜 app.py                # Main Streamlit app
 ┣ 📜 utils.py              # Chart rendering and helper functions
 ┣ 📜 create_db.py          # Script to generate sample dataset
 ┣ 📜 requirements.txt      # Python dependencies
 ┗ 📜 README.md             # Project documentation
🛠️ Installation & Setup
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/ai-bi-dashboard.git
cd ai-bi-dashboard
Create virtual environment (recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Generate sample database

bash
Copy
Edit
python create_db.py
Run the dashboard

bash
Copy
Edit
streamlit run app.py
📊 Sample Results
Example 1: Sales by Region
Query:
"Show me total sales by region"

AI-Generated SQL:

sql
Copy
Edit
SELECT region, SUM(sales_amount) as total_sales
FROM sales
GROUP BY region;
Visualization:
Bar chart with Region on X-axis and Total Sales on Y-axis.


Example 2: Monthly Sales Trend
Query:
"Show monthly sales trend for 2024"

AI-Generated SQL:

sql
Copy
Edit
SELECT strftime('%Y-%m', date) as month, SUM(sales_amount) as total_sales
FROM sales
WHERE date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY month
ORDER BY month;
Visualization:
Line chart showing Month vs Total Sales.


Example 3: Top 5 Products by Revenue
Query:
"Top 5 products by revenue"

AI-Generated SQL:

sql
Copy
Edit
SELECT product_name, SUM(sales_amount) as revenue
FROM sales
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 5;
Visualization:
Horizontal bar chart with Products vs Revenue.


📌 Tech Stack
LangChain – LLM-powered SQL generation

Streamlit – Web app framework

Plotly – Interactive charts

SQLite – Lightweight database

📈 Potential Use Cases
Business intelligence dashboards for SMBs

Quick internal analytics without SQL expertise

Educational tool for learning data analytics + AI integration

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

📜 License
This project is licensed under the MIT License.
