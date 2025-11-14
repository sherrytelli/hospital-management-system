import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    "db_host": os.getenv("DB_HOST"),
    "db_name": os.getenv("DB_NAME"),
    "db_user": os.getenv("DB_USER"),
    "db_pass": os.getenv("DB_PASS"),
    "db_port": os.getenv("DB_PASS")
}