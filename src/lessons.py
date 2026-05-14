"""Данные уроков (25 уроков)."""
from typing import Dict

LESSONS: Dict[int, Dict] = {
    1: {
        "topic": "Глагол To Be (Основа основ)",
        "explanation": (
            "🌟 *Глагол To Be* — фундамент английского.\n\n"
            "*Три формы в Present:*\n"
            "• *AM* — для 'I'\n• *IS* — для He, She, It\n• *ARE* — для We, You, They\n\n"
            "*Примеры:*\n`I am happy.` `She is a doctor.` `We are students.`\n\n"
            "*Отрицание:*\n`I am not tired.` `He is not here.`\n\n"
            "*Вопрос:*\n`Are you happy?`"
        ),
        "video": "https://youtu.be/gZE0DdpwRew",
        "tasks": (
            "📝 *ДЗ №1:* Напиши 10 предложений о себе и друзьях, используя am, is, are.\n\n"
            "Пример: `I am a student. My best friend is kind.`\n\n"
            "✍️ Текстом или 📷 фото рукописного текста!"
        ),
        "min_sentences": 10,
    },
    2: {
        "topic": "Артикли A, An, The",
        "explanation": (
            "🌟 *Артикли* — определители предметов.\n\n"
            "*A* — перед согласными: `a dog`, `a car`\n"
            "*AN* — перед гласными: `an apple`, `an idea`\n"
            "*THE* — конкретный предмет: `the sun`, `the Eiffel Tower`\n\n"
            "*⚠️ A/An нельзя перед множественным числом!*"
        ),
        "video": "https://www.youtube.com/watch?v=articles_english",
        "tasks": "📝 *ДЗ №2:* 5 слов с 'a', 5 с 'an', 5 с 'the'. Для каждого — предложение.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    3: {
        "topic": "Present Simple",
        "explanation": (
            "🌟 *Present Simple* — регулярные действия.\n\n"
            "*I/You/We/They* + глагол\n*He/She/It* + глагол + -S/-ES\n\n"
            "`I work every day.` `She works in a bank.`\n\n"
            "*Сигналы:* every day, usually, often, always, never\n\n"
            "*Отрицание:*\n`I don't work.` `He doesn't like coffee.`"
        ),
        "video": "https://www.youtube.com/watch?v=present_simple",
        "tasks": "📝 *ДЗ №3:* 15 предложений о привычках (Present Simple).\n\nИспользуй: always, usually, often, never, every day.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    4: {
        "topic": "Present Continuous",
        "explanation": (
            "🌟 *Present Continuous* — действие СЕЙЧАС.\n\n"
            "*am/is/are + глагол + -ING*\n\n"
            "`I am studying English.` `He is playing.`\n\n"
            "*Правила -ING:*\nwork → working | write → writing | run → running\n\n"
            "*Сигналы:* now, right now, at this moment, Look!, Listen!"
        ),
        "video": "https://www.youtube.com/watch?v=present_continuous",
        "tasks": "📝 *ДЗ №4:* 15 предложений о том, что происходит прямо сейчас.\n\nПример: `I am writing my homework.`\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    5: {
        "topic": "Past Simple",
        "explanation": (
            "🌟 *Past Simple* — завершённые действия в прошлом.\n\n"
            "*Правильные:* work → worked | play → played\n\n"
            "*Неправильные:*\ngo → went | see → saw | eat → ate\ncome → came | have → had\n\n"
            "`I worked yesterday.` `She went to Paris.`\n\n"
            "*Сигналы:* yesterday, last week, ago, in 2020"
        ),
        "video": "https://www.youtube.com/watch?v=past_simple",
        "tasks": "📝 *ДЗ №5:* Рассказ о дне вчера (20+ предложений, Past Simple).\n\nИспользуй правильные И неправильные глаголы!\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    6: {
        "topic": "Прилагательные и сравнение",
        "explanation": (
            "🌟 *Прилагательные* описывают существительные.\n\n"
            "*Короткие:* big → bigger → the biggest\n"
            "*Длинные:* beautiful → more beautiful → the most beautiful\n"
            "*Неправильные:* good → better → the best | bad → worse → the worst"
        ),
        "video": "https://www.youtube.com/watch?v=adjectives",
        "tasks": "📝 *ДЗ №6:* 5 предметов и 5 людей с формами сравнения (по 3 предложения).\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    7: {
        "topic": "Present Perfect",
        "explanation": (
            "🌟 *Present Perfect* — прошлое, результат важен сейчас.\n\n"
            "*have/has + Past Participle*\n\n"
            "`I have visited Paris.` `She has finished.`\n\n"
            "*Сигналы:* ever, never, just, already, yet, recently, for, since"
        ),
        "video": "https://www.youtube.com/watch?v=present_perfect",
        "tasks": "📝 *ДЗ №7:* 20 предложений о жизненных опытах (ever/never/just/already/yet).\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    8: {
        "topic": "Модальные глаголы",
        "explanation": (
            "🌟 *Модальные глаголы:*\n\n"
            "*CAN:* `I can swim.` — умею\n"
            "*MUST:* `I must study.` — обязан\n"
            "*SHOULD:* `You should rest.` — совет\n"
            "*MAY:* `May I enter?` — разрешение\n\n"
            "*⚠️ После модальных — базовая форма без TO!*"
        ),
        "video": "https://www.youtube.com/watch?v=modal_verbs",
        "tasks": "📝 *ДЗ №8:* По 5 предложений с can, must, should.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    9: {
        "topic": "Future Simple",
        "explanation": (
            "🌟 *Future Simple:*\n\n"
            "*will + глагол:* `I will travel.` `She won't come.`\n\n"
            "*be going to* — спланированные:\n`I am going to study engineering.`\n\n"
            "will — спонтанно | be going to — уже решил"
        ),
        "video": "https://www.youtube.com/watch?v=future_simple",
        "tasks": "📝 *ДЗ №9:* 20 предложений о планах (will + be going to).\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    10: {
        "topic": "Условные предложения",
        "explanation": (
            "🌟 *Conditionals:*\n\n"
            "*Zero:* If + Present, Present → `If you heat water, it boils.`\n"
            "*First:* If + Present, will → `If you study, you will pass.`\n"
            "*Second:* If + Past, would → `If I were rich, I would travel.`"
        ),
        "video": "https://www.youtube.com/watch?v=conditionals",
        "tasks": "📝 *ДЗ №10:* 15 условных предложений (5 Zero, 5 First, 5 Second).\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    11: {
        "topic": "Предлоги",
        "explanation": (
            "🌟 *Место:* in — внутри | on — на | at — у\nunder — под | between — между\n\n"
            "🌟 *Время:* in + месяц/год | on + день | at + время\n\n"
            "`The cat is under the table.` `Meet at 5 o'clock.`"
        ),
        "video": "https://www.youtube.com/watch?v=prepositions",
        "tasks": "📝 *ДЗ №11:* 20 предложений с предлогами места и времени.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    12: {
        "topic": "Вопросительные слова",
        "explanation": (
            "🌟 *Вопросительные слова:*\n"
            "What | Who | Where | When | Why | How\n\n"
            "*Составные:* How many | How much | How old | What time"
        ),
        "video": "https://www.youtube.com/watch?v=question_words",
        "tasks": "📝 *ДЗ №12:* 20 вопросов с разными вопросительными словами.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    13: {
        "topic": "Числительные и даты",
        "explanation": (
            "🌟 *Порядковые:* 1st, 2nd, 3rd, 4th...\n\n"
            "🌟 *Даты:* April 13 = the 13th of April\n\n"
            "🌟 *Время:* 3:15 = quarter past three | 3:30 = half past three"
        ),
        "video": "https://www.youtube.com/watch?v=numbers_dates",
        "tasks": "📝 *ДЗ №13:* Даты рождения 5 друзей, время встреч и цены прописью.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 10,
    },
    14: {
        "topic": "Passive Voice",
        "explanation": (
            "🌟 *Страдательный залог:* to be + Past Participle\n\n"
            "*Present:* A book is written by John.\n"
            "*Past:* This house was built in 2020.\n"
            "*Future:* A stadium will be built."
        ),
        "video": "https://www.youtube.com/watch?v=passive_voice",
        "tasks": "📝 *ДЗ №14:* 10 активных предложений переведи в пассивный залог.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 10,
    },
    15: {
        "topic": "Фразальные глаголы",
        "explanation": (
            "🌟 *Фразальные глаголы:*\n"
            "get up | look after | take off | put on\nturn on/off | give up | look for"
        ),
        "video": "https://www.youtube.com/watch?v=phrasal_verbs",
        "tasks": "📝 *ДЗ №15:* 15 предложений с фразальными глаголами.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    16: {
        "topic": "Косвенная речь",
        "explanation": (
            "🌟 *Reported Speech:*\n\n"
            "Direct: He said, 'I am tired.'\nReported: He said that he *was* tired.\n\n"
            "*Сдвиг:* Present→Past | now→then | today→that day"
        ),
        "video": "https://www.youtube.com/watch?v=reported_speech",
        "tasks": "📝 *ДЗ №16:* 10 прямых речей переведи в косвенную.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 10,
    },
    17: {
        "topic": "Союзы",
        "explanation": (
            "🌟 *Координирующие:* and | but | or | so\n\n"
            "🌟 *Подчиняющие:* because | if | when | although\n\n"
            "🌟 *Вводные:* First | Finally | Moreover | However"
        ),
        "video": "https://www.youtube.com/watch?v=conjunctions",
        "tasks": "📝 *ДЗ №17:* Рассказ 20-25 предложений со всеми типами союзов.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    18: {
        "topic": "Сравнение прилагательных",
        "explanation": (
            "🌟 *Краткие:* big → bigger → the biggest\n"
            "🌟 *Длинные:* important → more → the most\n"
            "🌟 *Неправильные:* good→better→best | bad→worse→worst"
        ),
        "video": "https://www.youtube.com/watch?v=comparison",
        "tasks": "📝 *ДЗ №18:* 5 предметов и 5 людей, по 3 предложения с разными формами сравнения.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    19: {
        "topic": "Исчисляемые и неисчисляемые",
        "explanation": (
            "🌟 *Countable:* a/an | some/many | How many?\n`one apple, two books`\n\n"
            "🌟 *Uncountable:* some/much (без мн.ч.) | How much?\n`some water, some milk`\n\n"
            "❌ a water | ✅ some water"
        ),
        "video": "https://www.youtube.com/watch?v=countable_uncountable",
        "tasks": "📝 *ДЗ №19:* 10 исчисляемых + 10 неисчисляемых с предложениями.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    20: {
        "topic": "Обзор всех времён",
        "explanation": (
            "🌟 *ФИНАЛЬНЫЙ УРОК!*\n\n"
            "🔴 Present: Simple | Continuous | Perfect\n"
            "🔵 Past: Simple | Continuous | Perfect\n"
            "🟢 Future: Simple | Continuous | Perfect\n\n"
            "✨ *ПОЗДРАВЛЯЕМ С ОКОНЧАНИЕМ КУРСА!* 🎉"
        ),
        "video": "https://www.youtube.com/watch?v=review_all_tenses",
        "tasks": "📝 *ФИНАЛЬНОЕ ДЗ №20:* История 40-50 предложений со ВСЕМИ временами!\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 40,
    },
    21: {
        "topic": "Advanced: Модальные глаголы",
        "explanation": (
            "🌟 *COULD:* `Could you help me?` — вежливо\n"
            "🌟 *MIGHT:* `I might go.` — возможно\n"
            "🌟 *OUGHT TO:* `You ought to exercise.`\n"
            "🌟 *NEED TO:* `I need to study more.`"
        ),
        "video": "https://www.youtube.com/watch?v=advanced_modals",
        "tasks": "📝 *ДЗ №21:* 15 предложений с could, might, ought to, need to.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    22: {
        "topic": "Past Perfect и Past Perfect Continuous",
        "explanation": (
            "🌟 *Past Perfect:* had + Past Participle\n`By the time she arrived, I had finished.`\n\n"
            "🌟 *Past Perfect Continuous:* had been + -ing\n`She had been studying for 3 hours.`"
        ),
        "video": "https://www.youtube.com/watch?v=past_perfect",
        "tasks": "📝 *ДЗ №22:* 10 Past Perfect + 10 Past Perfect Continuous.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    23: {
        "topic": "Future Perfect и Future Continuous",
        "explanation": (
            "🌟 *Future Perfect:* will have + PP\n`By next year, I will have learned 500 words.`\n\n"
            "🌟 *Future Continuous:* will be + -ing\n`At 5 PM tomorrow, I will be studying.`"
        ),
        "video": "https://www.youtube.com/watch?v=future_perfect",
        "tasks": "📝 *ДЗ №23:* 10 Future Perfect + 10 Future Continuous.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 20,
    },
    24: {
        "topic": "Слова-связки (Transition Words)",
        "explanation": (
            "🌟 *Добавление:* moreover, furthermore, also\n"
            "🌟 *Противление:* however, nevertheless\n"
            "🌟 *Причина:* therefore, as a result\n"
            "🌟 *Порядок:* first, then, finally"
        ),
        "video": "https://www.youtube.com/watch?v=transitions",
        "tasks": "📝 *ДЗ №24:* Рассказ 30 предложений с 10+ transition words.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 30,
    },
    25: {
        "topic": "Идиомы (Idioms)",
        "explanation": (
            "🌟 *ENGLISH IDIOMS:*\n\n"
            "break the ice — начать разговор\nunder the weather — плохо себя чувствовать\n"
            "piece of cake — проще простого\ngive up — сдаваться\non cloud nine — в восторге"
        ),
        "video": "https://www.youtube.com/watch?v=english_idioms",
        "tasks": "📝 *ДЗ №25:* 15 предложений с idioms. Объясни значение каждого.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 15,
    },
    26: {
        "topic": "Premium: Travel English",
        "premium": True,
        "explanation": (
            "🌟 *Travel English* — английский для поездок.\n\n"
            "*At the airport:* `I have a reservation.` `Where is gate 12?`\n"
            "*At the hotel:* `Can I check in?` `Is breakfast included?`\n"
            "*In the city:* `How much is the ticket?` `Could you help me?`\n\n"
            "Главная формула вежливости: *Could I...? / Could you...?*"
        ),
        "video": "https://www.youtube.com/watch?v=travel_english",
        "tasks": "📝 *ДЗ №26:* Напиши диалог в аэропорту или отеле на 14-18 реплик. Используй could, reservation, ticket, check in.\n\n✍️ Текстом или 📷 фото!",
        "min_sentences": 14,
    },
    27: {
        "topic": "Premium: Business English Basics",
        "premium": True,
        "explanation": (
            "🌟 *Business English* — базовые фразы для работы.\n\n"
            "`Let's schedule a meeting.` — Давайте назначим встречу.\n"
            "`Could you send me the report?` — Можете отправить отчёт?\n"
            "`The deadline is Friday.` — Дедлайн в пятницу.\n\n"
            "Для деловой речи используй короткие ясные предложения и вежливые просьбы."
        ),
        "video": "https://www.youtube.com/watch?v=business_english",
        "tasks": "📝 *ДЗ №27:* Напиши рабочее письмо на английском: попроси отчёт, предложи время встречи и уточни дедлайн. 120-160 слов.",
        "min_sentences": 10,
    },
    28: {
        "topic": "Premium: Speaking Fluency",
        "premium": True,
        "explanation": (
            "🌟 *Speaking Fluency* — как говорить плавнее.\n\n"
            "Используй связки: `Well`, `Actually`, `In my opinion`, `For example`, `That means`.\n"
            "Не переводи каждое слово. Говори блоками: мнение → пример → вывод.\n\n"
            "Шаблон: `In my opinion, ... For example, ... That's why ...`"
        ),
        "video": "https://www.youtube.com/watch?v=speaking_fluency",
        "tasks": "📝 *ДЗ №28:* Запиши или напиши монолог 1-2 минуты на тему `My goals in English`. Добавь 5 linking phrases.",
        "min_sentences": 12,
    },
    29: {
        "topic": "Premium: IELTS Writing Intro",
        "premium": True,
        "explanation": (
            "🌟 *IELTS Writing Intro* — структура академического ответа.\n\n"
            "Task 2 обычно строится так: introduction, body 1, body 2, conclusion.\n"
            "Во вступлении перефразируй тему и дай позицию.\n\n"
            "`This essay will discuss...` — нейтральная фраза для плана ответа."
        ),
        "video": "https://www.youtube.com/watch?v=ielts_writing_task_2",
        "tasks": "📝 *ДЗ №29:* Напиши IELTS-style эссе 180-220 слов: `Online learning is better than classroom learning. Do you agree?`",
        "min_sentences": 16,
    },
    30: {
        "topic": "Premium: Job Interview English",
        "premium": True,
        "explanation": (
            "🌟 *Job Interview English* — собеседование на английском.\n\n"
            "Частые вопросы: `Tell me about yourself`, `What are your strengths?`, `Why do you want this job?`\n"
            "Отвечай по формуле: опыт → навык → пример → результат.\n\n"
            "`I am good at solving problems because...`"
        ),
        "video": "https://www.youtube.com/watch?v=job_interview_english",
        "tasks": "📝 *ДЗ №30:* Ответь письменно на 5 вопросов собеседования. Каждый ответ 3-5 предложений.",
        "min_sentences": 15,
    },
}


