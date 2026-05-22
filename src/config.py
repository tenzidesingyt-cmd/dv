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
RAILWAY_ENV = os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("RAILWAY_ENVIRONMENT_NAME")
IS_RAILWAY = any(os.environ.get(name) for name in (
    "RAILWAY_ENVIRONMENT",
    "RAILWAY_ENVIRONMENT_NAME",
    "RAILWAY_PROJECT_ID",
    "RAILWAY_SERVICE_ID",
    "RAILWAY_PUBLIC_DOMAIN",
))
IS_PRODUCTION = (
    RAILWAY_ENV == "production"
    or os.environ.get("ENVIRONMENT") == "production"
    or IS_RAILWAY
)

# Настройки для webhook (Railway)
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.environ.get("PORT", 8000))
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# База данных. Если на Railway подключен Volume, используем его mount path.
DB_DIR = (
    os.environ.get("DB_DIR")
    or os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
    or str(ROOT_DIR)
)
Path(DB_DIR).mkdir(parents=True, exist_ok=True)
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

