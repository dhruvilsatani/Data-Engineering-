import os

DATA_DIR = os.getenv("DATA_DIR", "/app/data")
DB_PATH = os.path.join(DATA_DIR, "pipeline.db")

KAGGLE_DATASET = os.getenv("KAGGLE_DATASET", "sobhanmoosavi/us-accidents")
ZIP_NAME = os.getenv("ZIP_NAME", "us-accidents.zip")
CSV_NAME = os.getenv("CSV_NAME", "US_Accidents_March23.csv")

CSV_FILE = os.path.join(DATA_DIR, CSV_NAME)
ZIP_FILE = os.path.join(DATA_DIR, ZIP_NAME)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "200000"))

REQUIRED_COLUMNS = {
    "ID",
    "Start_Time",
    "End_Time",
    "State",
    "Severity",
    "Temperature(F)",
}