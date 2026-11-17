import pandas as pd

# ============================================================
# STEP 1: LOAD DATASET
# ============================================================

df = pd.read_csv("dataset/raw/telco.csv")


# ============================================================
# STEP 2: DATA QUALITY HEALTH CHECK
# ============================================================

print("=" * 60)
print("        DATA QUALITY HEALTH CHECK")
print("=" * 60)

# Dataset shape
print("\n1. Dataset Shape")
print("Rows, Columns:", df.shape)

# Column names
print("\n2. Columns")
print(df.columns.tolist())

# Data types
print("\n3. Data Types")
print(df.dtypes)

# Missing values
print("\n4. Missing Values")
print(df.isnull().sum())

# Duplicate rows
print("\n5. Duplicate Rows")
print(df.duplicated().sum())

# First 5 records
print("\n6. First 5 Records")
print(df.head())

print("\n" + "=" * 60)
print("        HEALTH CHECK COMPLETED")
print("=" * 60)