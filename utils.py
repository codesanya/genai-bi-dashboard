"""
Helper utilities: run SQL to pandas, detect column types, and map results to Plotly charts.
"""
import pandas as pd


def to_dataframe(cursor, rows):
    """Convert SQLAlchemy cursor result to pandas DataFrame when cursor returns description and rows."""
    try:
        cols = [col[0] for col in cursor.description]
        df = pd.DataFrame(rows, columns=cols)
    except Exception:
        df = pd.DataFrame(rows)
    return df


def choose_chart_and_render(df):
    """
    Heuristic chart chooser. Returns a tuple (chart_type, plotly_figure) where chart_type is a string.

    Rules:
    - If DataFrame has 'order_date' or a datetime-like column + numeric value -> time series line chart aggregated by date.
    - If there are 2 columns and one is categorical -> bar chart of aggregation.
    - If numeric columns >1 -> scatter.
    - Otherwise -> table.
    """
    import plotly.express as px

    # normalize column names
    cols = list(df.columns)

    # check for datetime-like columns
    date_cols = [c for c in cols if 'date' in c.lower() or 'time' in c.lower()]

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    if len(date_cols) >= 1 and len(numeric_cols) >= 1:
        date_col = date_cols[0]
        # aggregate by date
        df2 = df.copy()
        df2[date_col] = pd.to_datetime(df2[date_col])
        df2 = df2.groupby(df2[date_col].dt.to_period('M')).sum().reset_index()
        df2[date_col] = df2[date_col].dt.to_timestamp()
        fig = px.line(df2, x=date_col, y=numeric_cols, markers=True)
        return 'timeseries', fig

    if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
        cat = categorical_cols[0]
        num = numeric_cols[0]
        df2 = df.groupby(cat)[num].sum().reset_index().sort_values(num, ascending=False)
        fig = px.bar(df2, x=cat, y=num)
        return 'bar', fig

    if len(numeric_cols) >= 2:
        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], hover_data=cols)
        return 'scatter', fig

    # fallback: render table
    fig = px.scatter(df.reset_index(), x=df.index, y=[df.columns[0]]) if df.shape[1] >= 1 else None
    return 'table', None
