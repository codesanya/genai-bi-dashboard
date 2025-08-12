# GenAI-Powered Business Intelligence Dashboard

A **Generative AI-driven dashboard** that integrates **LangChain**, **Streamlit**, **Plotly**, and an **SQL backend** to allow stakeholders to query business datasets in plain English and receive **instant visual insights**.

---

## 🚀 Features
- **Natural Language Querying**: Use everyday language to fetch insights from structured datasets.
- **Interactive Visualizations**: Dynamic plots using Plotly.
- **Automated Insights**: LangChain + OpenAI integration for intelligent query translation.
- **SQL Backend**: Efficient querying and data storage.
- **End-to-End Local Setup**: Comes with a sample dataset and database initializer.

---

## 📂 Project Structure
```markdown
genai-bi-dashboard/
│
├── app.py # Streamlit dashboard app
├── create_db.py # Script to initialize sample SQLite DB
├── utils.py # Utility functions (query handling, plotting)
├── sample_data.csv # Sample dataset
├── requirements.txt # Dependencies
└── README.md # Documentation

```
---

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/genai-bi-dashboard.git
cd genai-bi-dashboard

```
---
2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
---
3. **Install dependencies**

```bash
pip install -r requirements.txt
```
---
4. **Set your OpenAI API Key**

```bash
export OPENAI_API_KEY="your_api_key_here"   # macOS/Linux
setx OPENAI_API_KEY "your_api_key_here"     # Windows

```
---
5. **Initialize the sample database**

```bash
python create_db.py

```
---
2. **Run the app**

```bash
streamlit run app.py
```
---
## 📊 Sample Queries
You can ask:

- "Show total sales by region"

- "Top 5 customers by revenue"

- "Monthly sales trend for 2023"

---

## Results
1. **Query Example: "Show sales by region"**
- Generated SQL:
```sql
SELECT region, SUM(sales) FROM sales_data GROUP BY region;

```
- Result:
  A bar chart showing total sales for each region.
---
2. **Query Example: "Monthly sales trend for 2023"**
- Generated SQL:
```sql
SELECT month, SUM(sales) FROM sales_data 
WHERE year = 2023 GROUP BY month;

```
- Result:
  A line chart illustrating monthly sales trends.
---
