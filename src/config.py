"""Конфигурация бота."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
PAYMENT_PROVIDER_TOKEN = os.environ.get("PAYMENT_PROVIDER_TOKEN", "")
PAYMENT_CURRENCY = os.environ.get("PAYMENT_CURRENCY", "KGS")
DB_PATH = ROOT_DIR / "english_dv.db"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не установлен!")
if ADMIN_ID == 0:
    raise RuntimeError("ADMIN_ID не установлен!")
