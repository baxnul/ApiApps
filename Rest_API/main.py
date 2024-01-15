from flask import Flask, session, Response, request, jsonify
from DB import get_usr_list, get_db_connection
from ML import find_most_similar_question
from datetime import timedelta
import hashlib

app = Flask(__name__)
app.secret_key = "\2\1thisismyscretkey\1\2\e\y\y\h"
app.permanent_session_lifetime = timedelta(minutes=180)


@app.route('/')
def hello_world():
    return 'Hello, world!'


@app.route('/api/data', methods=['GET'])
def handle_data() -> Response:
    if "user" in session:
        # username = session["user"]
        inputted_json = request.get_json()  # Получаем данные в формате JSON из запроса
        question = inputted_json['question']
        # Обрабатываем данные
        processed_data = find_most_similar_question(question)
        # print(processed_data)
        # Возвращаем обработанные данные в формате JSON
        return jsonify(processed_data)
    else:
        return jsonify("Авторизуйтесь на платформе")


@app.route("/registration", methods=['GET', 'POST'])
def registration() -> Response:
    try:
        inputted_json = request.get_json()
        print(inputted_json)
        new_user_login = inputted_json['login']
        psw = inputted_json['psw']
        hashed_password = hashlib.sha256(psw.encode('utf-8')).hexdigest()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users_1 (username, passw, active) VALUES (%s, %s, True)",
                    (str(new_user_login), str(hashed_password)))  # hashed_password
        conn.commit()
        cur.close()
        conn.close()
        return jsonify("Вы успешно зарегистрированы")
    except:
        return jsonify("Такой пользователь уже существует")


@app.route("/login", methods=['GET'])
def login() -> Response:
    try:
        inputted_json = request.get_json()
        users_inp = inputted_json['nm']
        password = inputted_json['psw']
        users_db = get_usr_list()
        for usr in users_db:  # в user_db пользователи из БД (словарь)
            # print("usr", usr)
            # print(list(usr['password']).join[2:-1], password)
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # шифруем пароль в sha-256
            if usr['login'] == users_inp and usr['password'] == hashed_password:
                print('Пароль верный')
                session.permanent = True
                session["user"] = users_inp
                return jsonify('Вы успешно авторизованы', session["user"])
        print(str(users_inp) + ' авторизация не удалась')
        return jsonify('Авторизация не удалась')
    except KeyError:
        return jsonify('Авторизация не удалась')


@app.route("/logout")
def logout() -> Response:
    if "user" in session:
        username = session["user"]
        session.pop("user", None)
        print(str(username) + ' завершил сессию')
        return jsonify('Сессия успешно завершилась')
    else:
        return jsonify('Проверьте правильность ввода данных для входа в систему')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
