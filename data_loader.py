import os
import pandas as pd
from sqlalchemy import create_engine

# Step 1: Load the Excel file
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
df = pd.read_excel(url, engine="openpyxl")

# Step 2: Lowercase column names
df.columns = [col.lower() for col in df.columns]

# Step 3: Setup DB connection
db_url = os.getenv("DB_URL", "postgresql://postgres:postgres@postgres:5432/ecommerce")
engine = create_engine(db_url)

# Step 4: Convert 'invoicedate' to datetime
df['invoicedate'] = pd.to_datetime(df['invoicedate'])

# Step 5: Date-shifting function with your logic
def shift_dates_with_r2_year_logic(df):
    today = pd.Timestamp.today()
    current_month = today.month

    # Calculate r1 once using max invoicedate
    max_month = df['invoicedate'].max().month
    r1 = max_month - current_month

    def shift(row):
        original_date = row['invoicedate']
        data_year = original_date.year
        data_month = original_date.month
        data_day = original_date.day

        r2 = data_month - r1
        if r2 <= 0:
            r2 += 12
            final_year = data_year + 13
        else:
            final_year = data_year + 14

        try:
            return pd.Timestamp(year=final_year, month=r2, day=data_day)
        except ValueError:
            # Handle end of month cases
            return pd.Timestamp(year=final_year, month=r2, day=1) + pd.offsets.MonthEnd(0)

    df['invoicedate'] = df.apply(shift, axis=1)
    return df

# Step 6: Apply date shifting to entire DataFrame (call function once)
df = shift_dates_with_r2_year_logic(df)

# Step 7: Upload the modified data to the target table
df.to_sql("orders", engine, if_exists="replace", index=False)
print("Data loaded and dates shifted into 'orders' table successfully!")
