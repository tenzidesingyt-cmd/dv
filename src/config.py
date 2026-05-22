"""Конфигурация бота."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

# Основные переменные
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
PAYMENT_PROVIDER_TOKEN = os.environ.get("PAYMENT_PROVIDER_TOKEN", "")
PAYMENT_CURRENCY = os.environ.get("PAYMENT_CURRENCY", "KGS")

# Railway и боевые среды
RAILWAY_ENV = os.environ.get("RAILWAY_ENVIRONMENT", "development")
IS_PRODUCTION = RAILWAY_ENV == "production" or os.environ.get("ENVIRONMENT") == "production"

# Настройки для webhook (Railway)
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.environ.get("PORT", 8000))
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# База данных - используем /tmp на Railway для экономии памяти
DB_DIR = os.environ.get("DB_DIR") or str(ROOT_DIR)
DB_PATH = Path(DB_DIR) / "english_dv.db"

# Проверяем обязательные переменные
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не установлен!")
if ADMIN_ID == 0:
    raise RuntimeError("ADMIN_ID не установлен!")

# Если на Railway и нет WEBHOOK_URL, генерируем его
if IS_PRODUCTION:
    if not WEBHOOK_URL:
        # Предположим, что RAILWAY_PUBLIC_DOMAIN установлен автоматически Railway
        railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
        if railway_domain:
            WEBHOOK_URL = f"https://{railway_domain}{WEBHOOK_PATH}"
        # На Railway WEBHOOK_URL может быть установлен позже, это нормально

