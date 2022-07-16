import random
from flask import Flask, redirect, render_template, request, session
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import time
import requests
import asyncio
import aiohttp
import json
import collections

app = Flask(__name__)
app.secret_key = '13579'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

from pages.assignment_4.assignment_4 import assignment_4

app.register_blueprint(assignment_4)


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


@app.route('/search')
def search_page():
    return redirect("https://www.google.com")


@app.route('/')
def main_page():
    return redirect(url_for('home_page'))


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/assignment3_1')
def display_hobbies_page():
    user_name = 'Aharon'
    hobby1 = 'sports'
    hobby2 = 'TRAveling'
    hobby3 = ''
    return render_template('assignment3_1.html',
                           user_name=user_name,
                           hobby1=hobby1,
                           hobby2=hobby2,
                           hobby3=hobby3,
                           artists=['Coldplay', 'Ed Sheeran', 'Passenger'])


@app.route('/friends')
def friends_page():
    return render_template('friends.html')


def check_email(email_to_check):
    for user_num, user_info in users.items():
        if user_info['email'] == email_to_check:
            return user_info['name'], user_info['email']
    return False


# define a users dict
users = {'user1': {'name': 'Dana', 'email': 'dana123@gmail.com'},
         'user2': {'name': 'Noam', 'email': 'noam456@gmail.com'},
         'user3': {'name': 'Lior', 'email': 'lior789@gmail.com'},
         'user4': {'name': 'Hadar', 'email': 'hadar246@gmail.com'},
         'user5': {'name': 'Alon', 'email': 'alon697@gmail.com'},
         'user6': {'name': 'Guy', 'email': 'guy846@gmail.com'}}


@app.route('/assignment3_2', methods=['GET', 'POST'])
def users_page():
    if request.method == 'GET':
        if 'user_email' in request.args:
            if check_email(request.args['user_email']):
                user_email = check_email(request.args['user_email'])
                return render_template('assignment3_2.html', user_email=user_email)
        return render_template('assignment3_2.html', users=users)
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        session['user_name'] = user_name
        session['logged_in'] = True
    return render_template('assignment3_2.html')


@app.route('/assignment_4/users')
def assignment_4_users():
    objects_dict = {}
    query = "select * from users"
    query_result = interact_db(query, query_type='fetch')
    for user in query_result:
        objects_dict[f'user_{user.id}'] = {
            'name': user.name,
            'email': user.email,
        }
    return jsonify(objects_dict)


def get_user(id_num):
    user = requests.get(f' https://reqres.in/api/users/{id_num}')
    user = user.json()
    return user


@app.route('/assignment_4/outer_source', methods=['GET', 'POST'])
def assignment_4_outer_source():
    if request.method == 'POST':
        id_num = request.form['id']
        user = get_user(id_num)
        return render_template('assignment_4_outer_source.html', user=user)
    return render_template('assignment_4_outer_source.html')


@app.route('/assignment_4/restapi_users', defaults={'user_id': 2})
@app.route('/assignment_4/restapi_users/<int:user_id>', methods=['GET', 'POST'])
def get_users_func(user_id):
    query = 'select * from users where id=%s;' % user_id
    users = interact_db(query=query, query_type='fetch')
    if len(users) == 0:
        return_dict = {
            'status': 'failed',
            'message': 'user not found'
        }
    else:
        return_dict = {
            'id': users[0].id,
            'name': users[0].name,
            'email': users[0].email,
        }
    return jsonify(return_dict)


@app.route('/logout')
def log_out():
    session.clear()
    session['user_name'] = ""
    session['logged_in'] = False
    return redirect(url_for('users_page'))


@app.route('/session')
def session_func():
    return jsonify(dict(session))


if __name__ == '__main__':
    app.run(debug=True)
