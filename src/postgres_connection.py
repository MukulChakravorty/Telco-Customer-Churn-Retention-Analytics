
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# =====================================================
# STEP 1: LOAD ENVIRONMENT VARIABLES
# =====================================================

project_root = Path(__file__).resolve().parents[1]

env_path = project_root / ".env"

load_dotenv(env_path)


# =====================================================
# STEP 2: READ DATABASE CREDENTIALS
# =====================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# =====================================================
# STEP 3: VALIDATE CREDENTIALS
# =====================================================

required_values = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD
}

missing_values = [
    key for key, value in required_values.items()
    if not value
]

if missing_values:
    raise ValueError(
        f"Missing database configuration: {missing_values}"
    )


# =====================================================
# STEP 4: CREATE DATABASE URL SAFELY
# =====================================================

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)


# =====================================================
# STEP 5: CREATE SQLALCHEMY ENGINE
# =====================================================

engine = create_engine(connection_url)


# =====================================================
# STEP 6: TEST DATABASE CONNECTION
# =====================================================

def test_connection():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT current_database(), current_user")
        )

        database_name, username = result.fetchone()

        print("DATABASE CONNECTION SUCCESSFUL")
        print("--------------------------------")
        print("Database:", database_name)
        print("User:", username)


if __name__ == "__main__":
    test_connection()
