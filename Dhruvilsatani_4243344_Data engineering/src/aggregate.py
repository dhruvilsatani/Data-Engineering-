import os
import pandas as pd
from .config import DB_PATH, CHUNK_SIZE, DATA_DIR
from .utils import log, connect_db, ensure_dir

def main():
    log("Starting AGGREGATE step")
    ensure_dir(DATA_DIR)
    conn = connect_db(DB_PATH)

    try:
        conn.execute("DROP TABLE IF EXISTS aggregated_accidents")
        conn.execute("DROP TABLE IF EXISTS aggregated_accidents_final")
        conn.commit()

        chunks = pd.read_sql("SELECT * FROM processed_accidents", conn, chunksize=CHUNK_SIZE)

        for i, chunk in enumerate(chunks, start=1):
            agg = (
                chunk.groupby(["Year", "Quarter", "State"])
                .agg(
                    total_accidents=("ID", "count"),
                    avg_severity=("Severity", "mean"),
                    avg_duration=("Duration_Minutes", "mean"),
                )
                .reset_index()
            )
            agg.to_sql("aggregated_accidents", conn, if_exists="append", index=False)
            log(f"Aggregated chunk {i} -> aggregated_accidents")

        final_agg = pd.read_sql(
            """
            SELECT Year, Quarter, State,
                   SUM(total_accidents) AS total_accidents,
                   AVG(avg_severity) AS avg_severity,
                   AVG(avg_duration) AS avg_duration
            FROM aggregated_accidents
            GROUP BY Year, Quarter, State
            """,
            conn
        )

        final_agg.to_sql("aggregated_accidents_final", conn, if_exists="replace", index=False)

        out_csv = os.path.join(DATA_DIR, "ml_ready_data.csv")
        final_agg.to_csv(out_csv, index=False)
        log(f"Exported final CSV: {out_csv}")

        log("AGGREGATE step complete")
    finally:
        conn.close()

if __name__ == "__main__":
    main()