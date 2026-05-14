"""AI промпты и функции для работы с ИИ."""
import re
import logging
import base64
import httpx
from .config import CLAUDE_API_KEY, OPENAI_API_KEY, GROQ_API_KEY


# ══════════════════════════════════════════════
#  AI SYSTEM PROMPTS
# ══════════════════════════════════════════════
AI_SYSTEM_PROMPT_HW = """Ты — строгий но справедливый учитель английского языка.
Проверяешь домашнее задание студента и выставляешь оценку.

ТВОЯ ЗАДАЧА:
1. Проверить текст на грамматику, пунктуацию, лексику
2. Выставить оценку от 0 до 100 баллов
3. Дать краткий фидбек

КРИТЕРИИ ОЦЕНКИ:
- 90-100: Всё правильно
- 75-89: Небольшие ошибки
- 60-74: Есть ошибки, но задание выполнено
- 40-59: Много ошибок
- 0-39: Нужно полностью переделать

ОБЯЗАТЕЛЬНЫЙ ФОРМАТ (строго соблюдай):
SCORE: [число 0-100]
FEEDBACK: [фидбек на русском, 3-5 предложений]"""

AI_SYSTEM_PROMPT_PHOTO = """Ты — учитель английского языка.
На изображении домашнее задание студента (рукописный текст).

Прочитай текст и проверь грамматику.

ОБЯЗАТЕЛЬНЫЙ ФОРМАТ:
SCORE: [число 0-100]
FEEDBACK: [фидбек на русском, 3-5 предложений с ошибками и похвалой]"""

AI_SYSTEM_PROMPT_CHAT = """Ты — дружелюбный учитель английского языка EnglishDV.

ПРАВИЛА:
1. Сообщение на РУССКОМ — отвечай по-русски, помогай с вопросами об английском.
2. Сообщение на АНГЛИЙСКОМ — проверь грамматику кратко (2-3 предложения).

Отвечай естественно, кратко, дружелюбно."""

AI_SYSTEM_PROMPT_PRONUNCIATION = """Ты — фонетический учитель английского языка.
Студент прочитал вслух текст. Ты получил транскрипцию того, что он произнёс.

ИСХОДНЫЙ ТЕКСТ (эталон): {original_text}
ЧТО ПРОИЗНЁС СТУДЕНТ (транскрипция): {transcribed_text}
ФОКУС УРОКА: {focus}

ТВОЯ ЗАДАЧА:
1. Сравни исходный текст с тем, что произнёс студент
2. Найди слова которые были произнесены неправильно или пропущены
3. Выставь оценку произношения от 0 до 100
4. Дай подробный фидбек с правилами произношения

КРИТЕРИИ ОЦЕНКИ ПРОИЗНОШЕНИЯ:
- 90-100: Почти идеально, мелкие акцентные неточности
- 75-89: Хорошо, но есть проблемы с отдельными звуками
- 60-74: Понятно, но много акцентных ошибок
- 40-59: Трудно понять, нужно больше практики
- 0-39: Текст прочитан с серьёзными ошибками

ОБЯЗАТЕЛЬНЫЙ ФОРМАТ ОТВЕТА:
SCORE: [число 0-100]
PRONUNCIATION_ERRORS: [список слов с ошибками и правильное произношение в скобках, каждое с новой строки через •]
FEEDBACK: [общий фидбек на русском, 2-3 предложения]
TIPS: [1-2 конкретных совета по произношению для этого урока]"""


# ══════════════════════════════════════════════
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ══════════════════════════════════════════════
def parse_ai_score_feedback(ai_response: str):
    """Парсит SCORE и FEEDBACK из ответа ИИ."""
    score = None
    feedback = ai_response

    score_match = re.search(r'SCORE:\s*(\d+)', ai_response, re.IGNORECASE)
    if score_match:
        score = min(100, max(0, int(score_match.group(1))))

    feedback_match = re.search(r'FEEDBACK:\s*(.+?)(?=SCORE:|TIPS:|PRONUNCIATION_ERRORS:|$)',
                                ai_response, re.IGNORECASE | re.DOTALL)
    if feedback_match:
        feedback = feedback_match.group(1).strip()

    if score is None:
        numbers = re.findall(r'\b(\d{1,3})\b', ai_response)
        for n in numbers:
            n = int(n)
            if 0 <= n <= 100:
                score = n
                break
        if score is None:
            score = 70

    return score, feedback


def parse_pronunciation_result(ai_response: str):
    """Парсит полный результат проверки произношения."""
    score = None
    errors = ""
    feedback = ""
    tips = ""

    score_match = re.search(r'SCORE:\s*(\d+)', ai_response, re.IGNORECASE)
    if score_match:
        score = min(100, max(0, int(score_match.group(1))))

    errors_match = re.search(r'PRONUNCIATION_ERRORS:\s*(.+?)(?=FEEDBACK:|TIPS:|$)',
                              ai_response, re.IGNORECASE | re.DOTALL)
    if errors_match:
        errors = errors_match.group(1).strip()

    feedback_match = re.search(r'FEEDBACK:\s*(.+?)(?=TIPS:|SCORE:|$)',
                                ai_response, re.IGNORECASE | re.DOTALL)
    if feedback_match:
        feedback = feedback_match.group(1).strip()

    tips_match = re.search(r'TIPS:\s*(.+?)$', ai_response, re.IGNORECASE | re.DOTALL)
    if tips_match:
        tips = tips_match.group(1).strip()

    if score is None:
        score = 70

    return score, errors, feedback, tips


