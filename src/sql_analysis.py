
import pandas as pd
from sqlalchemy import text

from postgres_connection import engine


# =====================================================
# STEP 1: DEFINE SQL QUERY
# =====================================================

query = """
SELECT
    "Churn Label" AS churn_status,

    COUNT(*) AS total_customers,

    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage

FROM public.telco_customers_raw

GROUP BY "Churn Label"

ORDER BY total_customers DESC;
"""


# =====================================================
# STEP 2: EXECUTE SQL FROM PYTHON
# =====================================================

with engine.connect() as connection:

    result_df = pd.read_sql(
        text(query),
        connection
    )


# =====================================================
# STEP 3: DISPLAY RESULTS
# =====================================================

print("\nCUSTOMER CHURN ANALYSIS")
print("=" * 50)

print(result_df)
