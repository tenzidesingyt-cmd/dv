@echo off
REM Local development startup script for Windows

echo.
echo 📌 Проверяем Python...
python --version
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.11+
    exit /b 1
)

REM Создаём виртуальное окружение если его нет
if not exist ".venv" (
    echo 🔧 Создаём виртуальное окружение...
    python -m venv .venv
)

echo ✅ Активируем окружение...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Ошибка активации окружения
    exit /b 1
)

echo 📦 Устанавливаем зависимости...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    exit /b 1
)

REM Проверяем .env файл
if not exist ".env" (
    echo ⚠️  .env не найден, копируем из .env.example...
    copy .env.example .env
    echo ✏️  Пожалуйста отредактируйте .env с вашими переменными!
    pause
    exit /b 1
)

REM Проверяем BOT_TOKEN
findstr /M "your_bot_token_here" .env >nul
if not errorlevel 1 (
    echo ❌ Ошибка: BOT_TOKEN не установлен в .env
    echo ✏️  Отредактируйте .env файл
    pause
    exit /b 1
)

REM Запускаем бота в development режиме
echo.
echo 🤖 Запускаем EnglishDV в режиме разработки...
echo.    Нажмите Ctrl+C для остановки
echo.
set ENVIRONMENT=development
python main.py

pause
