"""Клавиатуры бота."""
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


MAIN_MENU_BUTTONS = {
    "🏠 Главная", "👤 Личный кабинет", "💬 Чат с учителем", "🏆 Рейтинг",
    "📚 Мой План", "📘 Слова дня", "📖 Мой словарь",
    "📆 Расписание", "⏰ Уведомления", "🔄 Сброс прогресса",
    "💎 Премиум", "🌐 Язык",
    "📖 Объяснение темы", "✍️ Сдать ДЗ", "🚀 Следующая тема",
    "📝 Начать тест", "🎙 Аудио-урок",
    "🏠 Башкы меню", "👤 Жеке кабинет", "💬 Мугалим менен чат", "🏆 Рейтинг",
    "📚 Менин планым", "📘 Күндүн сөздөрү", "📖 Менин сөздүгүм",
    "📆 Жадыбал", "⏰ Эскертмелер", "🔄 Прогрессти тазалоо",
    "💎 Премиум", "🌐 Тил",
    "📖 Теманы түшүндүрүү", "✍️ Үй тапшырма", "🚀 Кийинки тема",
    "📝 Тест баштоо", "🎙 Аудио-сабак",
}


def main_kb(language: str = "ru"):
    """Главное меню."""
    kb = ReplyKeyboardBuilder()
    if language == "ky":
        kb.row(types.KeyboardButton(text="👤 Жеке кабинет"), types.KeyboardButton(text="💬 Мугалим менен чат"))
        kb.row(types.KeyboardButton(text="🏆 Рейтинг"), types.KeyboardButton(text="📚 Менин планым"))
        kb.row(types.KeyboardButton(text="📘 Күндүн сөздөрү"), types.KeyboardButton(text="📖 Менин сөздүгүм"))
        kb.row(types.KeyboardButton(text="💎 Премиум"), types.KeyboardButton(text="📆 Жадыбал"))
        kb.row(types.KeyboardButton(text="⏰ Эскертмелер"), types.KeyboardButton(text="🔄 Прогрессти тазалоо"))
        kb.row(types.KeyboardButton(text="🌐 Тил"), types.KeyboardButton(text="🏠 Башкы меню"))
    else:
        kb.row(types.KeyboardButton(text="👤 Личный кабинет"), types.KeyboardButton(text="💬 Чат с учителем"))
        kb.row(types.KeyboardButton(text="🏆 Рейтинг"), types.KeyboardButton(text="📚 Мой План"))
        kb.row(types.KeyboardButton(text="📘 Слова дня"), types.KeyboardButton(text="📖 Мой словарь"))
        kb.row(types.KeyboardButton(text="💎 Премиум"), types.KeyboardButton(text="📆 Расписание"))
        kb.row(types.KeyboardButton(text="⏰ Уведомления"), types.KeyboardButton(text="🔄 Сброс прогресса"))
        kb.row(types.KeyboardButton(text="🌐 Язык"), types.KeyboardButton(text="🏠 Главная"))
    return kb.as_markup(resize_keyboard=True)


def lesson_kb(hw_status, language: str = "ru"):
    """Клавиатура урока."""
    kb = ReplyKeyboardBuilder()
    if language == "ky":
        kb.row(types.KeyboardButton(text="📖 Теманы түшүндүрүү"))
        if hw_status == "approved":
            kb.row(types.KeyboardButton(text="🚀 Кийинки тема"))
        else:
            kb.row(types.KeyboardButton(text="✍️ Үй тапшырма"))
        kb.row(types.KeyboardButton(text="🎙 Аудио-сабак"), types.KeyboardButton(text="🏠 Башкы меню"))
    else:
        kb.row(types.KeyboardButton(text="📖 Объяснение темы"))
        if hw_status == "approved":
            kb.row(types.KeyboardButton(text="🚀 Следующая тема"))
        else:
            kb.row(types.KeyboardButton(text="✍️ Сдать ДЗ"))
        kb.row(types.KeyboardButton(text="🎙 Аудио-урок"), types.KeyboardButton(text="🏠 Главная"))
    return kb.as_markup(resize_keyboard=True)


def language_kb():
    """Выбор языка интерфейса."""
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text="Русский", callback_data="lang:ru"),
        types.InlineKeyboardButton(text="Кыргызча", callback_data="lang:ky"),
    )
    return kb.as_markup()


def days_kb(selected_str):
    """Клавиатура выбора дней."""
    kb = InlineKeyboardBuilder()
    selected = [x for x in (selected_str or "").split(",") if x]
    days = [("пн","Пн"),("вт","Вт"),("ср","Ср"),("чт","Чт"),("пт","Пт"),("сб","Сб"),("вс","Вс")]
    for code, name in days:
        mark = "✅" if code in selected else "◻️"
        kb.add(types.InlineKeyboardButton(text=f"{mark} {name}", callback_data=f"day_{code}"))
    kb.adjust(4)
    kb.row(types.InlineKeyboardButton(text="Сохранить дни", callback_data="days_done"))
    return kb.as_markup()


def get_admin_hw_kb(student_id, lesson_num):
    """Клавиатура админа для ДЗ."""
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text="✅ Принять", callback_data=f"hw:approve:{student_id}:{lesson_num}"),
        types.InlineKeyboardButton(text="❌ Отклонить", callback_data=f"hw:reject:{student_id}:{lesson_num}"),
    )
    return kb.as_markup()


def audio_lesson_kb():
    """Клавиатура после получения текста для чтения."""
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="🔄 Другой текст"))
    kb.row(types.KeyboardButton(text="📚 Мой План"), types.KeyboardButton(text="🏠 Главная"))
    return kb.as_markup(resize_keyboard=True)


def word_goal_kb():
    """Клавиатура выбора количества слов."""
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="5 слов"), types.KeyboardButton(text="10 слов"))
    kb.row(types.KeyboardButton(text="📖 Мой словарь"), types.KeyboardButton(text="🏠 Главная"))
    return kb.as_markup(resize_keyboard=True)


def word_learning_kb():
    """Клавиатура для изучения слов."""
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="✅ Выучил"))
    kb.row(types.KeyboardButton(text="🔄 Повторить"), types.KeyboardButton(text="🏠 Главная"))
    return kb.as_markup(resize_keyboard=True)


def cancel_kb():
    """Клавиатура отмены."""
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="🏠 Главная"))
    return kb.as_markup(resize_keyboard=True)


def after_audio_result_kb():
    """Клавиатура после результата аудио-урока."""
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="🎙 Аудио-урок"))
    kb.row(types.KeyboardButton(text="📚 Мой План"), types.KeyboardButton(text="🏠 Главная"))
    return kb.as_markup(resize_keyboard=True)


def test_start_kb():
    """Клавиатура для начала теста."""
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="📝 Начать тест"))
    return kb.as_markup(resize_keyboard=True)
