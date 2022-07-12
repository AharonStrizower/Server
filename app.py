from flask import Flask, render_template, url_for, redirect
from flask import request, session, jsonify
from datetime import timedelta
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
        if (user_info['email'] == email_to_check):
            return (user_info['email'])
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
