import pandas as pd
from .config import DB_PATH, CHUNK_SIZE
from .utils import log, connect_db

def main():
    log("Starting PREPROCESS step")
    conn = connect_db(DB_PATH)

    try:
        conn.execute("DROP TABLE IF EXISTS processed_accidents")
        conn.commit()

        query = "SELECT * FROM raw_accidents"
        chunks = pd.read_sql(query, conn, chunksize=CHUNK_SIZE)

        for i, chunk in enumerate(chunks, start=1):
            chunk = chunk.drop_duplicates(subset="ID")
            chunk = chunk.dropna(subset=["Start_Time", "Severity", "State"])

            chunk["Start_Time"] = pd.to_datetime(chunk["Start_Time"], errors="coerce")
            chunk["End_Time"] = pd.to_datetime(chunk["End_Time"], errors="coerce")

            chunk = chunk.dropna(subset=["Start_Time"])  # ensure valid start time

            chunk["Year"] = chunk["Start_Time"].dt.year
            chunk["Quarter"] = chunk["Start_Time"].dt.to_period("Q").astype(str)

            chunk["Duration_Minutes"] = (
                (chunk["End_Time"] - chunk["Start_Time"]).dt.total_seconds() / 60.0
            )

            chunk.to_sql("processed_accidents", conn, if_exists="append", index=False)
            log(f"Processed chunk {i} -> processed_accidents")

        conn.commit()
        log("PREPROCESS step complete")
    finally:
        conn.close()

if __name__ == "__main__":
    main()