"""EnglishDV Telegram Bot."""
import asyncio
import logging
import re
import datetime
import html
import base64

import httpx

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Импорт конфигурации
from src.config import BOT_TOKEN, ADMIN_ID, PAYMENT_PROVIDER_TOKEN, PAYMENT_CURRENCY
from src.database import (
    init_db, get_user, update_user, add_points, ensure_user_name,
    save_hw_result, update_streak, add_to_chat_history, get_chat_history,
    clear_chat_history, get_leaderboard, get_users_for_notification,
    get_words_for_review, update_word_review, add_word, get_vocabulary,
    get_unlearned_words, mark_word_learned, get_admin_stats,
    activate_premium, save_payment, user_has_premium
)
from src.lessons import LESSONS, INTRO_QUESTIONS, MIDTERM_TEST, WORD_BANK
from src.keyboards import (
    main_kb, lesson_kb, days_kb, get_admin_hw_kb, audio_lesson_kb,
    cancel_kb, after_audio_result_kb, test_start_kb, MAIN_MENU_BUTTONS,
    word_goal_kb, word_learning_kb, language_kb
)
from src.ai import (
    get_ai_response, parse_ai_score_feedback, parse_pronunciation_result,
    score_to_emoji, bonus_points_for_score, transcribe_audio
)
from src.reading_texts import READING_TEXTS, get_random_reading_text

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


PREMIUM_PLANS = {
    "month": {"title": "Премиум на 1 месяц", "ky_title": "1 айлык премиум", "days": 30, "price": 29900},
    "quarter": {"title": "Премиум на 3 месяца", "ky_title": "3 айлык премиум", "days": 90, "price": 74900},
    "year": {"title": "Премиум на 1 год", "ky_title": "1 жылдык премиум", "days": 365, "price": 249900},
}

KY_MENU_ALIASES = {
    "🏠 Башкы меню": "🏠 Главная",
    "👤 Жеке кабинет": "👤 Личный кабинет",
    "💬 Мугалим менен чат": "💬 Чат с учителем",
    "📚 Менин планым": "📚 Мой План",
    "📘 Күндүн сөздөрү": "📘 Слова дня",
    "📖 Менин сөздүгүм": "📖 Мой словарь",
    "📆 Жадыбал": "📆 Расписание",
    "⏰ Эскертмелер": "⏰ Уведомления",
    "🔄 Прогрессти тазалоо": "🔄 Сброс прогресса",
    "🌐 Тил": "🌐 Язык",
    "📖 Теманы түшүндүрүү": "📖 Объяснение темы",
    "✍️ Үй тапшырма": "✍️ Сдать ДЗ",
    "🚀 Кийинки тема": "🚀 Следующая тема",
    "🎙 Аудио-сабак": "🎙 Аудио-урок",
    "📝 Тест баштоо": "📝 Начать тест",
}

TEXTS = {
    "main_menu": {"ru": "Главное меню. Выбери действие:", "ky": "Башкы меню. Аракетти танда:"},
    "start_first": {
        "ru": "Привет! Добро пожаловать в EnglishDV! 🇬🇧\n\nДавай определим твой уровень. Ответь на вопросы (всего 12 вопросов, подбираются по сложности).\n\n💡 Подсказка: нажми /help чтобы узнать как пользоваться ботом!",
        "ky": "Салам! EnglishDV ботуна кош келиңиз! 🇬🇧\n\nАдегенде деңгээлиңди аныктайбыз. Суроолорго жооп бер (жалпы 12 суроо).\n\n💡 Жардам керек болсо /help бас.",
    },
    "unknown": {"ru": "Не понял команду. Используй меню или /start.", "ky": "Команданы түшүнгөн жокмун. Менюну же /start колдон."},
    "language_prompt": {"ru": "Выбери язык интерфейса:", "ky": "Интерфейстин тилин танда:"},
    "language_saved": {"ru": "✅ Язык сохранён: Русский", "ky": "✅ Тил сакталды: Кыргызча"},
    "premium_inactive": {"ru": "не активен", "ky": "активдүү эмес"},
}


def get_language(user: dict | None) -> str:
    return "ky" if user and user.get("language") == "ky" else "ru"


def t(key: str, language: str = "ru") -> str:
    return TEXTS.get(key, {}).get(language) or TEXTS.get(key, {}).get("ru", key)


async def user_language(user_id: int) -> str:
    return get_language(await get_user(user_id))


def format_premium_until(user: dict | None) -> str:
    language = get_language(user)
    if not user or not user.get("premium_until"):
        return t("premium_inactive", language)
    try:
        premium_until = datetime.datetime.fromisoformat(user["premium_until"])
    except ValueError:
        return t("premium_inactive", language)
    if premium_until <= datetime.datetime.now():
        return t("premium_inactive", language)
    return premium_until.strftime("%d.%m.%Y %H:%M")


def premium_plans_kb(language: str = "ru"):
    kb = InlineKeyboardBuilder()
    for code, plan in PREMIUM_PLANS.items():
        price_som = plan["price"] // 100
        title = plan["ky_title"] if language == "ky" else plan["title"]
        kb.row(types.InlineKeyboardButton(
            text=f"{title} — {price_som} сом",
            callback_data=f"premium:buy:{code}",
        ))
    return kb.as_markup()


def lesson_is_locked(lesson: dict | None, user: dict | None) -> bool:
    return bool(lesson and lesson.get("premium") and not user_has_premium(user))


# ══════════════════════════════════════════════
#  СОСТОЯНИЯ FSM
# ══════════════════════════════════════════════
class Form(StatesGroup):
    taking_test = State()
    waiting_for_hw = State()
    waiting_for_time = State()
    waiting_for_word = State()
    choosing_word_goal = State()
    learning_words = State()
    ai_chatting = State()
    waiting_for_audio_hw = State()


class TestStates(StatesGroup):
    answering = State()


# ══════════════════════════════════════════════
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ══════════════════════════════════════════════
async def reset_state_if_needed(state: FSMContext, text: str):
    current = await state.get_state()
    if current is not None and text in MAIN_MENU_BUTTONS:
        await state.clear()


async def process_hw_result(msg: types.Message, state: FSMContext, ai_raw: str, u: dict, lesson, hw_type: str = "text"):
    """Обрабатывает результат проверки ДЗ."""
    score, feedback = parse_ai_score_feedback(ai_raw)
    emoji = score_to_emoji(score)
    bonus = bonus_points_for_score(score)

    await save_hw_result(msg.from_user.id, u["lesson_num"], score, feedback, hw_type)

    if score >= 60:
        await update_user(msg.from_user.id, hw_status="approved")
        await add_points(msg.from_user.id, bonus)
        await msg.answer(
            f"{emoji} *Оценка: {score}/100*\n\n"
            f"{feedback}\n\n"
            f"✅ *ДЗ засчитано!* +{bonus} XP\n"
            f"Нажми '🚀 Следующая тема' чтобы продолжить.",
            parse_mode="Markdown",
            reply_markup=lesson_kb("approved"),
        )
    else:
        await update_user(msg.from_user.id, hw_status="not_sent")
        await add_points(msg.from_user.id, bonus)
        await msg.answer(
            f"{emoji} *Оценка: {score}/100*\n\n"
            f"{feedback}\n\n"
            f"📝 Нужно доработать. Попробуй ещё раз!\n"
            f"+{bonus} XP за попытку.",
            parse_mode="Markdown",
            reply_markup=lesson_kb("not_sent"),
        )

    try:
        type_icon = "📷" if hw_type == "photo" else "✍️"
        await bot.send_message(
            ADMIN_ID,
            f"📊 *ДЗ проверено ИИ* {type_icon}\n\n"
            f"👤 {msg.from_user.full_name} (@{msg.from_user.username or 'нет'})\n"
            f"📚 Урок №{u['lesson_num']}: {lesson['topic'] if lesson else '—'}\n"
            f"🎯 Оценка: *{score}/100*\n"
            f"{'✅ Засчитано' if score >= 60 else '❌ На доработку'}",
            parse_mode="Markdown",
            reply_markup=get_admin_hw_kb(msg.from_user.id, u["lesson_num"])
        )
    except Exception as e:
        logging.error(f"Не удалось уведомить админа: {e}")

    await state.clear()


