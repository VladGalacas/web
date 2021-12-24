from flask import Flask, render_template, request, redirect, abort
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    return connection


def query_introduction(insert_query):
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()


def users_list():
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = connection.cursor()
    result = None
    cursor.execute('SELECT * FROM users')
    result = cursor.fetchall()
    total = []
    for user in result:
        user = list(user)
        total1 = []
        for val in user:
            total1.append(val.strip())
        total.append(total1)
        user_list = []
    for val in total:
        user_list.append(
            {'username': val[0] + val[1], 'name': val[0], 'surname': val[1], 'telephone': val[2], 'age': val[3]})
    return user_list


def check_for_presence_in_db(value):
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = connection.cursor()
    result = None
    cursor.execute('SELECT * FROM users')
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    total = []
    for user in result:
        user = list(user)
        total1 = []
        for val in user:
            total1.append(val.strip())
        total.append(total1)
    for st in total:
        if ' '.join(st) == value:
            return True
    return False


app = Flask(__name__)


@app.route('/', methods=['get'])
def index():
    return render_template('index.html')


@app.route('/name/<name>', methods=['get'])
def name_page(name):
    return render_template('index.html', username=name)


@app.route('/users', methods=['get', 'post'])
def users():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        telephone = request.form.get('telephone')
        age = request.form.get('age')
        if not check_for_presence_in_db(f'{name} {surname} {telephone} {age}'):
            insert_query = (
                f"INSERT INTO users (name, surname, telephone, age) VALUES ('{name}', '{surname}', '{telephone}', '{age}')")
            query_introduction(insert_query)
    return render_template('users.html', users=users_list())


@app.route('/')
def index1():
    return redirect('/users')


@app.route('/users/<username>')
def check(username):
    flag = False
    for i in users_list():
        if username == i['username']:
            flag = True
            users = i
    if not flag:
        abort(505)

    return f'<h2>UserName:{users["username"]} </h2> <br>' \
           f'<h2>Name:{users["name"]} </h2> <br>' \
           f'<h2>Surname:{users["surname"]} </h2> <br>' \
           f'<h2>Telephone:{users["telephone"]} </h2> <br>' \
           f'<h2>Age:{users["age"]} </h2> <br>'


@app.route('/users/<username>/del')
def delete_user(username):
    flag = False
    for i in users_list():
        if username == i['username']:
            flag = True
            users = i
    if not flag:
        abort(505)
    insert_query = (
        f"DELETE FROM users WHERE name='{users['name']}' AND surname='{users['surname']}' AND telephone='{users['telephone']}' AND age='{users['age']}'")
    query_introduction(insert_query)
    return redirect('/users')


@app.route('/users/<username>/update', methods=['get', 'post'])
def update_user(username):
    flag = False
    for i in users_list():
        if username == i['username']:
            flag = True
            users = i
    if not flag:
        abort(505)
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        telephone = request.form.get('telephone')
        age = request.form.get('age')
        flag = True
        for i in users_list():
            if name + surname == i['username']:
                flag = False
                abort(404)
        if flag:
            insert_query = (
                f"UPDATE users SET name='{name}', surname='{surname}', telephone='{telephone}', age='{age}' WHERE name='{users['name']}' AND surname='{users['surname']}' AND telephone='{users['telephone']}' AND age='{users['age']}'")
            query_introduction(insert_query)
    return render_template('update_user.html')


if __name__ == '__main__':
    app.run(debug=True)
