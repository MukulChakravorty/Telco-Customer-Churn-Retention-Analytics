
import pandas as pd
from sqlalchemy import text

from postgres_connection import engine


# ==========================================
# STEP 1: FETCH DATA FROM POSTGRESQL
# ==========================================

query = """
SELECT *
FROM public.telco_customers_raw;
"""


# ==========================================
# STEP 2: LOAD DATA INTO PANDAS
# ==========================================

with engine.connect() as connection:
    df = pd.read_sql(
        text(query),
        connection
    )


# ==========================================
# STEP 3: VALIDATE DATA
# ==========================================

print("DATA FETCHED SUCCESSFULLY")
print("--------------------------")

print("Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nData Types:")
print(df.dtypes)
