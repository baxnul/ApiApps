import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.metrics import jaccard_distance
from cdifflib import CSequenceMatcher
from DB import get_db_connection

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


# Функция для предварительной обработки текста
def preprocess_text(text):
    # Приведение к нижнему регистру
    text = text.lower()
    # Токенизация текста
    tokens = word_tokenize(text)
    # Удаление стоп-слов
    stop_words = set(stopwords.words('english', 'russian'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # Лемматизация токенов
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    # Определение частей речи токенов
    tagged_tokens = pos_tag(lemmatized_tokens)
    # Формирование нового текста из лемматизированных и помеченных токенов
    processed_text = ' '.join([token[0] + '_' + token[1] for token in tagged_tokens])

    return processed_text


conn = get_db_connection()
cur = conn.cursor()

# Выборка всех вопросов из базы данных
cur.execute("select aq.question ,aq.answer from answer_question aq")
rows = cur.fetchall()

# Создание списка вопросов и ответов
questions = []
answers = []

# Предварительная обработка и добавление вопросов и ответов в списки
for row in rows:
    question = preprocess_text(row[0])
    answer = row[1]
    questions.append(question)
    answers.append(answer)

# Закрытие соединения с базой данных
cur.close()
conn.close()


# Функция для поиска наиболее похожего вопроса и вывода ответа
def find_most_similar_question(input_question):
    # Предварительная обработка входного вопроса
    processed_input_question = preprocess_text(input_question)

    # Вычисление сходства между вопросами и входным вопросом
    similarities = [jaccard_distance(set(processed_input_question.split('_')), set(question.split('_'))) for
                    question in questions]

    # Нахождение индекса наиболее похожего вопроса
    most_similar_index = similarities.index(min(similarities))
    print("Схожесть вопроса в %:", CSequenceMatcher(None, input_question, rows[most_similar_index][0]).ratio())

    # Вывод вопроса и ответа наиболее похожего вопроса
    print("Похожий вопрос:", rows[most_similar_index][0])
    print("Ответ:", rows[most_similar_index][1])
    return "Вопрос: " + rows[most_similar_index][0], "Ответ: " + rows[most_similar_index][1]
