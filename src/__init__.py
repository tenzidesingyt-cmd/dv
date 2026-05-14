"""EnglishDV Telegram Bot package."""
from .config import BOT_TOKEN, ADMIN_ID, CLAUDE_API_KEY, OPENAI_API_KEY, GROQ_API_KEY, DB_PATH
from .database import init_db, get_user, update_user, add_points
from .lessons import LESSONS, INTRO_QUESTIONS, MIDTERM_TEST
from .keyboards import main_kb, lesson_kb, MAIN_MENU_BUTTONS
from .ai import get_ai_response, parse_ai_score_feedback, score_to_emoji
from .reading_texts import READING_TEXTS, get_random_reading_text