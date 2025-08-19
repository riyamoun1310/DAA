import duckdb
import pandas as pd

# Example: Run a DuckDB SQL query on a large dataset (CSV or Parquet)
def run_duckdb_query(query: str, file_path: str):
    try:
        con = duckdb.connect()
        # You can use read_csv_auto for CSV or parquet_scan for Parquet
        df = con.execute(f"SELECT * FROM read_csv_auto('{file_path}')").df()
        result = con.execute(query).fetchdf()
        return result.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()
