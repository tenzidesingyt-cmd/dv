"""База данных — все операции с БД."""
import aiosqlite
import datetime
import logging
from pathlib import Path
from .config import DB_PATH


async def init_db():
    """Создаёт таблицы если их нет."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id         INTEGER PRIMARY KEY,
                lesson_num      INTEGER DEFAULT 1,
                hw_status       TEXT    DEFAULT 'not_sent',
                level           TEXT    DEFAULT 'Not Tested',
                notify_days     TEXT    DEFAULT '',
                notify_time     TEXT    DEFAULT '',
                streak          INTEGER DEFAULT 0,
                last_activity   TEXT    DEFAULT '',
                total_words     INTEGER DEFAULT 0,
                points          INTEGER DEFAULT 0,
                username        TEXT    DEFAULT '',
                first_name      TEXT    DEFAULT '',
                last_score      INTEGER DEFAULT 0,
                audio_score     INTEGER DEFAULT 0,
                premium_until   TEXT    DEFAULT '',
                premium_source  TEXT    DEFAULT '',
                language        TEXT    DEFAULT 'ru'
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER,
                word         TEXT,
                translation  TEXT,
                added_date   TEXT,
                next_review  TEXT,
                review_stage INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER,
                role       TEXT,
                content    TEXT,
                created_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS hw_history (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER,
                lesson_num   INTEGER,
                score        INTEGER,
                feedback     TEXT,
                hw_type      TEXT DEFAULT 'text',
                submitted_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id                          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id                     INTEGER,
                payload                     TEXT,
                plan_code                   TEXT,
                amount                      INTEGER,
                currency                    TEXT,
                telegram_payment_charge_id  TEXT,
                provider_payment_charge_id  TEXT,
                paid_at                     TEXT
            )
        """)
        # Миграция для старых БД
        migration_cols = [
            ("username",     "TEXT DEFAULT ''"),
            ("first_name",   "TEXT DEFAULT ''"),
            ("streak",       "INTEGER DEFAULT 0"),
            ("last_activity","TEXT DEFAULT ''"),
            ("total_words",  "INTEGER DEFAULT 0"),
            ("daily_word_goal", "INTEGER DEFAULT 5"),
            ("points",       "INTEGER DEFAULT 0"),
            ("last_score",   "INTEGER DEFAULT 0"),
            ("audio_score",  "INTEGER DEFAULT 0"),
            ("premium_until", "TEXT DEFAULT ''"),
            ("premium_source","TEXT DEFAULT ''"),
            ("language",     "TEXT DEFAULT 'ru'"),
        ]
        for col_name, col_def in migration_cols:
            try:
                await db.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}")
            except Exception:
                pass
        try:
            await db.execute("ALTER TABLE vocabulary ADD COLUMN learned INTEGER DEFAULT 0")
        except Exception:
            pass
        await db.commit()
    logging.info("База данных готова.")


def _parse_iso_datetime(value: str):
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        return None


def user_has_premium(user: dict | None) -> bool:
    """Проверить активный премиум по данным пользователя."""
    if not user:
        return False
    premium_until = _parse_iso_datetime(user.get("premium_until", ""))
    return bool(premium_until and premium_until > datetime.datetime.now())


async def activate_premium(user_id: int, days: int, source: str = "manual"):
    """Выдать или продлить премиум на N дней."""
    user = await get_user(user_id)
    now = datetime.datetime.now()
    current_until = _parse_iso_datetime(user.get("premium_until", "")) if user else None
    start_at = current_until if current_until and current_until > now else now
    premium_until = start_at + datetime.timedelta(days=days)
    await update_user(
        user_id,
        premium_until=premium_until.isoformat(timespec="seconds"),
        premium_source=source,
    )
    return premium_until


async def save_payment(
    user_id: int,
    payload: str,
    plan_code: str,
    amount: int,
    currency: str,
    telegram_payment_charge_id: str,
    provider_payment_charge_id: str,
):
    """Сохранить успешную оплату Telegram Payments."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO payments (
                user_id, payload, plan_code, amount, currency,
                telegram_payment_charge_id, provider_payment_charge_id, paid_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                payload,
                plan_code,
                amount,
                currency,
                telegram_payment_charge_id,
                provider_payment_charge_id,
                datetime.datetime.now().isoformat(timespec="seconds"),
            ),
        )
        await db.commit()


async def get_user(user_id):
    """Получить пользователя по ID."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as c:
            res = await c.fetchone()
            return dict(res) if res else None


async def update_user(user_id, **kwargs):
    """Обновить данные пользователя."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as c:
            if not await c.fetchone():
                await db.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        if kwargs:
            set_str = ", ".join([f"{k} = ?" for k in kwargs.keys()])
            await db.execute(
                f"UPDATE users SET {set_str} WHERE user_id = ?",
                list(kwargs.values()) + [user_id],
            )
        await db.commit()


async def add_points(user_id: int, amount: int):
    """Добавить баллы пользователю."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (amount, user_id))
        await db.commit()


