# Railway Deployment Guide (EnglishDV Bot)

## Быстрый старт (5 минут)

### 1. Подготовка репозитория

```bash
git add .
git commit -m "Ready for Railway deployment"
git push
```

### 2. На Railway.com

1. Перейдите на https://railway.app/
2. Нажмите "New Project" → "Deploy from GitHub repo"
3. Выберите ваш репозиторий
4. Railway автоматически обнаружит Python приложение

### 3. Установка переменных окружения

В Railway dashboard → Variables → добавьте:

```
BOT_TOKEN=<ваш_токен_от_BotFather>
ADMIN_ID=<ваш_telegram_id>
CLAUDE_API_KEY=<openrouter_key>
ENVIRONMENT=production
```

Опциональные (если используются):
```
OPENAI_API_KEY=<key>
GROQ_API_KEY=<key>
PAYMENT_PROVIDER_TOKEN=<token>
```

### 4. Нажмите Deploy

Railway автоматически:
- Установит зависимости из requirements.txt
- Запустит бота через Procfile
- Выдаст публичный домен
- Бот начнёт работать через webhooks

## Проверка статуса

1. В Railway dashboard посмотрите Logs
2. Должно быть: `🚀 EnglishDV запущен в PRODUCTION MODE (webhooks)`
3. Посетите `https://your-app.railway.app/health` - должно вернуть "OK"

## Если что-то не работает

### Ошибка: "Cannot decode webhook response"
- Убедитесь, что BOT_TOKEN правильный
- Посмотрите логи в Railway dashboard
- Подождите 30 секунд после развёртывания

### Ошибка: "RuntimeError: BOT_TOKEN не установлен"
- Проверьте, что BOT_TOKEN добавлен в Variables Railway

### Ошибка: "WEBHOOK_URL не установлен"
- Это нормально на Railway - домен установится автоматически
- Проверьте статус в Logs

### База данных не создаётся
- Railway предоставляет временное хранилище
- БД создаётся автоматически при первом запуске
- Данные сохраняются в `/tmp/english_dv.db`

## Масштабирование

Railway автоматически управляет масштабированием. Если нужно:
- Увеличить ресурсы: Settings → Resources → Allocated RAM
- Добавить реплики: Settings → Instances

## Переменные окружения, которые Railway устанавливает автоматически

```
PORT=8000                          # Порт приложения
RAILWAY_ENVIRONMENT=production     # Режим окружения
RAILWAY_PUBLIC_DOMAIN=xxx.railway.app  # Публичный домен
```

## Полезные команды

### Просмотр логов в реальном времени
```
railway logs --follow
```

### Переменные Railway CLI
```
railway variables
```

### Перезапуск приложения
В dashboard → Deployment → Redeploy

## Диагностика

Если бот не отвечает:
1. Проверьте логи: Railway Dashboard → Logs
2. Проверьте переменные: Railway Dashboard → Variables
3. Убедитесь, что webhook регистрирует обновления
4. Проверьте статус: `curl https://your-app.railway.app/health`

## Обновление бота

1. Сделайте изменения локально
2. `git push` в основной репозиторий
3. Railway автоматически перезапустит приложение
4. Проверьте логи

## Costs

Railway предоставляет:
- $5 в месяц бесплатно
- Минимальное использование бота обычно не превышает лимит
- Проверьте Usage в Dashboard

## Проблемы с производительностью?

1. Оптимизируйте AI запросы
2. Кэшируйте результаты где возможно
3. Используйте Groq для аудио (быстрее чем OpenAI)
4. Мониторьте логи для медленных операций

## Безопасность

- ❌ Никогда не коммитьте .env файл
- ✅ Используйте переменные окружения для всех секретов
- ✅ Регулярно ротируйте API ключи
- ✅ Логируйте подозрительную активность

## Поддержка

Railway поддержка: https://docs.railway.app/
Документация бота: см. README.md

---
Last updated: 2026-05-14