# Тесты для вступительного и промежуточного
INTRO_QUESTIONS = [
    # Уровень A1 (базовый)
    {"q": "I ___ a doctor.", "a": "am", "options": ["am", "is", "are"], "level": "A1"},
    {"q": "She ___ an apple every day.", "a": "eats", "options": ["eat", "eats", "eating"], "level": "A1"},
    {"q": "My name ___ Alex.", "a": "is", "options": ["am", "is", "are"], "level": "A1"},
    {"q": "They ___ students.", "a": "are", "options": ["am", "is", "are"], "level": "A1"},
    
    # Уровень A2 (средний)
    {"q": "I ___ (not/like) coffee.", "a": "don't like", "options": ["doesn't like", "don't like", "not like"], "level": "A2"},
    {"q": "Yesterday I ___ (go) to the park.", "a": "went", "options": ["go", "went", "gone"], "level": "A2"},
    {"q": "Look! She ___ (play) with her phone.", "a": "is playing", "options": ["plays", "is playing", "playing"], "level": "A2"},
    {"q": "___ you like pizza?", "a": "Do", "options": ["Do", "Does", "Are"], "level": "A2"},
    
    # Уровень B1 (выше среднего)
    {"q": "If I ___ (have) time, I will help you.", "a": "have", "options": ["have", "had", "would have"], "level": "B1"},
    {"q": "By next year, I ___ (live) in London for 5 years.", "a": "will have lived", "options": ["will live", "will have lived", "have lived"], "level": "B1"},
    {"q": "She said she ___ (be) busy yesterday.", "a": "was", "options": ["is", "was", "were"], "level": "B1"},
    {"q": "___ he had told me, I would have helped.", "a": "If", "options": ["If", "When", "Unless"], "level": "B1"},
]