async def ensure_user_name(user_id: int, username: str, first_name: str):
    """Обновить имя пользователя если пустое."""
    u = await get_user(user_id)
    if u and (not u.get("first_name") or not u.get("username")):
        await update_user(user_id, username=username or "", first_name=first_name or "")


async def save_hw_result(user_id: int, lesson_num: int, score: int, feedback: str, hw_type: str = "text"):
    """Сохранить результат ДЗ."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO hw_history (user_id, lesson_num, score, feedback, hw_type, submitted_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, lesson_num, score, feedback, hw_type, datetime.datetime.now().isoformat())
        )
        await db.commit()
    if hw_type == "audio":
        await update_user(user_id, audio_score=score)
    else:
        await update_user(user_id, last_score=score)


async def update_streak(user_id):
    """Обновить стрик активности."""
    await update_user(user_id)
    user = await get_user(user_id)
    if not user:
        return 1
    today = datetime.date.today()
    last_act_str = user.get("last_activity", "")
    streak = user.get("streak", 0)
    if last_act_str:
        try:
            last_act = datetime.datetime.strptime(last_act_str, "%Y-%m-%d").date()
            delta = (today - last_act).days
            if delta == 1:
                streak += 1
            elif delta > 1:
                streak = 1
        except ValueError:
            streak = 1
    else:
        streak = 1
    await update_user(user_id, streak=streak, last_activity=today.strftime("%Y-%m-%d"))
    return streak


async def add_to_chat_history(user_id, role, content):
    """Добавить в историю чата."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO chat_history (user_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (user_id, role, content, datetime.datetime.now().isoformat())
        )
        await db.commit()


async def get_chat_history(user_id, limit=5):
    """Получить историю чата."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT role, content FROM chat_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ) as cursor:
            return list(reversed([dict(m) for m in await cursor.fetchall()]))


async def clear_chat_history(user_id):
    """Очистить историю чата."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        await db.commit()


async def get_leaderboard(limit=10):
    """Получить топ пользователей."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT user_id, points, username, first_name, last_score, audio_score FROM users ORDER BY points DESC LIMIT ?",
            (limit,)
        ) as c:
            return await c.fetchall()


async def get_users_for_notification(cur_t):
    """Получить пользователей для уведомления."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE notify_time = ?", (cur_t,)) as cursor:
            return await cursor.fetchall()


async def get_words_for_review(today):
    """Получить слова для повторения."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM vocabulary WHERE next_review = ?", (today,)) as cursor:
            return await cursor.fetchall()


async def update_word_review(word_id, new_date, new_stage):
    """Обновить дату повторения слова."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE vocabulary SET next_review = ?, review_stage = ? WHERE id = ?",
            (new_date, new_stage, word_id)
        )
        await db.commit()


async def add_word(user_id, word, translation):
    """Добавить слово в словарь."""
    today = datetime.date.today()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO vocabulary (user_id, word, translation, added_date, next_review) VALUES (?, ?, ?, ?, ?)",
            (user_id, word, translation, today.strftime("%Y-%m-%d"),
             (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")),
        )
        await db.execute("UPDATE users SET total_words = total_words + 1 WHERE user_id = ?", (user_id,))
        await db.commit()


async def get_vocabulary(user_id, limit=20, learned_only=False):
    """Получить словарь пользователя."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if learned_only:
            query = "SELECT word, translation FROM vocabulary WHERE user_id = ? AND learned = 0 ORDER BY id DESC LIMIT ?"
        else:
            query = "SELECT word, translation, learned FROM vocabulary WHERE user_id = ? ORDER BY id DESC LIMIT ?"
        async with db.execute(query, (user_id, limit)) as c:
            return await c.fetchall()


async def get_unlearned_words(user_id, limit=10):
    """Получить незакреплённые слова для тренировки."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, word, translation FROM vocabulary WHERE user_id = ? AND learned = 0 ORDER BY id ASC LIMIT ?",
            (user_id, limit),
        ) as c:
            return await c.fetchall()


async def mark_word_learned(word_id):
    """Отметить слово как выученное."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE vocabulary SET learned = 1 WHERE id = ?",
            (word_id,),
        )
        await db.commit()


async def get_admin_stats():
    """Получить статистику для админа."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c:
            total_users = (await c.fetchone())[0]
        async with db.execute("SELECT SUM(total_words) FROM users") as c:
            total_words = (await c.fetchone())[0] or 0
        async with db.execute("SELECT COUNT(*) FROM users WHERE hw_status = 'pending'") as c:
            pending_hw = (await c.fetchone())[0]
        async with db.execute("SELECT AVG(score) FROM hw_history WHERE hw_type != 'audio'") as c:
            avg_score = (await c.fetchone())[0] or 0
        async with db.execute("SELECT AVG(score) FROM hw_history WHERE hw_type = 'audio'") as c:
            avg_audio = (await c.fetchone())[0] or 0
        async with db.execute("SELECT COUNT(*) FROM hw_history WHERE hw_type = 'audio'") as c:
            audio_count = (await c.fetchone())[0]
        return {
            "total_users": total_users,
            "total_words": total_words,
            "pending_hw": pending_hw,
            "avg_score": avg_score,
            "avg_audio": avg_audio,
            "audio_count": audio_count,
        }
