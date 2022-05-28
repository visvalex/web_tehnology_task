# -*- coding: utf-8 -*-
# Подключаем объект приложения Flask из __init__.py
from labapp import app
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for
from . import dbservice    # подключение модуля с CRUD-методами для работы с БД из локального пакета
import functools
"""

    Модуль регистрации маршрутов для запросов к серверу, т.е.
    здесь реализуется обработка запросов при переходе пользователя на определенные адреса веб-приложения

"""

# Структура основного навигационнго меню веб-приложения,
# оформленное в виде массива dict-объектов
navmenu = [
    {
        'name': 'Главная',
        'addr': '/main'
    },
    {
        'name': 'О школе',
        'addr': '/school'
    },
    {
        'name': 'Ученикам',
        'addr': '/students'
    },
    {
        'name': 'Курсы',
        'addr': '/kurs'
    },
    {
        'name': 'Контакты',
        'addr': '#'
    },
]

# Функция-декоратор для проверки авторизации пользователя
def login_required(route_func):
    @functools.wraps(route_func)
    def decorated_route(*args, **kwargs):
        # Если не установлен параметр сессии user или значение cookie 'AuthToken' не равно логину пользователя
        if not session.get('user') or request.cookies.get('AuthToken') != session.get('user'):
            # перенаправляем на страницу авторизации
            return redirect(url_for('login'))
        return route_func(*args, **kwargs)
    return decorated_route


# Обработка запроса к индексной странице
@app.route('/')
@app.route('/main')
def main():
    # "рендеринг" (т.е. вставка динамически изменяемых данных) index.html и возвращение готовой страницы
    return render_template('main.html', title='Visvalex', pname='Главная', navmenu=navmenu)

@app.route('/school')
def school():
    return render_template('school.html', title='Visvalex', pname='О школе', navmenu=navmenu)

@app.route('/students')
def students():
    return render_template('students.html', title='Visvalex', pname='Ученикам', navmenu=navmenu)

@app.route('/kurs')
@login_required
def kurs():
    return render_template('kurs.html', title='Visvalex', pname='Курсы', navmenu=navmenu)

# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если POST-запрос
    if request.method == 'POST':
        # если нажата кнопка "Зарегистрировать", переадресуем на страницу регистрации
        if request.form.get('regBtn') == 'true':
            return redirect(url_for('register'))
        # иначе запускаем авторизацию по данным формы
        else:
            return dbservice.login_user(request.form)
    else:
        return render_template('login.html', title='Visvalex', navmenu=navmenu)

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Если POST-запрос, регистрируем нового пользователя
    if request.method == 'POST':
        return dbservice.register_user(request.form)
    else:
        return render_template('register.html', title='Visvalex', navmenu=navmenu)

"""

    Реализация обработчиков маршрутов (@app.route) REST API для модели ContactRequest (см. models.py).
    Обработчики маршрутов вызывают соответствующие HTTP-методам CRUD-операции из контроллера (см. dbservice.py)

"""
@app.route('/apii/contactrequest', methods=['GET'])
def get_previous_requests():
    previous = dbservice.get_previous_requests()
    return json_response(previous)

@app.route('/api/contactrequest', methods=['GET'])
# Получаем все записи contactrequests из БД
def get_contact_req_all():
    response = dbservice.get_contact_req_all()
    return json_response(response)


@app.route('/api/contactrequest/<int:id>', methods=['GET'])
# Получаем запись по id
def get_contact_req_by_id(id):
    response = dbservice.get_contact_req_by_id(id)
    return json_response(response)


@app.route('/api/contactrequest/author/<string:firstname>', methods=['GET'])
# Получаем запись по имени пользователя
def get_get_contact_req_by_author(firstname):
    if not firstname:
        # то возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
        # Иначе отправляем json-ответ
    else:
        response = dbservice.get_contact_req_by_author(firstname)
    return json_response(response)

 #Обработка POST-запроса для демонстрации AJAX
#@app.route('/api/contactrequest', methods=['POST'])
#def post_contact():
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в этом объекте нет, например, обязательного поля 'firstname'
#    if not request.json or not 'firstname' in request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
#        return bad_request()
    # Иначе отправляем json-ответ
 #   else:
#        msg = request.json['firstname'] + ", ваш запрос получен !";
  #      return json_response({ 'message': msg })

@app.route('/api/contactrequest', methods=['POST'])
# Обработка запроса на создание новой записи в БД
def create_contact_req():
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в данных нет обязательного поля 'firstname' или 'reqtext'
    if not request.json or not 'firstname' or not 'email' in request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе добавляем запись в БД отправляем json-ответ
    else:
        response = dbservice.create_contact_req(request.json)
        return json_response(response)


@app.route('/api/contactrequest/<int:id>', methods=['PUT'])
# Обработка запроса на обновление записи в БД
def update_contact_req_by_id(id):
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в данных нет обязательного поля 'reqtext'
    if not request.json or not 'email' in request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе обновляем запись в БД и отправляем json-ответ
    else:
        response = dbservice.update_contact_req_by_id(id, request.json)
        return json_response(response)


@app.route('/api/contactrequest/<int:id>', methods=['DELETE'])
# Обработка запроса на удаление записи в БД по id
def delete_contact_req_by_id(id):
    response = dbservice.delete_contact_req_by_id(id)
    return json_response(response)



"""

    Реализация response-методов, возвращающих клиенту стандартные коды протокола HTTP

"""

# Возврат html-страницы с кодом 404 (Не найдено)
@app.route('/notfound')
def not_found_html():
    return render_template('404.html', title='404', err={ 'error': 'Not found', 'code': 404 })

# Формирование json-ответа. Если в метод передается только data (dict-объект), то по-умолчанию устанавливаем код возврата code = 200
# В Flask есть встроенный метод jsonify(dict), который также реализует данный метод (см. пример метода not_found())
def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))

# Пример формирования json-ответа с использованием встроенного метода jsonify()
# Обработка ошибки 404 протокола HTTP (Данные/страница не найдены)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)

# Обработка ошибки 400 протокола HTTP (Неверный запрос)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)


