import os
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# Tudo vem de variáveis de ambiente (Azure: Settings > Environment variables).
SERVER = os.environ["DB_SERVER"]
DATABASE = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DRIVER = os.environ.get("DB_DRIVER", "ODBC Driver 18 for SQL Server")

odbc_str = (
    f"DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};"
    f"UID={DB_USER};PWD={DB_PASSWORD};"
    "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"mssql+aioodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}",
)

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = "HS256"
ACCESS_TOKEN_MINUTES = 60 * 24 * 7