def score_to_emoji(score: int) -> str:
    """Конвертирует оценку в эмодзи."""
    if score >= 90: return "🏆"
    elif score >= 75: return "🥇"
    elif score >= 60: return "👍"
    elif score >= 40: return "📝"
    else: return "💪"


def bonus_points_for_score(score: int) -> int:
    """Бонусные баллы за оценку."""
    if score >= 90: return 20
    elif score >= 75: return 15
    elif score >= 60: return 10
    else: return 5


# ══════════════════════════════════════════════
#  ТРАНСКРИПЦИЯ АУДИО
# ══════════════════════════════════════════════
async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.ogg") -> str:
    """Транскрибирует аудио через Groq Whisper → OpenAI Whisper → fallback."""
    if GROQ_API_KEY:
        try:
            from groq import AsyncGroq
            client = AsyncGroq(api_key=GROQ_API_KEY)
            
            # Создаем временный файл для аудио
            import tempfile
            import asyncio
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            with open(tmp_path, "rb") as file:
                transcription = await client.audio.transcriptions.create(
                    file=file,
                    model="whisper-large-v3-turbo",
                    temperature=0,
                    response_format="verbose_json",
                )
            
            # Удаляем временный файл
            import os
            os.unlink(tmp_path)
            
            return transcription.text.strip() if transcription.text else "__TRANSCRIPTION_FAILED__"
            
        except Exception as e:
            logging.error(f"Ошибка транскрипции через Groq: {e}")

    if OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    files={
                        "file": (filename, audio_bytes, "audio/ogg"),
                        "model": (None, "whisper-1"),
                        "language": (None, "en"),
                        "response_format": (None, "text"),
                    }
                )
                if response.status_code == 200:
                    return response.text.strip()
                logging.error(f"OpenAI Whisper error: {response.status_code} {response.text}")
        except Exception as e:
            logging.error(f"Ошибка транскрипции через OpenAI: {e}")

    return await transcribe_via_openrouter(audio_bytes)


async def transcribe_via_openrouter(audio_bytes: bytes) -> str:
    """Fallback: транскрипция через OpenRouter."""
    try:
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {CLAUDE_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/whisper-large-v3",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Transcribe this English audio. Return ONLY the transcribed text, nothing else."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:audio/ogg;base64,{audio_b64}"}
                                }
                            ]
                        }
                    ],
                    "max_tokens": 500,
                }
            )
            data = response.json()
            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"].get("content", "").strip()
    except Exception as e:
        logging.error(f"OpenRouter transcription error: {e}")

    return "__TRANSCRIPTION_FAILED__"


# ══════════════════════════════════════════════
#  AI ФУНКЦИИ
# ══════════════════════════════════════════════
async def get_ai_response(
    user_id: int,
    user_text: str,
    user_level: str,
    is_homework: bool = False,
    photo_base64: str = None,
    lesson_topic: str = "",
    system_override: str = None,
) -> str:
    """Получить ответ от ИИ."""
    try:
        if system_override:
            system_prompt = system_override
        elif is_homework:
            system_prompt = AI_SYSTEM_PROMPT_PHOTO if photo_base64 else AI_SYSTEM_PROMPT_HW
        else:
            system_prompt = AI_SYSTEM_PROMPT_CHAT

        messages = []
        if not is_homework and not system_override:
            from .database import get_chat_history, add_to_chat_history
            history = await get_chat_history(user_id, limit=5)
            messages = [{"role": m["role"], "content": m["content"]} for m in history]

        if photo_base64:
            user_content = [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{photo_base64}"}},
                {"type": "text", "text": f"Тема урока: {lesson_topic}\nПроверь домашнее задание на фото."}
            ]
        else:
            if is_homework:
                user_content = f"Тема урока: {lesson_topic}\n\nДомашнее задание:\n\n{user_text}"
            else:
                user_content = user_text

        messages.append({"role": "user", "content": user_content})

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {CLAUDE_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://railway.com",
                    "X-OpenRouter-Title": "EnglishDV Bot",
                },
                json={
                    "model": "nvidia/nemotron-3-super-120b-a12b:free",
                    "messages": [{"role": "system", "content": system_prompt}, *messages],
                    "max_tokens": 800,
                },
            )
            data = response.json()
            if "error" in data:
                logging.error(f"API error: {data['error']}")
                return "❌ Ошибка API. Попробуй ещё раз."
            if "choices" not in data or not data["choices"]:
                return "❌ Нет ответа от модели."
            ai_response = data['choices'][0]['message'].get('content', '').strip()
            if not is_homework and not system_override:
                from .database import add_to_chat_history
                await add_to_chat_history(user_id, "user", user_text)
                await add_to_chat_history(user_id, "assistant", ai_response)
            return ai_response
    except httpx.TimeoutException:
        return "⏱️ Сервер медленный. Попробуй ещё раз."
    except Exception as e:
        logging.error(f"Ошибка ИИ: {e}")
        return f"❌ Ошибка: {str(e)[:50]}"