"""Тексты для аудио-уроков (чтение вслух)."""
import random
from typing import Dict, List

READING_TEXTS: Dict[int, List[Dict]] = {
    1: [
        {
            "text": "I am a student. She is my teacher. We are friends. He is happy today.",
            "focus": "am, is, are",
            "tip": "Обрати внимание на произношение: AM [æm], IS [ɪz], ARE [ɑːr]"
        },
        {
            "text": "My name is Alex. I am from Russia. My sister is a doctor. They are at home.",
            "focus": "to be в разных лицах",
            "tip": "IS произносится как [ɪz], не [ис]"
        },
    ],
    2: [
        {
            "text": "I have a dog and an apple. The dog is big. An elephant is in the zoo.",
            "focus": "a, an, the",
            "tip": "A [ə] перед согласными, AN [æn] перед гласными"
        },
        {
            "text": "She has a car. It is an old car. The car is red. An umbrella is useful.",
            "focus": "артикли",
            "tip": "THE произносится [ðə] перед согласными и [ðiː] перед гласными"
        },
    ],
    3: [
        {
            "text": "I work every day. She works at a hospital. They play football on Sundays.",
            "focus": "-s/-es окончания",
            "tip": "works [wɜːrks], plays [pleɪz] — окончание -s меняет звучание"
        },
        {
            "text": "He usually drinks coffee in the morning. We always study English together.",
            "focus": "Present Simple с наречиями",
            "tip": "usually [ˈjuːʒuəli], always [ˈɔːlweɪz]"
        },
    ],
    4: [
        {
            "text": "I am studying English right now. She is reading a book. They are playing outside.",
            "focus": "am/is/are + ing",
            "tip": "studying [ˈstʌdiɪŋ], reading [ˈriːdɪŋ] — окончание -ing"
        },
        {
            "text": "Look! The cat is sleeping on the sofa. Listen! Someone is knocking at the door.",
            "focus": "Present Continuous",
            "tip": "sleeping [ˈsliːpɪŋ], knocking [ˈnɒkɪŋ]"
        },
    ],
    5: [
        {
            "text": "Yesterday I went to school. She saw a beautiful bird. They ate pizza for dinner.",
            "focus": "неправильные глаголы в прошлом",
            "tip": "went [went], saw [sɔː], ate [eɪt] — неправильные формы"
        },
        {
            "text": "Last week we visited our grandparents. He worked hard and finished the project.",
            "focus": "правильные и неправильные глаголы",
            "tip": "visited [ˈvɪzɪtɪd], worked [wɜːrkt], finished [ˈfɪnɪʃt]"
        },
    ],
    6: [
        {
            "text": "This book is more interesting than that one. She is the most beautiful girl in class.",
            "focus": "сравнительные прилагательные",
            "tip": "more [mɔːr], most [moʊst], interesting [ˈɪntrəstɪŋ]"
        },
        {
            "text": "My brother is taller than me. The blue car is faster than the red one.",
            "focus": "short adjectives comparison",
            "tip": "taller [ˈtɔːlər], faster [ˈfæstər] — двойное произношение er"
        },
    ],
    7: [
        {
            "text": "I have already eaten breakfast. She has never visited London. Have you ever seen a whale?",
            "focus": "Present Perfect",
            "tip": "already [ɔːlˈredi], never [ˈnevər], ever [ˈevər]"
        },
        {
            "text": "They have just arrived. He has not finished his homework yet. We have been friends for years.",
            "focus": "just, yet, for",
            "tip": "just [dʒʌst], yet [jet] — короткие слова, важна чёткость"
        },
    ],
    8: [
        {
            "text": "I can swim very well. You must study harder. She should drink more water every day.",
            "focus": "модальные глаголы",
            "tip": "can [kæn], must [mʌst], should [ʃʊd]"
        },
        {
            "text": "May I open the window? You cannot park here. We should help our neighbors.",
            "focus": "may, cannot, should",
            "tip": "cannot [ˈkænɒt] — одно слово, не can not"
        },
    ],
    9: [
        {
            "text": "I will travel to Paris next summer. She is going to study medicine at university.",
            "focus": "will и be going to",
            "tip": "will [wɪl], going to [ˈɡoʊɪŋ tuː] — слитное произношение"
        },
        {
            "text": "They will not come to the party. Are you going to visit your parents this weekend?",
            "focus": "отрицание и вопросы в будущем",
            "tip": "won't [woʊnt] — сокращение от will not"
        },
    ],
    10: [
        {
            "text": "If you study hard, you will pass the exam. If it rains, we will stay at home.",
            "focus": "First Conditional",
            "tip": "if [ɪf] — краткое произношение, will [wɪl]"
        },
        {
            "text": "If I were a bird, I would fly around the world. If she had more time, she would read more books.",
            "focus": "Second Conditional",
            "tip": "were [wɜːr], would [wʊd] — важны для Second Conditional"
        },
    ],
    11: [
        {
            "text": "The cat is under the table. My keys are on the desk. She works at the hospital.",
            "focus": "предлоги места",
            "tip": "under [ˈʌndər], table [ˈteɪbəl], hospital [ˈhɒspɪtəl]"
        },
        {
            "text": "I was born in May. The meeting is on Monday at three o'clock in the afternoon.",
            "focus": "предлоги времени",
            "tip": "o'clock [əˈklɒk], afternoon [ˌɑːftəˈnuːn]"
        },
    ],
    12: [
        {
            "text": "What is your name? Where do you live? When is your birthday? Why do you study English?",
            "focus": "вопросительные слова",
            "tip": "what [wɒt], where [weər], when [wen], why [waɪ]"
        },
        {
            "text": "How old are you? How many books do you have? How much water do you drink per day?",
            "focus": "How much / How many",
            "tip": "how [haʊ], many [ˈmeni], much [mʌtʃ]"
        },
    ],
    13: [
        {
            "text": "Today is the first of April. My birthday is on the twenty-third of September.",
            "focus": "порядковые числительные",
            "tip": "first [fɜːrst], third [θɜːrd] — звук [θ] как в think"
        },
        {
            "text": "It is quarter past three. The train arrives at half past seven in the evening.",
            "focus": "время по-английски",
            "tip": "quarter [ˈkwɔːrtər], half [hɑːf] — half не читается как хаф!"
        },
    ],
    14: [
        {
            "text": "This book was written by a famous author. English is spoken all over the world.",
            "focus": "страдательный залог",
            "tip": "written [ˈrɪtən], spoken [ˈspoʊkən] — past participle"
        },
        {
            "text": "The letter was sent yesterday. The house will be built next year.",
            "focus": "Passive в разных временах",
            "tip": "sent [sent], built [bɪlt] — неправильные причастия"
        },
    ],
    15: [
        {
            "text": "Please turn off the lights when you leave. I always get up at seven in the morning.",
            "focus": "фразальные глаголы",
            "tip": "turn off [tɜːrn ɒf], get up [ɡet ʌp] — раздельное произношение"
        },
        {
            "text": "Don't give up! Look for your keys. She put on her coat and went outside.",
            "focus": "give up, look for, put on",
            "tip": "give up [ɡɪv ʌp], look for [lʊk fɔːr]"
        },
    ],
    16: [
        {
            "text": "He said that he was tired. She told me that she had finished her work already.",
            "focus": "косвенная речь",
            "tip": "said [sed], told [toʊld] — прошедшие формы say и tell"
        },
        {
            "text": "They said that they would come the next day. He asked if I wanted some coffee.",
            "focus": "reported questions",
            "tip": "asked [ɑːskt], wanted [ˈwɒntɪd]"
        },
    ],
    17: [
        {
            "text": "I like coffee, but she prefers tea. He studied hard, so he passed the exam.",
            "focus": "союзы and, but, so",
            "tip": "but [bʌt], so [soʊ], prefer [prɪˈfɜːr]"
        },
        {
            "text": "Although it was raining, we went for a walk. I stayed because I wanted to help.",
            "focus": "although, because",
            "tip": "although [ɔːlˈðoʊ] — звук [ð] как в this, the"
        },
    ],
    18: [
        {
            "text": "This is the best movie I have ever seen. She is more intelligent than her sister.",
            "focus": "сравнения: best, more",
            "tip": "best [best], intelligent [ɪnˈtelɪdʒənt]"
        },
        {
            "text": "The weather is worse today than yesterday. He runs faster than anyone in the school.",
            "focus": "worse, faster",
            "tip": "worse [wɜːrs], faster [ˈfæstər]"
        },
    ],
    19: [
        {
            "text": "I need some water. How many apples do you have? There is not much sugar left.",
            "focus": "countable / uncountable",
            "tip": "sugar [ˈʃʊɡər], water [ˈwɔːtər], apple [ˈæpəl]"
        },
        {
            "text": "She gave me some good advice. We need some information about the schedule.",
            "focus": "неисчисляемые: advice, information",
            "tip": "advice [ədˈvaɪs], information [ˌɪnfəˈmeɪʃən]"
        },
    ],
    20: [
        {
            "text": "I have been studying English for two years. By next month I will have finished all lessons.",
            "focus": "смешение времён",
            "tip": "been [biːn], studying [ˈstʌdiɪŋ], finished [ˈfɪnɪʃt]"
        },
        {
            "text": "She was reading when he called. They had already left before I arrived at the station.",
            "focus": "Past Continuous и Past Perfect",
            "tip": "reading [ˈriːdɪŋ], arrived [əˈraɪvd]"
        },
    ],
    21: [
        {
            "text": "You ought to see a doctor. I might go to the cinema tonight if I finish early.",
            "focus": "ought to, might",
            "tip": "ought [ɔːt], might [maɪt] — тихое t в конце might"
        },
        {
            "text": "Could you help me with this? She need not worry about the test results.",
            "focus": "could, need not",
            "tip": "could [kʊd], worry [ˈwʌri]"
        },
    ],
    22: [
        {
            "text": "By the time I arrived, she had already left. He had been waiting for an hour.",
            "focus": "Past Perfect",
            "tip": "arrived [əˈraɪvd], waiting [ˈweɪtɪŋ]"
        },
        {
            "text": "They had been living in London for five years before they moved to Paris.",
            "focus": "Past Perfect Continuous",
            "tip": "living [ˈlɪvɪŋ], moved [muːvd]"
        },
    ],
    23: [
        {
            "text": "By next year I will have learned five hundred new words in English.",
            "focus": "Future Perfect",
            "tip": "learned [lɜːrnd], hundred [ˈhʌndrəd]"
        },
        {
            "text": "At this time tomorrow she will be flying to New York for a business trip.",
            "focus": "Future Continuous",
            "tip": "flying [ˈflaɪɪŋ], business [ˈbɪznɪs] — silent i"
        },
    ],
    24: [
        {
            "text": "First, I woke up early. Then, I had breakfast. Finally, I went to work.",
            "focus": "transition words",
            "tip": "finally [ˈfaɪnəli], breakfast [ˈbrekfəst] — break не как break!"
        },
        {
            "text": "Moreover, the weather was perfect. However, we decided to stay inside.",
            "focus": "moreover, however",
            "tip": "moreover [mɔːrˈoʊvər], however [haʊˈevər]"
        },
    ],
    25: [
        {
            "text": "Learning English is a piece of cake for her. I am on cloud nine after passing the test!",
            "focus": "idioms",
            "tip": "piece [piːs], cloud [klaʊd], nine [naɪn]"
        },
        {
            "text": "Let's break the ice with some introductions. Don't beat around the bush, tell me the truth!",
            "focus": "more idioms",
            "tip": "break [breɪk], bush [bʊʃ], truth [truːθ] — звук [θ]"
        },
    ],
}


def get_random_reading_text(lesson_num: int) -> Dict:
    """Получить случайный текст для аудио-урока."""
    texts = READING_TEXTS.get(lesson_num)
    if not texts:
        # Если нет текстов для этого урока — берём из ближайшего
        for n in range(lesson_num, 0, -1):
            texts = READING_TEXTS.get(n)
            if texts:
                break
        if not texts:
            texts = READING_TEXTS[1]
    return random.choice(texts)