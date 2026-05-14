#!/bin/bash
# Local development startup script

# Проверяем Python версию
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "📌 Python version: $python_version"

# Активируем виртуальное окружение если нужно
if [ ! -d ".venv" ]; then
    echo "🔧 Создаём виртуальное окружение..."
    python -m venv .venv
fi

echo "✅ Активируем окружение..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source .venv/Scripts/activate
else
    # Linux/macOS
    source .venv/bin/activate
fi

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt --quiet

# Проверяем .env
if [ ! -f ".env" ]; then
    echo "⚠️  .env не найден, копируем из .env.example..."
    cp .env.example .env
    echo "✏️  Пожалуйста отредактируйте .env с вашими переменными!"
    exit 1
fi

# Проверяем BOT_TOKEN
if grep -q "BOT_TOKEN=your_bot_token_here" .env; then
    echo "❌ Ошибка: BOT_TOKEN не установлен в .env"
    exit 1
fi

# Запускаем бота в development режиме
echo "🤖 Запускаем EnglishDV в режиме разработки..."
echo "   Нажмите Ctrl+C для остановки"
ENVIRONMENT=development python main.py
