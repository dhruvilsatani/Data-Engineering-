import os
import subprocess
import pandas as pd

from .config import DATA_DIR, DB_PATH, KAGGLE_DATASET, ZIP_FILE, CSV_FILE, CHUNK_SIZE, REQUIRED_COLUMNS
from .utils import log, ensure_dir, connect_db, validate_schema

def kaggle_download():
    # Kaggle library reads env vars KAGGLE_USERNAME / KAGGLE_KEY
    log(f"Downloading Kaggle dataset: {KAGGLE_DATASET}")
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", KAGGLE_DATASET, "-p", DATA_DIR, "-f", os.path.basename(ZIP_FILE)],
        check=True
    )

def unzip_dataset():
    log("Unzipping dataset")
    subprocess.run(["unzip", "-o", ZIP_FILE, "-d", DATA_DIR], check=True)

def load_raw_to_sqlite():
    log("Loading raw CSV into SQLite: raw_accidents")
    conn = connect_db(DB_PATH)
    try:
        conn.execute("DROP TABLE IF EXISTS raw_accidents")
        conn.commit()

        chunks = pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE)
        for i, chunk in enumerate(chunks, start=1):
            validate_schema(chunk, REQUIRED_COLUMNS)
            chunk.to_sql("raw_accidents", conn, if_exists="append", index=False)
            log(f"Inserted chunk {i} into raw_accidents")
        conn.commit()
    finally:
        conn.close()

def main():
    ensure_dir(DATA_DIR)
    kaggle_download()
    unzip_dataset()
    load_raw_to_sqlite()
    log("INGEST step complete")

if __name__ == "__main__":
    main()