async def _advance_lesson(msg, u):
    new_num = u["lesson_num"] + 1
    if new_num > len(LESSONS):
        return await msg.answer("🎉 Поздравляю! Весь курс пройден!", reply_markup=main_kb())
    lesson = LESSONS.get(new_num)
    if lesson_is_locked(lesson, u):
        return await msg.answer(
            "💎 Следующая тема входит в премиум.\n\n"
            "Открой премиум, чтобы продолжить курс с дополнительными уроками, "
            "практикой и проверкой заданий.",
            reply_markup=premium_plans_kb(),
        )
    await update_user(msg.from_user.id, lesson_num=new_num, hw_status="not_sent")
    await msg.answer(
        f"🎉 Переходим к новой теме!\n"
        f"📍 *Урок №{new_num}: {lesson['topic'] if lesson else '?'}*\n\n"
        f"Нажми '📚 Мой План' чтобы начать.",
        parse_mode="Markdown", reply_markup=main_kb()
    )


# ══════════════════════════════════════════════
#  ОБРАБОТЧИКИ КОМАНД
# ══════════════════════════════════════════════
@dp.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext):
    await state.clear()
    await update_streak(msg.from_user.id)
    await update_user(
        msg.from_user.id,
        username=msg.from_user.username or "",
        first_name=msg.from_user.first_name or "",
    )
    user = await get_user(msg.from_user.id)
    language = get_language(user)

    if not user or user["level"] == "Not Tested":
        await msg.answer(
            t("start_first", language)
        )
        await state.update_data(q_idx=0, score=0)
        await state.set_state(Form.taking_test)
        await send_intro_q(msg, 0)
    else:
        lesson = LESSONS.get(user["lesson_num"])
        lesson_info = f"\nТекущий урок: *{lesson['topic']}*" if lesson else "\nВсе уроки пройдены! 🎉"
        await msg.answer(
            f"С возвращением, {msg.from_user.first_name}! 👋\n"
            f"Твой уровень: {user['level']}{lesson_info}\n\n"
            f"🎙 Попробуй *аудио-урок* — читай вслух и получай оценку произношения!\n\n"
            f"Чтобы узнать управление, напиши /help",
            parse_mode="Markdown",
            reply_markup=main_kb(language)
        )


@dp.message(Command("help"))
async def cmd_help(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "📖 *Как пользоваться EnglishDV?*\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎯 *Основные функции:*\n\n"
        "*📚 Мой План* — начать урок дня\n"
        "• Смотри объяснение грамматики\n"
        "• Сдай домашнее задание (текст или фото)\n"
        "• ИИ проверит и даст оценку 0-100\n"
        "• Переходи к следующей теме\n\n"
        "*🎙 Аудио-урок* — практика произношения\n"
        "• Прочитай текст вслух\n"
        "• Отправь голосовое сообщение\n"
        "• ИИ анализирует произношение\n"
        "• Получишь рекомендации\n\n"
        "*💬 Чат с учителем* — свободная практика\n"
        "• Пиши на английском или русском\n"
        "• ИИ-учитель проверит ошибки\n"
        "• Помощь в любых вопросах\n\n"
        "*📘 Слова дня* — учи новые слова\n"
        "• Бот выдаёт слова автоматически\n"
        "• Введи любое число слов\n"
        "• Слова скрываются после изучения\n\n"
        "*👤 Личный кабинет* — твой прогресс\n"
        "• Уровень, баллы, достижения\n"
        "• Стрик (дни подряд занятий)\n"
        "• История оценок\n\n"
        "*🏆 Рейтинг* — соревнуйся с друзьями\n"
        "• Топ учеников по баллам\n"
        "• Покажи свои успехи!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 *Советы:*\n"
        "✅ Занимайся каждый день для стрика\n"
        "✅ Используй аудио-уроки для произношения\n"
        "✅ Практикуйся в чате с учителем\n"
        "✅ Начинай «📘 Слова дня» для новых слов\n\n"
        "Начни с '📚 Мой План'! 🚀",
        parse_mode="Markdown",
        reply_markup=main_kb()
    )


@dp.message(Command("language"))
@dp.message(F.text.in_({"🌐 Язык", "🌐 Тил"}))
async def choose_language(msg: types.Message, state: FSMContext):
    await state.clear()
    language = await user_language(msg.from_user.id)
    await msg.answer(t("language_prompt", language), reply_markup=language_kb())


@dp.callback_query(F.data.startswith("lang:"))
async def set_language(call: types.CallbackQuery, state: FSMContext):
    language = call.data.split(":")[-1]
    if language not in {"ru", "ky"}:
        return await call.answer("Language not found", show_alert=True)
    await update_user(call.from_user.id, language=language)
    await state.clear()
    await call.message.answer(t("language_saved", language), reply_markup=main_kb(language))
    await call.answer()


async def send_intro_q(msg, idx):
    q = INTRO_QUESTIONS[idx]
    kb = ReplyKeyboardBuilder()
    for opt in q["options"]:
        kb.add(types.KeyboardButton(text=opt))
    await msg.answer(f"Вопрос {idx + 1}: {q['q']}", reply_markup=kb.as_markup(resize_keyboard=True))


def format_words_list(words):
    return "\n".join([f"• *{w['word']}* — {w['translation']}" for w in words])


async def ensure_bot_vocab(user_id: int):
    rows = await get_vocabulary(user_id, limit=1)
    if rows:
        return
    for item in WORD_BANK:
        await add_word(user_id, item["word"], item["translation"])


async def start_word_learning(msg: types.Message, count: int, state: FSMContext):
    await ensure_bot_vocab(msg.from_user.id)
    await update_user(msg.from_user.id, daily_word_goal=count)
    rows = await get_unlearned_words(msg.from_user.id, limit=count)
    if not rows:
        return await msg.answer(
            "Все слова из базы уже выучены. Я могу показать их снова позже.",
            reply_markup=main_kb()
        )
    if len(rows) < count:
        await msg.answer(
            f"Сейчас доступно только {len(rows)} незавершённых слов. Я покажу их все.",
            reply_markup=word_learning_kb()
        )
    words_text = format_words_list(rows)
    await state.update_data(word_ids=[r["id"] for r in rows], words=[r["word"] for r in rows])
    await state.set_state(Form.learning_words)
    await msg.answer(
        f"📘 Сегодня ты изучаешь {len(rows)} слов:\n\n{words_text}\n\n"
        "🔊 Прочитай их вслух и отправь голосовое сообщение, или нажми '✅ Выучил'.\n"
        "Я помогу запомнить и скрою слова после изучения.",
        parse_mode="Markdown",
        reply_markup=word_learning_kb()
    )


