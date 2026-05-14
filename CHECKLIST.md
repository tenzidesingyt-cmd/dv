# Checklist: Готовность бота к Railway

## ✅ Исправленные баги

- [x] **Логирование**: Все `logging.error()` заменены на `logger.error()` для консистентности
- [x] **Конфигурация Railway**: Добавлена поддержка переменных окружения Railway
- [x] **Webhooks**: Реализована поддержка webhook вместо polling на production
- [x] **Обработка ошибок**: Улучшена обработка отсутствующих переменных окружения
- [x] **Зависимости**: `requirements.txt` организован и содержит все необходимые пакеты

## 📋 Добавленные файлы для Railway

- [x] **Procfile** - конфигурация для Railway/Heroku
- [x] **railway.json** - дополнительная конфигурация для Railway
- [x] **runtime.txt** - указание версии Python 3.11
- [x] **.env.example** - пример переменных окружения
- [x] **.gitignore** - исключение чувствительных файлов
- [x] **RAILWAY_DEPLOYMENT.md** - полное руководство развёртывания
- [x] **run_dev.sh** - скрипт для локального запуска (Linux/macOS)
- [x] **run_dev.bat** - скрипт для локального запуска (Windows)

## 🚀 Режимы работы

### Development (Polling)
```bash
# Локально или на сервере с polling
ENVIRONMENT=development python main.py
```

**Особенности:**
- Бот запрашивает обновления от Telegram каждые N секунд
- Подходит для разработки и отладки
- Не требует публичного домена

### Production (Webhooks)
```bash
# На Railway.com
ENVIRONMENT=production python main.py
```

**Особенности:**
- Telegram отправляет обновления на webhook
- Более эффективно и быстро
- Требует публичного домена (Railway предоставляет)
- Автоматическое переключение на Railway

## 📝 Переменные окружения (необходимые)

```
BOT_TOKEN               # Токен бота от @BotFather
ADMIN_ID               # Ваш Telegram ID
CLAUDE_API_KEY         # OpenRouter API ключ
```

## 📚 Переменные окружения (опциональные)

```
OPENAI_API_KEY         # OpenAI Whisper (для аудио)
GROQ_API_KEY           # Groq Whisper (альтернатива)
PAYMENT_PROVIDER_TOKEN # Для платежей
ENVIRONMENT            # development или production
PORT                   # Порт (по умолчанию 8000)
WEBHOOK_HOST           # Хост webhook (для локальной разработки)
DB_DIR                 # Директория БД (по умолчанию корень проекта)
```

## ✨ Railway переменные (автоматические)

Установлены автоматически Railway:
```
RAILWAY_ENVIRONMENT    # production
RAILWAY_PUBLIC_DOMAIN  # xxx.railway.app
PORT                   # 8000
```

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

### Или вручную:
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt

# Создайте .env из .env.example и заполните данные

ENVIRONMENT=development python main.py
```

## 🌐 Развёртывание на Railway

1. Создайте аккаунт на railway.app
2. Подключите GitHub репозиторий
3. Добавьте переменные окружения в Railway dashboard
4. Railway автоматически развернёт бота
5. Проверьте логи: все должно быть в порядке!

## 🔍 Проверка статуса

### Локально:
```bash
curl http://localhost:8000/health
# Ответ: OK
```

### На Railway:
```bash
curl https://your-app.railway.app/health
# Ответ: OK
```

### Логи на Railway:
Railway dashboard → Logs → ищите сообщения о запуске

## 🐛 Типичные проблемы и решения

### "Cannot decode webhook response"
**Решение**: Проверьте BOT_TOKEN в переменных Railway

### "RuntimeError: BOT_TOKEN не установлен"
**Решение**: Добавьте BOT_TOKEN в Variables на Railway dashboard

### "WEBHOOK_URL не установлен"
**Решение**: Нормально для Railway, домен установится автоматически

### База данных не создаётся
**Решение**: Это нормально, создаётся при первом запуске в /tmp/english_dv.db

### Бот не отвечает на сообщения
**Решение**: 
1. Проверьте логи на Railway
2. Убедитесь в правильности BOT_TOKEN
3. Подождите 30-60 секунд после развёртывания

## 📊 Мониторинг

Railway предоставляет:
- **Logs**: логи в реальном времени
- **Metrics**: использование CPU, памяти, сети
- **Deployments**: история развёртываний
- **Analytics**: статистика использования

## 💚 Отладка

Для отладки на Railway:

1. Посмотрите логи:
   ```
   railway logs --follow
   ```

2. Проверьте переменные:
   ```
   railway variables
   ```

3. Перезапустите:
   ```
   railway logs --follow --after 5m
   # потом нажмите Redeploy в dashboard
   ```

## 🎯 Что дальше?

После успешного развёртывания:
1. Добавьте бота в Telegram (@YourBotName)
2. Напишите /start
3. Бот должен ответить приветствием
4. Проверьте все основные функции

## 📞 Помощь

Если что-то не работает:
1. Проверьте логи на Railway
2. Убедитесь, что все переменные установлены
3. Посмотрите RAILWAY_DEPLOYMENT.md
4. Проверьте документацию Railway: docs.railway.app

---

**Бот готов к развёртыванию! 🚀**

Last Updated: 2026-05-14
