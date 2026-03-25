from data_extraction import extract_all
from db_setup import get_engine, create_tables

def load_all():
    print("Step 1/3 — Creating tables in PostgreSQL...")
    create_tables()

    print("\nStep 2/3 — Extracting data from PhonePe Pulse repo...")
    dataframes = extract_all()

    print("\nStep 3/3 — Loading data into PostgreSQL...")
    engine = get_engine()

    for table_name, df in dataframes.items():
        if df.empty:
            print(f"  [SKIP] {table_name} — empty, skipping.")
            continue
        try:
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="replace",
                index=False,
                method="multi",
                chunksize=1000,
            )
            print(f"  [OK] {table_name:30s} → {len(df):>6} rows loaded")
        except Exception as e:
            print(f"  [ERROR] {table_name}: {e}")

    print("\nAll data loaded successfully!")

if __name__ == "__main__":
    load_all()
