import duckdb
import pandas as pd

# Example: Run a DuckDB SQL query on a large dataset (CSV or Parquet)
def run_duckdb_query(query: str, file_path: str):
    try:
        con = duckdb.connect()
        df = con.execute(f"SELECT * FROM read_csv_auto('{file_path}')").df()
        result = con.execute(query).fetchdf()
        # Output as array or object based on query or question
        if "array" in query.lower():
            return result.to_dict(orient="records")
        else:
            return result.head().to_dict()
    except Exception as e:
        return {"error": f"DuckDB error: {str(e)}"}
    finally:
        con.close()
