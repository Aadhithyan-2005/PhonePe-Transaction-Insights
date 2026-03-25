import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "phonepe_db",
    "user":     "postgres",
    "password": "Eremika@0139",  
}

def get_engine():
    from urllib.parse import quote_plus
    password = quote_plus(DB_CONFIG['password'])  # safely encodes special characters
    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{password}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(url)

def create_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    tables = [
        """CREATE TABLE IF NOT EXISTS aggregated_transaction (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, transaction_type VARCHAR(100),
            transaction_count BIGINT, transaction_amount NUMERIC(20,2))""",

        """CREATE TABLE IF NOT EXISTS aggregated_user (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, registered_users BIGINT, app_opens BIGINT,
            brand VARCHAR(100), device_count BIGINT, device_percentage NUMERIC(6,4))""",

        """CREATE TABLE IF NOT EXISTS aggregated_insurance (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, insurance_type VARCHAR(100),
            transaction_count BIGINT, transaction_amount NUMERIC(20,2))""",

        """CREATE TABLE IF NOT EXISTS map_transaction (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, district VARCHAR(150),
            transaction_count BIGINT, transaction_amount NUMERIC(20,2))""",

        """CREATE TABLE IF NOT EXISTS map_user (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, district VARCHAR(150),
            registered_users BIGINT, app_opens BIGINT)""",

        """CREATE TABLE IF NOT EXISTS map_insurance (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, district VARCHAR(150),
            transaction_count BIGINT, transaction_amount NUMERIC(20,2))""",

        """CREATE TABLE IF NOT EXISTS top_transaction (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, entity_type VARCHAR(20), entity_name VARCHAR(150),
            transaction_count BIGINT, transaction_amount NUMERIC(20,2))""",

        """CREATE TABLE IF NOT EXISTS top_user (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, entity_type VARCHAR(20), entity_name VARCHAR(150),
            registered_users BIGINT)""",

        """CREATE TABLE IF NOT EXISTS top_insurance (
            id SERIAL PRIMARY KEY, state VARCHAR(100), year SMALLINT,
            quarter SMALLINT, entity_type VARCHAR(20), entity_name VARCHAR(150),
            transaction_count BIGINT, transaction_amount NUMERIC(20,2))""",
    ]

    for stmt in tables:
        cur.execute(stmt)

    conn.commit()
    cur.close()
    conn.close()
    print("All 9 tables created successfully!")

if __name__ == "__main__":
    create_tables()