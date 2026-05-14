# 🚀 EnglishDV Bot - Готово к Railway!

## Что было исправлено и подготовлено

### 🐛 Исправленные баги:
1. **Логирование** - все `logging.error()` заменены на `logger.error()` для единообразия
2. **Конфигурация** - добавлена полная поддержка Railway переменных окружения
3. **Обработка ошибок** - улучшена обработка отсутствующих конфигов

### ✨ Добавлены для Railway:
- `Procfile` - запуск приложения
- `railway.json` - конфигурация Railway
- `runtime.txt` - версия Python 3.11
- `.env.example` - пример переменных
- `.gitignore` - исключение файлов
- `RAILWAY_DEPLOYMENT.md` - подробное руководство
- `CHECKLIST.md` - полный чек-лист
- `run_dev.sh` / `run_dev.bat` - скрипты для локального запуска

### 🔄 Обновлён `main.py`:
- Добавлена поддержка **webhooks** для production (Railway)
- Сохранён **polling** для development (локальная разработка)
- Автоматический выбор режима в зависимости от `ENVIRONMENT`
- Добавлен HTTP сервер через `aiohttp` для webhook приёма

### 📦 Обновлён `requirements.txt`:
- Добавлены комментарии для каждого пакета
- Все зависимости актуальны
- Поддерживает как polling, так и webhooks

## 📋 Быстрый старт на Railway

### Шаг 1: GitHub
```bash
git add .
git commit -m "Railway deployment ready"
git push
```

### Шаг 2: Railway Dashboard
1. Откройте https://railway.app/
2. New Project → Deploy from GitHub
3. Выберите ваш репозиторий

### Шаг 3: Переменные окружения
В Railway dashboard добавьте переменные:

**Обязательные:**
```
BOT_TOKEN=<ваш_токен>
ADMIN_ID=<ваш_id>
CLAUDE_API_KEY=<ваш_ключ>
ENVIRONMENT=production
```

**Опциональные:**
```
OPENAI_API_KEY=<key>
GROQ_API_KEY=<key>
PAYMENT_PROVIDER_TOKEN=<token>
```

### Шаг 4: Deploy
Нажмите Deploy - и всё!

Railway автоматически:
- Установит зависимости
- Запустит бота
- Создаст webhook URL
- Начнёт принимать обновления

## 🧪 Локальное тестирование

### Windows:
```bash
.\run_dev.bat
```

### Linux/macOS:
```bash
chmod +x run_dev.sh
./run_dev.sh
```

## 📖 Полная документация

- **README.md** - основная информация о проекте
- **RAILWAY_DEPLOYMENT.md** - подробное руководство Railway
- **CHECKLIST.md** - полный чек-лист всех изменений

## 🎯 Как это работает

### Development (локально):
```
Polling Mode (опросы каждые N секунд)
↓
ENVIRONMENT=development python main.py
↓
dp.start_polling(bot)
```

### Production (Railway):
```
Webhook Mode (Telegram отправляет обновления)
↓
ENVIRONMENT=production python main.py
↓
aiohttp веб-сервер слушает port 8000
↓
Telegram → webhook URL → bot.feed_update()
```

## ✅ Проверка статуса

Локально:
```bash
curl http://localhost:8000/health
# Ответ: OK
```

На Railway:
```bash
curl https://your-app.railway.app/health
# Ответ: OK
```

## 🔍 Логи и диагностика

### Railway логи:
```bash
railway logs --follow
```

### Проверка переменных:
```bash
railway variables
```

### Статус webhook:
В логах должно быть:
```
✅ Webhook установлен: https://xxx.railway.app/webhook
```

## 💡 Полезные команды

```bash
# Локальный запуск
ENVIRONMENT=development python main.py

# Проверка синтаксиса
python -m py_compile main.py src/config.py

# Установка зависимостей
pip install -r requirements.txt

# Обновление Railway
git push
```

## 📊 Структура проекта

```
.
├── main.py                    # Основной файл бота
├── requirements.txt           # Зависимости
├── Procfile                   # Конфигурация Railway
├── railway.json              # Дополнительная конфиг
├── runtime.txt               # Python версия
├── .env.example              # Пример переменных
├── .gitignore                # Исключения для git
├── README.md                 # Основная информация
├── RAILWAY_DEPLOYMENT.md     # Руководство Railway
├── CHECKLIST.md              # Чек-лист изменений
├── run_dev.sh                # Скрипт запуска (Linux/macOS)
├── run_dev.bat               # Скрипт запуска (Windows)
└── src/
    ├── __init__.py
    ├── config.py             # Конфигурация (улучшена для Railway)
    ├── database.py           # БД операции
    ├── lessons.py            # Уроки
    ├── keyboards.py          # Клавиатуры
    ├── ai.py                 # AI функции
    └── reading_texts.py      # Тексты
```

## 🚀 Готово!

Бот полностью готов к развёртыванию на Railway.com!

**Что дальше:**
1. ✅ Исправьте .env.example → .env (локально)
2. ✅ Протестируйте локально: `run_dev.bat` или `run_dev.sh`
3. ✅ Push в GitHub
4. ✅ Создайте новый проект на Railway
5. ✅ Добавьте переменные окружения
6. ✅ Нажмите Deploy
7. ✅ Проверьте логи
8. ✅ Добавьте бота в Telegram
9. ✅ Напишите `/start`
10. ✅ Наслаждайтесь! 🎉

---

**Вопросы? Смотрите:**
- RAILWAY_DEPLOYMENT.md (подробное руководство)
- CHECKLIST.md (все изменения)
- Railway docs (docs.railway.app)

**Last Updated:** 2026-05-14