MIDTERM_TEST = [
    {"q": "I ___ (be) very happy right now.", "a": "am", "options": ["am", "is", "are"], "level": "B1"},
    {"q": "She ___ (be) at home at the moment.", "a": "is", "options": ["is", "am", "are"], "level": "B1"},
    {"q": "They ___ (play) football now.", "a": "are playing", "options": ["play", "are playing", "playing"], "level": "B1"},
    {"q": "He ___ (have) lived here since 2010.", "a": "has", "options": ["have", "has", "had"], "level": "B2"},
    {"q": "I ___ (not/understand) this exercise yet.", "a": "don't understand", "options": ["don't understand", "doesn't understand", "not understand"], "level": "B2"},
    {
        "q": "What is a verb? Напиши своим словами.",
        "type": "open",
        "keywords": ["action", "doing", "state", "word", "run", "go", "be", "have", "do", "write", "verb"],
        "level": "B2"
    },
]

WORD_BANK = [
    {"word": "apple", "translation": "яблоко"},
    {"word": "book", "translation": "книга"},
    {"word": "friend", "translation": "друг"},
    {"word": "school", "translation": "школа"},
    {"word": "house", "translation": "дом"},
    {"word": "family", "translation": "семья"},
    {"word": "work", "translation": "работа"},
    {"word": "city", "translation": "город"},
    {"word": "food", "translation": "еда"},
    {"word": "time", "translation": "время"},
    {"word": "water", "translation": "вода"},
    {"word": "music", "translation": "музыка"},
    {"word": "movie", "translation": "фильм"},
    {"word": "happy", "translation": "счастливый"},
    {"word": "sad", "translation": "грустный"},
    {"word": "beautiful", "translation": "красивый"},
    {"word": "cold", "translation": "холодный"},
    {"word": "hot", "translation": "горячий"},
    {"word": "good", "translation": "хороший"},
    {"word": "bad", "translation": "плохой"},
    {"word": "new", "translation": "новый"},
    {"word": "old", "translation": "старый"},
    {"word": "easy", "translation": "легкий"},
    {"word": "difficult", "translation": "сложный"},
    {"word": "night", "translation": "ночь"},
    {"word": "day", "translation": "день"},
    {"word": "morning", "translation": "утро"},
    {"word": "evening", "translation": "вечер"},
    {"word": "drink", "translation": "пить"},
    {"word": "phone", "translation": "телефон"},
    {"word": "computer", "translation": "компьютер"},
    {"word": "travel", "translation": "путешествовать"},
    {"word": "learn", "translation": "учить"},
    {"word": "listen", "translation": "слушать"},
    {"word": "speak", "translation": "говорить"},
]