@dp.message(F.text == "📘 Слова дня")
async def start_daily_words(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "Сколько слов хочешь выучить сегодня? Введи число или выбери быстрый вариант:",
        reply_markup=word_goal_kb()
    )
    await state.set_state(Form.choosing_word_goal)


@dp.message(Form.choosing_word_goal)
async def choose_word_goal(msg: types.Message, state: FSMContext):
    if msg.text in {"5 слов", "10 слов"}:
        count = 5 if msg.text == "5 слов" else 10
    elif msg.text.isdigit():
        count = int(msg.text)
        if count <= 0 or count > 50:
            return await msg.answer("Введи число от 1 до 50.", reply_markup=word_goal_kb())
    else:
        return await msg.answer("Введи число слов, например 5 или 10.", reply_markup=word_goal_kb())
    await start_word_learning(msg, count, state)


@dp.message(Form.learning_words, F.text == "✅ Выучил")
async def complete_word_learning(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    word_ids = data.get("word_ids", [])
    if not word_ids:
        await state.clear()
        return await msg.answer("Слова не найдены. Начни снова через '📘 Слова дня'.", reply_markup=main_kb())
    for word_id in word_ids:
        await mark_word_learned(word_id)
    await state.clear()
    await msg.answer(
        "✅ Отлично! Я отметил эти слова как выученные. Они больше не будут приходить в ежедневные занятия.",
        reply_markup=main_kb()
    )


@dp.message(Form.learning_words, F.text == "🔄 Повторить")
async def repeat_word_learning(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    word_ids = data.get("word_ids", [])
    if not word_ids:
        await state.clear()
        return await msg.answer("Слова не найдены. Начни снова через '📘 Слова дня'.", reply_markup=main_kb())
    rows = await get_unlearned_words(msg.from_user.id, limit=len(word_ids))
    if not rows:
        await state.clear()
        return await msg.answer("Слова закончились. Ты выучил все слова из базы. Зайди в '📘 Слова дня', чтобы повторить или начать снова.", reply_markup=main_kb())
    await msg.answer(
        f"🔁 Повторяем слова:\n\n{format_words_list(rows)}",
        parse_mode="Markdown",
        reply_markup=word_learning_kb()
    )


@dp.message(Form.learning_words, F.voice)
async def practice_words_audio(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    word_ids = data.get("word_ids", [])
    words = data.get("words", [])
    if not words:
        await state.clear()
        return await msg.answer("Слова не найдены. Начни снова через '📘 Слова дня'.", reply_markup=main_kb())

    processing_msg = await msg.answer("🎧 Получил голосовое. Анализирую произношение... Подожди пару секунд.")
    try:
        voice_file = await bot.get_file(msg.voice.file_id)
        async with httpx.AsyncClient() as client:
            audio_bytes = await client.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{voice_file.file_path}")
            audio_data = audio_bytes.content
    except Exception as e:
        logging.error(f"Ошибка загрузки аудио слов: {e}")
        await processing_msg.delete()
        return await msg.answer("❌ Не удалось загрузить аудио. Попробуй ещё раз.", reply_markup=word_learning_kb())

    transcribed = await transcribe_audio(audio_data, "words.ogg")
    await processing_msg.delete()
    if transcribed == "__TRANSCRIPTION_FAILED__" or not transcribed:
        return await msg.answer(
            "❌ Не удалось распознать речь. Попробуй ещё раз или нажми '✅ Выучил'.",
            reply_markup=word_learning_kb()
        )
    text = transcribed.lower()
    matched = []
    remaining_words = []
    remaining_ids = []
    for word_id, word in zip(word_ids, words):
        if re.search(rf"\b{re.escape(word.lower())}\b", text):
            matched.append(word)
        else:
            remaining_ids.append(word_id)
            remaining_words.append(word)
    if not matched:
        return await msg.answer(
            f"Я распознал: {transcribed}\n\nНе удалось найти ваши слова. Попробуй ещё раз или нажми '✅ Выучил'.",
            reply_markup=word_learning_kb()
        )
    for word_id in [wid for wid, word in zip(word_ids, words) if word in matched]:
        await mark_word_learned(word_id)
    if remaining_ids:
        await state.update_data(word_ids=remaining_ids, words=remaining_words)
        await msg.answer(
            f"✅ Отлично! Я распознал: {', '.join(matched)}. Эти слова отмечены как выученные.\n\n"
            f"Остальные слова пока не распознаны: {', '.join(remaining_words)}.\n"
            f"Отправь голосовое сообщение ещё раз для оставшихся слов или нажми '🔄 Повторить'.",
            reply_markup=word_learning_kb()
        )
    else:
        await state.clear()
        await msg.answer(
            f"✅ Отлично! Я распознал: {', '.join(matched)}. Эти слова отмечены как выученные.",
            reply_markup=main_kb()
        )


@dp.message(Form.learning_words, F.text)
async def learning_words_text(msg: types.Message, state: FSMContext):
    if msg.text in MAIN_MENU_BUTTONS:
        await state.clear()
        return await msg.answer("Главное меню:", reply_markup=main_kb())
    await msg.answer(
        "Отправь голосовое сообщение, чтобы я проверил произношение, или нажми '✅ Выучил'.",
        reply_markup=word_learning_kb()
    )


@dp.message(Form.taking_test)
async def handle_intro_test(msg: types.Message, state: FSMContext):
    if msg.text in MAIN_MENU_BUTTONS:
        await state.clear()
        return await msg.answer("Главное меню:", reply_markup=main_kb())
    data = await state.get_data()
    idx, score = data["q_idx"], data["score"]
    if msg.text == INTRO_QUESTIONS[idx]["a"]:
        score += 1
    if idx + 1 < len(INTRO_QUESTIONS):
        await state.update_data(q_idx=idx + 1, score=score)
        await send_intro_q(msg, idx + 1)
    else:
        # Улучшенная логика определения уровня
        total = len(INTRO_QUESTIONS)
        percent = (score / total) * 100
        
        if percent >= 75:
            lvl = "B1 (Выше среднего)"
        elif percent >= 50:
            lvl = "A2 (Базовый)"
        else:
            lvl = "A1 (Начинающий)"
        
        await update_user(msg.from_user.id, level=lvl, lesson_num=1, hw_status="not_sent")
        await msg.answer(
            f"✅ *Тест завершен!*\n\n"
            f"Правильных ответов: *{score}/{total}* ({percent:.0f}%)\n"
            f"Твой уровень: *{lvl}*\n\n"
            f"Начнём обучение! 🚀",
            parse_mode="Markdown",
            reply_markup=main_kb()
        )
        await state.clear()


# ══════════════════════════════════════════════
#  ГЛАВНОЕ МЕНЮ
# ══════════════════════════════════════════════
@dp.message(F.text == "🏠 Главная")
async def go_home(msg: types.Message, state: FSMContext):
    await state.clear()
    await ensure_user_name(msg.from_user.id, msg.from_user.username or "", msg.from_user.first_name or "")
    language = await user_language(msg.from_user.id)
    await msg.answer(t("main_menu", language), reply_markup=main_kb(language))


# ══════════════════════════════════════════════
#  ЛИЧНЫЙ КАБИНЕТ
# ══════════════════════════════════════════════
@dp.message(F.text == "👤 Личный кабинет")
async def show_profile(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    u = await get_user(msg.from_user.id)
    if not u:
        return await msg.answer("Сначала нажми /start")
    total_lessons = len(LESSONS)
    progress_percent = min(int((u["lesson_num"] / total_lessons) * 100), 100)
    streak_fire = "🔥" if u.get("streak", 0) > 0 else "❄️"
    premium_status = format_premium_until(u)
    language = get_language(u)
    await msg.answer(
        f"👤 *Твой профиль, {msg.from_user.first_name}*\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📊 *Статус:*\n"
        f"┣ Уровень: `{u['level']}`\n"
        f"┣ Прогресс: `{progress_percent}%` 📈\n"
        f"┗ Пройдено: `{u['lesson_num']}/{total_lessons}` уроков\n\n"
        f"🏆 *Достижения:*\n"
        f"┣ Стрик: {u.get('streak', 0)} дн. {streak_fire}\n"
        f"┣ Последняя оценка за ДЗ: `{u.get('last_score', 0)}/100` 🎯\n"
        f"┣ Произношение: `{u.get('audio_score', 0)}/100` 🎙\n"
        f"┣ Слов выучено: `{u.get('total_words', 0)}` 📝\n"
        f"┣ Премиум: `{premium_status}` 💎\n"
        f"┗ Баллы: `{u.get('points', 0)}` ⭐\n"
        f"━━━━━━━━━━━━━━━━━━",
        parse_mode="Markdown", reply_markup=main_kb(language)
    )


# ══════════════════════════════════════════════
#  МОЙ ПЛАН / УРОКИ
# ══════════════════════════════════════════════
@dp.message(F.text == "💎 Премиум")
async def show_premium(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    u = await get_user(msg.from_user.id)
    premium_status = format_premium_until(u)
    language = get_language(u)
    if language == "ky":
        text = (
            "💎 *EnglishDV Премиум*\n\n"
            f"Статус: `{premium_status}`\n\n"
            "Эмне кирет:\n"
            "• кошумча 26-30 сабактар\n"
            "• премиум темалардын тапшырмалары жана түшүндүрмөлөрү\n"
            "• кеңейтилген курс боюнча аудио-практика\n\n"
            "Төлөм Telegram Payments аркылуу сом менен жүргүзүлөт, Stars эмес."
        )
    else:
        text = (
            "💎 *Премиум EnglishDV*\n\n"
            f"Статус: `{premium_status}`\n\n"
            "Что входит:\n"
            "• дополнительные уроки 26-30\n"
            "• доступ к заданиям и объяснениям премиум-тем\n"
            "• аудио-практика по расширенному курсу\n\n"
            "Оплата идёт обычными деньгами в сомах через Telegram Payments, не звёздами."
        )
    await msg.answer(text, parse_mode="Markdown", reply_markup=premium_plans_kb(language))


@dp.message(Command("premium"))
async def cmd_premium(msg: types.Message, state: FSMContext):
    await show_premium(msg, state)


@dp.message(Command("paysupport"))
async def cmd_pay_support(msg: types.Message):
    await msg.answer(
        "Поддержка оплат EnglishDV:\n\n"
        "Если оплата прошла, но премиум не активировался, отправь администратору "
        "скрин оплаты и свой Telegram ID. Проверим платёж и выдадим доступ вручную."
    )


@dp.callback_query(F.data.startswith("premium:buy:"))
async def buy_premium(call: types.CallbackQuery):
    plan_code = call.data.split(":")[-1]
    plan = PREMIUM_PLANS.get(plan_code)
    language = await user_language(call.from_user.id)
    if not plan:
        return await call.answer("Тариф не найден", show_alert=True)
    if not PAYMENT_PROVIDER_TOKEN:
        return await call.message.answer(
            "Оплата пока не настроена.\n\n"
            "Добавь PAYMENT_PROVIDER_TOKEN в .env от платёжного провайдера Telegram Payments "
            "и перезапусти бота."
        )

    title = plan["ky_title"] if language == "ky" else plan["title"]
    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title=title,
        description="Премиум-доступ EnglishDV с оплатой в сомах.",
        payload=f"premium:{plan_code}:{call.from_user.id}",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency=PAYMENT_CURRENCY,
        prices=[types.LabeledPrice(label=title, amount=plan["price"])],
        start_parameter=f"premium-{plan_code}",
    )
    await call.answer()


@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    payload_parts = (pre_checkout_query.invoice_payload or "").split(":")
    if len(payload_parts) != 3 or payload_parts[0] != "premium" or payload_parts[1] not in PREMIUM_PLANS:
        return await pre_checkout_query.answer(ok=False, error_message="Некорректный тариф.")
    await pre_checkout_query.answer(ok=True)


@dp.message(F.successful_payment)
async def process_successful_payment(msg: types.Message):
    payment = msg.successful_payment
    payload_parts = (payment.invoice_payload or "").split(":")
    plan_code = payload_parts[1] if len(payload_parts) >= 2 else ""
    plan = PREMIUM_PLANS.get(plan_code)
    if not plan:
        return await msg.answer("Оплата прошла, но тариф не найден. Напиши администратору.")

    premium_until = await activate_premium(msg.from_user.id, plan["days"], source=f"payment:{plan_code}")
    await save_payment(
        user_id=msg.from_user.id,
        payload=payment.invoice_payload,
        plan_code=plan_code,
        amount=payment.total_amount,
        currency=payment.currency,
        telegram_payment_charge_id=payment.telegram_payment_charge_id,
        provider_payment_charge_id=payment.provider_payment_charge_id,
    )
    language = await user_language(msg.from_user.id)
    await msg.answer(
        f"✅ Премиум активирован до *{premium_until.strftime('%d.%m.%Y %H:%M')}*.\n\n"
        "Теперь доступны дополнительные уроки.",
        parse_mode="Markdown",
        reply_markup=main_kb(language),
    )


@dp.message(F.text == "📚 Мой План")
async def show_plan(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    u = await get_user(msg.from_user.id)
    if not u:
        return await msg.answer("Сначала нажми /start")
    language = get_language(u)
    lesson = LESSONS.get(u["lesson_num"])
    if not lesson:
        return await msg.answer("Ты прошёл все доступные темы! 🎉", reply_markup=main_kb(language))
    if lesson_is_locked(lesson, u):
        return await msg.answer(
            "💎 Этот урок доступен в премиуме.\n\n"
            "Оформи подписку, чтобы открыть дополнительные темы курса.",
            reply_markup=premium_plans_kb(language),
        )

    status_text = {
        "not_sent": "📤 Нужно сдать ДЗ",
        "pending":  "⏳ ДЗ на проверке",
        "approved": "✅ ДЗ принято — можно идти дальше!",
    }.get(u["hw_status"], "📤 Нужно сдать ДЗ")

    await msg.answer(
        f"📍 *Урок №{u['lesson_num']}: {lesson['topic']}*\n\n"
        f"Статус: {status_text}\n\n"
        f"💡 *Совет:* Пройди 🎙 Аудио-урок для тренировки произношения!",
        parse_mode="Markdown",
        reply_markup=lesson_kb(u["hw_status"])
    )


@dp.message(F.text == "📖 Объяснение темы")
async def show_theory(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    u = await get_user(msg.from_user.id)
    if not u:
        return await msg.answer("Сначала нажми /start")
    language = get_language(u)
    lesson = LESSONS.get(u["lesson_num"])
    if not lesson:
        return await msg.answer("Все темы пройдены! 🎉", reply_markup=main_kb(language))
    if lesson_is_locked(lesson, u):
        return await msg.answer(
            "💎 Объяснение этой темы входит в премиум.",
            reply_markup=premium_plans_kb(language),
        )
    await msg.answer(
        f"📖 *Урок №{u['lesson_num']}: {lesson['topic']}*\n\n"
        f"{lesson['explanation']}\n\n"
        f"🎬 Видео: {lesson['video']}\n\n"
        f"🎙 После изучения попробуй *Аудио-урок* для практики произношения!",
        reply_markup=lesson_kb(u["hw_status"], language)
    )


# ══════════════════════════════════════════════
#  🎙 АУДИО-УРОК
# ══════════════════════════════════════════════
@dp.message(F.text == "🎙 Аудио-урок")
async def start_audio_lesson(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    u = await get_user(msg.from_user.id)
    if not u:
        return await msg.answer("Сначала нажми /start")
    language = get_language(u)

    lesson_num = u.get("lesson_num", 1)
    lesson = LESSONS.get(lesson_num)
    if lesson_is_locked(lesson, u):
        return await msg.answer(
            "💎 Аудио-практика этой темы доступна в премиуме.",
            reply_markup=premium_plans_kb(language),
        )
    reading = get_random_reading_text(lesson_num)

    await state.update_data(
        reading_text=reading["text"],
        reading_focus=reading["focus"],
        reading_tip=reading["tip"],
        lesson_num=lesson_num,
    )
    await state.set_state(Form.waiting_for_audio_hw)

    await msg.answer(
        f"🎙 *Аудио-урок — Урок №{lesson_num}*\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"📖 *Прочитай этот текст вслух:*\n\n"
        f"_{reading['text']}_\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 *Фокус:* {reading['focus']}\n"
        f"💡 *Подсказка:* {reading['tip']}\n\n"
        f"🎤 *Запиши голосовое сообщение и отправь его!*\n"
        f"ИИ проверит произношение и покажет ошибки.",
        parse_mode="Markdown",
        reply_markup=audio_lesson_kb()
    )


@dp.message(F.text == "🔄 Другой текст")
async def another_reading_text(msg: types.Message, state: FSMContext):
    current = await state.get_state()
    if current == Form.waiting_for_audio_hw.state:
        await start_audio_lesson(msg, state)
    else:
        await start_audio_lesson(msg, state)


@dp.message(Form.waiting_for_audio_hw, F.voice)
async def process_audio_hw(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    reading_text = data.get("reading_text", "")
    reading_focus = data.get("reading_focus", "")
    reading_tip = data.get("reading_tip", "")
    lesson_num = data.get("lesson_num", 1)

    u = await get_user(msg.from_user.id)

    processing_msg = await msg.answer(
        "🎧 Получил голосовое!\n"
        "⏳ Распознаю речь...\n"
        "🔍 Анализирую произношение...\n\n"
        "Подожди 15-30 секунд."
    )

    try:
        voice_file = await bot.get_file(msg.voice.file_id)
        async with httpx.AsyncClient() as client:
            from src.config import BOT_TOKEN
            voice_response = await client.get(
                f"https://api.telegram.org/file/bot{BOT_TOKEN}/{voice_file.file_path}"
            )
            audio_bytes = voice_response.content
    except Exception as e:
        logging.error(f"Ошибка скачивания аудио: {e}")
        await processing_msg.delete()
        return await msg.answer(
            "❌ Не удалось загрузить аудио. Попробуй ещё раз.",
            reply_markup=audio_lesson_kb()
        )

    transcribed = await transcribe_audio(audio_bytes, "voice.ogg")

    if transcribed == "__TRANSCRIPTION_FAILED__" or not transcribed:
        await processing_msg.delete()
        return await msg.answer(
            "❌ Не удалось распознать речь.\n\n"
            "Попробуй:\n"
            "• Говорить чётче и медленнее\n"
            "• Записать в тихом месте\n"
            "• Отправить ещё раз\n\n"
            "Или добавь OPENAI_API_KEY в переменные окружения для лучшего распознавания.",
            reply_markup=audio_lesson_kb()
        )

    from src.ai import AI_SYSTEM_PROMPT_PRONUNCIATION
    pronunciation_prompt = AI_SYSTEM_PROMPT_PRONUNCIATION.format(
        original_text=reading_text,
        transcribed_text=transcribed,
        focus=reading_focus,
    )

    ai_raw = await get_ai_response(
        msg.from_user.id,
        f"Оригинал: {reading_text}\nРаспознано: {transcribed}",
        u.get("level", "A1") if u else "A1",
        system_override=pronunciation_prompt,
    )

    try:
        await processing_msg.delete()
    except Exception:
        pass

    score, errors, feedback, tips = parse_pronunciation_result(ai_raw)
    emoji = score_to_emoji(score)
    bonus = bonus_points_for_score(score)

    await save_hw_result(msg.from_user.id, lesson_num, score, feedback, hw_type="audio")
    await add_points(msg.from_user.id, bonus)

    escaped_errors = html.escape(errors) if errors else ""
    escaped_feedback = html.escape(feedback) if feedback else ""
    escaped_tips = html.escape(tips) if tips else ""

    result_parts = [
        f"{emoji} <b>Оценка произношения: {score}/100</b>"
    ]

    if errors and errors.strip() and errors.strip() != "—":
        result_parts.append(f"🔤 <b>Ошибки произношения:</b>\n{escaped_errors}")
    else:
        result_parts.append("✅ <b>Ошибок произношения не обнаружено!</b>")

    if feedback:
        result_parts.append(f"💬 <b>Фидбек:</b>\n{escaped_feedback}")

    if tips:
        result_parts.append(f"🎯 <b>Советы:</b>\n{escaped_tips}")

    result_parts.append(f"+{bonus} XP за практику! 🎙")

    result_text = "\n\n".join(result_parts)

    if len(result_text) > 4000:
        result_text = result_text[:4000] + "..."

    await msg.answer(
        result_text,
        parse_mode="HTML",
        reply_markup=after_audio_result_kb()
    )

    await state.clear()


@dp.message(Form.waiting_for_audio_hw, F.audio)
async def process_audio_file(msg: types.Message, state: FSMContext):
    msg.voice = types.Voice(
        file_id=msg.audio.file_id,
        file_unique_id=msg.audio.file_unique_id,
        duration=msg.audio.duration or 0,
    )
    await process_audio_hw(msg, state)


@dp.message(Form.waiting_for_audio_hw, F.text)
async def audio_lesson_text_handler(msg: types.Message, state: FSMContext):
    if msg.text == "📖 Объяснение темы":
        await state.clear()
        return await show_theory(msg, state)

    if msg.text in MAIN_MENU_BUTTONS or msg.text == "🔄 Другой текст":
        if msg.text == "🔄 Другой текст":
            return await start_audio_lesson(msg, state)
        await state.clear()
        if msg.text == "🏠 Главная":
            return await msg.answer("Главное меню:", reply_markup=main_kb())
        return await msg.answer("Главное меню:", reply_markup=main_kb())
    await msg.answer(
        "🎤 Жду голосовое сообщение!\n\n"
        "Нажми на микрофон в Telegram и запиши как ты читаешь текст.",
        reply_markup=audio_lesson_kb()
    )


# ══════════════════════════════════════════════
#  ДОМАШНЕЕ ЗАДАНИЕ
# ══════════════════════════════════════════════
@dp.message(F.text == "✍️ Сдать ДЗ")
async def start_hw(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    u = await get_user(msg.from_user.id)
    if not u:
        return await msg.answer("Сначала нажми /start")
    language = get_language(u)
    lesson = LESSONS.get(u["lesson_num"])
    if not lesson:
        return await msg.answer("Все темы пройдены!")
    if lesson_is_locked(lesson, u):
        return await msg.answer(
            "💎 Домашнее задание этой темы доступно в премиуме.",
            reply_markup=premium_plans_kb(language),
        )

    await msg.answer(
        f"📝 *Урок №{u['lesson_num']}: {lesson['topic']}*\n\n"
        f"{lesson['tasks']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"📤 *Отправь ответ:*\n"
        f"• ✍️ Текстом — просто напиши\n"
        f"• 📷 Фото — сфотографируй рукописный текст\n\n"
        f"ИИ проверит и поставит оценку 0-100 🎯",
        parse_mode="Markdown",
        reply_markup=cancel_kb(),
    )
    await state.set_state(Form.waiting_for_hw)


@dp.message(Form.waiting_for_hw, F.text)
async def process_hw_text(msg: types.Message, state: FSMContext):
    if msg.text in MAIN_MENU_BUTTONS:
        await state.clear()
        return await msg.answer("Главное меню:", reply_markup=main_kb())

    u = await get_user(msg.from_user.id)
    if not u:
        await state.clear()
        return await msg.answer("Сначала нажми /start")

    lesson = LESSONS.get(u["lesson_num"])

    if len(msg.text.strip()) < 20:
        return await msg.answer("❌ Ответ слишком короткий! Напиши хотя бы несколько предложений.")

    checking_msg = await msg.answer("🔍 ИИ проверяет ДЗ...\n⏳ Подожди 10-20 секунд.")

    ai_raw = await get_ai_response(
        msg.from_user.id,
        msg.text,
        u.get("level", "A1"),
        is_homework=True,
        lesson_topic=lesson["topic"] if lesson else ""
    )

    try:
        await checking_msg.delete()
    except Exception:
        pass

    await process_hw_result(msg, state, ai_raw, u, lesson, hw_type="text")


@dp.message(Form.waiting_for_hw, F.photo)
async def process_hw_photo(msg: types.Message, state: FSMContext):
    u = await get_user(msg.from_user.id)
    if not u:
        await state.clear()
        return await msg.answer("Сначала нажми /start")

    lesson = LESSONS.get(u["lesson_num"])

    checking_msg = await msg.answer(
        "📷 Получил фото!\n"
        "🔍 ИИ читает и проверяет текст...\n"
        "⏳ Подожди 15-30 секунд."
    )

    try:
        photo = msg.photo[-1]
        file = await bot.get_file(photo.file_id)
        from src.config import BOT_TOKEN
        async with httpx.AsyncClient() as client:
            photo_response = await client.get(
                f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
            )
            photo_bytes = photo_response.content
        photo_base64 = base64.b64encode(photo_bytes).decode("utf-8")
    except Exception as e:
        logging.error(f"Ошибка фото: {e}")
        await checking_msg.delete()
        return await msg.answer("❌ Не удалось загрузить фото. Попробуй ещё раз или отправь текстом.")

    ai_raw = await get_ai_response(
        msg.from_user.id,
        "",
        u.get("level", "A1"),
        is_homework=True,
        photo_base64=photo_base64,
        lesson_topic=lesson["topic"] if lesson else ""
    )

    try:
        await checking_msg.delete()
    except Exception:
        pass

    await process_hw_result(msg, state, ai_raw, u, lesson, hw_type="photo")


# ══════════════════════════════════════════════
#  РЕШЕНИЕ АДМИНА
# ══════════════════════════════════════════════
@dp.callback_query(F.data.startswith("hw:"))
async def handle_admin_decision(call: types.CallbackQuery):
    parts = call.data.split(":")
    if len(parts) != 4:
        return await call.answer("Некорректные данные", show_alert=True)
    decision = parts[1]
    try:
        student_id = int(parts[2])
        lesson_num = int(parts[3])
    except (ValueError, IndexError):
        return await call.answer("Ошибка парсинга", show_alert=True)

    if decision == "approve":
        await update_user(student_id, hw_status="approved")
        await add_points(student_id, 10)
        try:
            await bot.send_message(
                student_id,
                f"✅ *Куратор одобрил ДЗ №{lesson_num}!*\nМожешь переходить дальше. 🚀",
                parse_mode="Markdown", reply_markup=lesson_kb("approved")
            )
        except Exception:
            pass
        await call.message.edit_text(call.message.text + "\n\n✅ ПРИНЯТО КУРАТОРОМ")
    elif decision == "reject":
        await update_user(student_id, hw_status="not_sent")
        try:
            await bot.send_message(
                student_id,
                f"❌ *Куратор вернул ДЗ №{lesson_num} на доработку.*\nПопробуй ещё раз.",
                parse_mode="Markdown", reply_markup=lesson_kb("not_sent")
            )
        except Exception:
            pass
        await call.message.edit_text(call.message.text + "\n\n❌ ОТКЛОНЕНО КУРАТОРОМ")
    await call.answer()


# ══════════════════════════════════════════════
#  СЛЕДУЮЩАЯ ТЕМА + ПРОМЕЖУТОЧНЫЙ ТЕСТ
# ══════════════════════════════════════════════
@dp.message(F.text == "🚀 Следующая тема")
async def check_for_test(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    u = await get_user(msg.from_user.id)
    if not u:
        return await msg.answer("Сначала нажми /start")
    if u["hw_status"] != "approved":
        return await msg.answer(
            "❌ Сначала сдай ДЗ!\n\nНажми '✍️ Сдать ДЗ' и отправь выполненное задание.",
        reply_markup=lesson_kb(u["hw_status"], language)
    )
    if u["lesson_num"] == 5:
        await msg.answer(
            "🛑 *STOP! Проверка знаний.*\n\n"
            "Ты прошёл первые 5 тем.\nМинимальный балл: *4 из 5*.",
            parse_mode="Markdown",
            reply_markup=test_start_kb(),
        )
    else:
        await _advance_lesson(msg, u)


@dp.message(F.text == "📝 Начать тест")
async def start_midterm(msg: types.Message, state: FSMContext):
    await state.update_data(test_idx=0, test_score=0)
    await state.set_state(TestStates.answering)
    await send_test_step(msg, 0)


async def send_test_step(msg, idx):
    q = MIDTERM_TEST[idx]
    if q.get("type") == "open":
        reply_markup = cancel_kb()
    else:
        kb = ReplyKeyboardBuilder()
        for opt in q["options"]:
            kb.add(types.KeyboardButton(text=opt))
        reply_markup = kb.as_markup(resize_keyboard=True)
    await msg.answer(
        f"❓ Вопрос {idx+1}/{len(MIDTERM_TEST)}:\n\n{q['q']}",
        reply_markup=reply_markup
    )


def is_open_answer_correct(text: str, question: dict) -> bool:
    answer = text.strip().lower()
    if len(answer) < 3:
        return False
    keywords = question.get("keywords", [])
    if not keywords:
        return True
    return any(k in answer for k in keywords)


@dp.message(TestStates.answering)
async def process_test_answer(msg: types.Message, state: FSMContext):
    if msg.text in MAIN_MENU_BUTTONS:
        await state.clear()
        return await msg.answer("Тест прерван.", reply_markup=main_kb())
    data = await state.get_data()
    idx, score = data["test_idx"], data["test_score"]
    q = MIDTERM_TEST[idx]
    if q.get("type") == "open":
        if not msg.text or len(msg.text.strip()) < 3:
            return await msg.answer(
                "Напиши чуть больше текста, чтобы я мог засчитать ответ.",
                reply_markup=cancel_kb()
            )
        if is_open_answer_correct(msg.text, q):
            score += 1
    else:
        if msg.text == q["a"]:
            score += 1
    if idx + 1 < len(MIDTERM_TEST):
        await state.update_data(test_idx=idx + 1, test_score=score)
        await send_test_step(msg, idx + 1)
    else:
        await state.clear()
        if score >= 4:
            await update_user(msg.from_user.id, lesson_num=6, hw_status="not_sent")
            await add_points(msg.from_user.id, 50)
            await msg.answer(
                f"🎉 *Тест пройден!* {score}/{len(MIDTERM_TEST)}\nОткрыт Урок №6! +50 XP",
                parse_mode="Markdown", reply_markup=main_kb())
        else:
            await msg.answer(
                f"😟 *Тест не пройден.* {score}/{len(MIDTERM_TEST)}\nПовтори темы 1-5.",
                parse_mode="Markdown", reply_markup=main_kb())


# ══════════════════════════════════════════════
#  СЛОВАРЬ
# ══════════════════════════════════════════════
@dp.message(F.text == "📖 Мой словарь")
async def show_vocabulary(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    rows = await get_vocabulary(msg.from_user.id, learned_only=True)
    if not rows:
        return await msg.answer("Новых слов для изучения пока нет. Зайди в '📘 Слова дня', чтобы получить новые слова.", reply_markup=main_kb())
    vocab_list = "\n".join([f"• *{r['word']}* — {r['translation']}" for r in rows])
    await msg.answer(
        f"📚 *Текущий словарь для изучения:*\n\n{vocab_list}",
        parse_mode="Markdown", reply_markup=main_kb()
    )


# ══════════════════════════════════════════════
#  РАСПИСАНИЕ И УВЕДОМЛЕНИЯ
# ══════════════════════════════════════════════
@dp.message(F.text == "📆 Расписание")
async def show_schedule(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    u = await get_user(msg.from_user.id)
    days_text = (u.get("notify_days") or "Не выбраны") if u else "Не выбраны"
    time_text = (u.get("notify_time") or "Не установлено") if u else "Не установлено"
    await msg.answer(
        f"📅 *Твоё расписание:*\n\nДни: *{days_text}*\nВремя: *{time_text}*\n\nИзменить — '⏰ Уведомления'.",
        parse_mode="Markdown", reply_markup=main_kb(),
    )


@dp.message(F.text == "⏰ Уведомления")
async def start_notify_setup(msg: types.Message, state: FSMContext):
    await state.clear()
    u = await get_user(msg.from_user.id)
    current_days = (u.get("notify_days") or "") if u else ""
    await state.update_data(days=current_days)
    await msg.answer("Выбери дни для уведомлений:", reply_markup=days_kb(current_days))


@dp.callback_query(F.data.startswith("day_"))
async def toggle_day(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = set(x for x in (data.get("days") or "").split(",") if x)
    day = call.data.split("_")[1]
    selected.discard(day) if day in selected else selected.add(day)
    new_str = ",".join(sorted(filter(None, selected)))
    await state.update_data(days=new_str)
    await call.message.edit_reply_markup(reply_markup=days_kb(new_str))
    await call.answer()


@dp.callback_query(F.data == "days_done")
async def finish_days_setup(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    days = data.get("days", "")
    if not days:
        return await call.answer("Выбери хотя бы один день!", show_alert=True)
    await update_user(call.from_user.id, notify_days=days)
    await call.message.edit_text(
        f"✅ Дни: *{days}*\n\nВведи время ЧЧ:ММ (например: 19:30):",
        parse_mode="Markdown"
    )
    await state.set_state(Form.waiting_for_time)
    await call.answer()


@dp.message(Form.waiting_for_time, F.text)
async def process_time(msg: types.Message, state: FSMContext):
    if msg.text in MAIN_MENU_BUTTONS:
        await state.clear()
        return await msg.answer("Главное меню:", reply_markup=main_kb())
    if not re.match(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", msg.text.strip()):
        return await msg.answer("❌ Формат: ЧЧ:ММ (например: 18:00)")
    await update_user(msg.from_user.id, notify_time=msg.text.strip())
    await msg.answer(f"✅ Напоминания в *{msg.text.strip()}*.", parse_mode="Markdown", reply_markup=main_kb())
    await state.clear()


# ══════════════════════════════════════════════
#  РЕЙТИНГ
# ══════════════════════════════════════════════
@dp.message(F.text == "🏆 Рейтинг")
async def show_leaderboard(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    await ensure_user_name(msg.from_user.id, msg.from_user.username or "", msg.from_user.first_name or "")
    rows = await get_leaderboard()
    if not rows:
        return await msg.answer("Рейтинг пока пуст.")
    lines = []
    medals = ["🥇", "🥈", "🥉"]
    for i, r in enumerate(rows):
        medal = medals[i] if i < 3 else f"{i+1}."
        fn = (r["first_name"] or "").strip()
        un = (r["username"] or "").strip()
        if fn and un:
            name = f"{fn} (@{un})"
        elif fn:
            name = fn
        elif un:
            name = f"@{un}"
        else:
            name = f"Пользователь {r['user_id']}"
        audio_str = f" 🎙{r['audio_score']}" if r["audio_score"] else ""
        lines.append(f"{medal} {name} — {r['points']} XP{audio_str}")
    await msg.answer(
        "🏆 <b>Топ учеников:</b>\n\n" + "\n".join(lines),
        parse_mode="HTML", reply_markup=main_kb()
    )


# ══════════════════════════════════════════════
#  ЧАТ С УЧИТЕЛЕМ
# ══════════════════════════════════════════════
@dp.message(F.text == "💬 Чат с учителем")
async def start_ai_chat(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "🌟 *Режим практики с AI-учителем!*\n\n"
        "• Английский → проверю ошибки\n"
        "• Русский → пообщаемся\n\n"
        "Выход: '🏠 Главная'",
        parse_mode="Markdown",
        reply_markup=cancel_kb(),
    )
    await state.set_state(Form.ai_chatting)


@dp.message(Form.ai_chatting, F.text)
async def ai_chat_process(msg: types.Message, state: FSMContext):
    if msg.text in MAIN_MENU_BUTTONS:
        await clear_chat_history(msg.from_user.id)
        await state.clear()
        return await msg.answer("Главное меню:", reply_markup=main_kb())
    u = await get_user(msg.from_user.id)
    level = u.get("level", "A1") if u else "A1"
    await bot.send_chat_action(msg.chat.id, "typing")
    reply = await get_ai_response(msg.from_user.id, msg.text, level, is_homework=False)
    await msg.answer(reply)


# ══════════════════════════════════════════════
#  СБРОС ПРОГРЕССА
# ══════════════════════════════════════════════
@dp.message(F.text == "🔄 Сброс прогресса")
async def reset_progress(msg: types.Message, state: FSMContext):
    await reset_state_if_needed(state, msg.text)
    await update_user(msg.from_user.id, lesson_num=1, hw_status="not_sent")
    await msg.answer("🔄 Прогресс сброшен до урока 1.", reply_markup=main_kb())


# ══════════════════════════════════════════════
#  АДМИН-ПАНЕЛЬ
# ══════════════════════════════════════════════
@dp.message(Command("admin"))
async def admin_panel(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    stats = await get_admin_stats()
    await msg.answer(
        f"⚙️ *Панель администратора*\n\n"
        f"👥 Учеников: {stats['total_users']}\n"
        f"📝 Слов выучено: {stats['total_words']}\n"
        f"🔔 ДЗ на проверке: {stats['pending_hw']}\n"
        f"🎯 Средняя оценка ДЗ: {stats['avg_score']:.1f}/100\n"
        f"🎙 Аудио-уроков пройдено: {stats['audio_count']}\n"
        f"🎙 Средняя оценка произношения: {stats['avg_audio']:.1f}/100",
        parse_mode="Markdown"
    )


@dp.message(Command("give_premium"))
async def admin_give_premium(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = (msg.text or "").split()
    try:
        if len(parts) == 1:
            target_id = msg.from_user.id
            days = 30
        elif len(parts) == 2:
            target_id = int(parts[1])
            days = 30
        else:
            target_id = int(parts[1])
            days = int(parts[2])
    except ValueError:
        return await msg.answer("Формат: /give_premium [telegram_id] [days]\nНапример: /give_premium 8217301497 30")

    if days <= 0 or days > 3650:
        return await msg.answer("Количество дней должно быть от 1 до 3650.")

    premium_until = await activate_premium(target_id, days, source="admin")
    await msg.answer(
        f"✅ Премиум выдан пользователю `{target_id}` до *{premium_until.strftime('%d.%m.%Y %H:%M')}*.",
        parse_mode="Markdown",
    )
    if target_id != msg.from_user.id:
        try:
            await bot.send_message(
                target_id,
                f"💎 Администратор активировал тебе премиум до *{premium_until.strftime('%d.%m.%Y %H:%M')}*.",
                parse_mode="Markdown",
                reply_markup=main_kb(),
            )
        except Exception:
            pass


@dp.message(F.text.in_(set(KY_MENU_ALIASES.keys())))
async def ky_menu_router(msg: types.Message, state: FSMContext):
    """Маршрутизирует кыргызские кнопки на существующие обработчики."""
    action = KY_MENU_ALIASES.get(msg.text)
    if action == "🏠 Главная":
        await state.clear()
        return await msg.answer(t("main_menu", "ky"), reply_markup=main_kb("ky"))
    if action == "👤 Личный кабинет":
        return await show_profile(msg, state)
    if action == "💬 Чат с учителем":
        return await start_ai_chat(msg, state)
    if action == "🏆 Рейтинг":
        return await show_leaderboard(msg, state)
    if action == "📚 Мой План":
        return await show_plan(msg, state)
    if action == "📘 Слова дня":
        return await start_daily_words(msg, state)
    if action == "📖 Мой словарь":
        return await show_vocabulary(msg, state)
    if action == "📆 Расписание":
        return await show_schedule(msg, state)
    if action == "⏰ Уведомления":
        return await start_notify_setup(msg, state)
    if action == "🔄 Сброс прогресса":
        return await reset_progress(msg, state)
    if action == "🌐 Язык":
        return await choose_language(msg, state)
    if action == "📖 Объяснение темы":
        return await show_theory(msg, state)
    if action == "✍️ Сдать ДЗ":
        return await start_hw(msg, state)
    if action == "🚀 Следующая тема":
        return await check_for_test(msg, state)
    if action == "🎙 Аудио-урок":
        return await start_audio_lesson(msg, state)
    if action == "📝 Начать тест":
        return await start_midterm(msg, state)


# ══════════════════════════════════════════════
#  FALLBACK
# ══════════════════════════════════════════════
@dp.message()
async def fallback(msg: types.Message, state: FSMContext):
    current = await state.get_state()
    if current is not None:
        return
    await ensure_user_name(msg.from_user.id, msg.from_user.username or "", msg.from_user.first_name or "")
    language = await user_language(msg.from_user.id)
    await msg.answer(t("unknown", language), reply_markup=main_kb(language))


# ══════════════════════════════════════════════
#  ФОНОВЫЕ ЗАДАЧИ
# ══════════════════════════════════════════════
import httpx

async def notification_loop():
    day_map = {"пн": 0, "вт": 1, "ср": 2, "чт": 3, "пт": 4, "сб": 5, "вс": 6}
    notified_this_minute: set = set()
    while True:
        try:
            import datetime
            now = datetime.datetime.now()
            await asyncio.sleep(max(1, 60 - now.second))
            now = datetime.datetime.now()
            cur_t = now.strftime("%H:%M")
            day_idx = now.weekday()
            if now.minute == 0:
                notified_this_minute.clear()
            users = await get_users_for_notification(cur_t)
            for row in users:
                cache_key = f"{row['user_id']}_{cur_t}"
                if cache_key in notified_this_minute:
                    continue
                days = [d for d in (row["notify_days"] or "").split(",") if d]
                if any(day_map.get(d) == day_idx for d in days):
                    try:
                        lesson = LESSONS.get(row["lesson_num"])
                        t = lesson["topic"] if lesson else "новому уроку"
                        await bot.send_message(
                            row["user_id"],
                            f"⏰ *Время занятий!*\n\n"
                            f"📍 {t}\n"
                            f"🎙 Не забудь про аудио-урок! Жду тебя! 📚",
                            parse_mode="Markdown"
                        )
                        notified_this_minute.add(cache_key)
                    except Exception as e:
                        logging.error(f"Уведомление {row['user_id']}: {e}")
        except Exception as e:
            logging.error(f"notification_loop: {e}")
            await asyncio.sleep(60)


async def review_words_loop():
    REVIEW_STAGES = [1, 3, 7, 30]
    while True:
        try:
            import datetime
            today = datetime.date.today().strftime("%Y-%m-%d")
            rows = await get_words_for_review(today)
            for row in rows:
                try:
                    await bot.send_message(
                        row["user_id"],
                        f"🔔 *Повторение слова!*\n\n*{row['word']}* = ?\n\nОтвет: _{row['translation']}_",
                        parse_mode="Markdown"
                    )
                    ns = row["review_stage"] + 1
                    nd = REVIEW_STAGES[ns] if ns < len(REVIEW_STAGES) else REVIEW_STAGES[-1]
                    new_date = (datetime.date.today() + datetime.timedelta(days=nd)).strftime("%Y-%m-%d")
                    await update_word_review(row["id"], new_date, ns)
                except Exception as e:
                    logging.error(f"review word id={row['id']}: {e}")
            await asyncio.sleep(3600)
        except Exception as e:
            logging.error(f"review_words_loop: {e}")
            await asyncio.sleep(3600)


# ══════════════════════════════════════════════
#  ЗАПУСК
# ══════════════════════════════════════════════
async def main():
    await init_db()
    asyncio.create_task(notification_loop())
    asyncio.create_task(review_words_loop())
    logging.info("Фоновые задачи запущены.")
    await bot.delete_webhook(drop_pending_updates=True)
    print("=== Бот EnglishDV запущен! ===")
    from src.config import GROQ_API_KEY, OPENAI_API_KEY
    if GROQ_API_KEY:
        audio_mode = "Groq Whisper (whisper-large-v3-turbo)"
    elif OPENAI_API_KEY:
        audio_mode = "OpenAI Whisper"
    else:
        audio_mode = "OpenRouter fallback"
    print(f"=== Аудио-уроки: {audio_mode} ===")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
