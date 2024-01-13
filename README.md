# RestApiApps

Основная цель данного приложения: Пользователь отправляет любой вопрос на сервер --> сервер возвращает наиболее "похожий вопрос:ответ" из БД (предварительно обучившись на данных из БД).

В данном приложении мною реализована RestApi модель, а также реализовано подробное описание с примером взаимодействия пользователя при помощи API на сервер.

Мой проект делится на две папки(части):
        - RestAPI (серверная часть)
        - test_unit (пользовательская часть)

        
Пользователь может направлять на сервер запросы следующего вида: 
        - Регистрация в приложении
        - Авторизация в приложении (содержащий логин и пароль для входа в наше приложение)
        - Вопрос от пользователя (использовано Машинное Обучение: Сервер получает вопрос от пользователя, далее производится вычисление растояния                                                                                 методом Жаккара, после чего выдается наиболее похожий "вопрос:ответ".)
        - Выход из сессии

На все запросы на сервер пользователь в ответ получает тип данных "object".


На серверной части реализована модель машинного обучения (файл ML.py), при запуске нашего приложения на сервере, при помощи библиотек NLTK производится предподготовка данных из БД, далее производится вычисление растояния методом Жаккара для того чтобы успешно отвечать на пользовательские вопросы,



Инструкция по запуску:
1) Необходимо создать базу данных
2) Запустить следующий код в ранеее созданной базе. Создаем таблицу вопрос-ответ, с колонками id, вопрос, ответ:

        CREATE TABLE public.answer_question (
        	id int4 NOT NULL,
        	question varchar NULL,
        	answer varchar NULL
        );
        
        -- Permissions
        
        ALTER TABLE public.answer_question OWNER TO postgres;
        GRANT ALL ON TABLE public.answer_question TO postgres;

3) Создаем или загружаем свои данные в созданную нами таблицу "answer_question".
   
4) Также необходимо создать таблицу пользователей, содержащая информацию логинов и паролей пользователей для доступа к данным приложения а также колонку активный аккаунт или нет. Администратор базы может выключать доступ пользователю отжав галочку в колонке "active", тем самым у пользователя пропадет доступ к данным и в ответ будет возвращаться текст "Авторизация не удалась" даже если пользователь ранее имел доступ к данным:

        CREATE TABLE public.users_1 (
        	id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
        	username varchar(50) NOT NULL,
        	passw varchar NOT NULL,
        	active bool NULL
        );
        CREATE UNIQUE INDEX username_1 ON public.users_1 USING btree (username);
        
        -- Permissions
        
        ALTER TABLE public.users_1 OWNER TO postgres;
        GRANT ALL ON TABLE public.users_1 TO postgres;
   
5) Программный код с папкой Rest_API распологаем на сервере
6) Программный код с папкой test_unit сохраняем на компьютере, откуда будем обращаться с запросом (для просмотра работы кода можно временно расположить папку на том же компьютере где находится папка RestAPI)
7) В файле "config1.json" в качестве ip нужно указать ip-адрес вашего сервера, в котором будет распологаться папка Rest_API
8) Необходимо установить пакеты из файла requirements.txt.
9) Запускаем файл "main.py"
10) Предподготовка данных закончена


Теперь нам нужно открыть файл "User_request_from_api.ipynb" 
и запустить каждый шаг по отдельности

