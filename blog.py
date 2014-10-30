"""
	A basic blog system built on Flask web framework.
	Credits for Mysql Wrapper: Kailash Nadh - http://nadh.in - https://github.com/knadh/simplemysql
	Foundation of the platform: Flaskr http://flask.pocoo.org/docs/0.10/tutorial/introduction/
	About the Flask framework: http://flask.pocoo.org

	License: GNU GPLv2

	Vishnu Sudhakaran, http://vishnus.name 
	October 30th, 2014

"""

import sqlite3, time
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from simplemysql import SimpleMysql  # mysql wrapper 

db = SimpleMysql(
	host="127.0.0.1",
	db="blog",
	user="root",
	passwd="",
	keep_alive=True
)


DEBUG = True  """ not to be used in production """
USERNAME = 'admin'
PASSWORD = 'default' 

"""
 Since single user, I kept the user details here, you can keep this in separate config file / database as well
"""
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_entries():
	""" Show all the entries - basic home page """
	cur = db.query("SELECT title, text, date, time FROM entries ORDER BY id DESC")
	entries = [dict(title=row[0], text=row[1], date=row[2], time=row[3]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	""" Add a new entry """
	if not session.get('logged_in'):
		abort(401)

	current_date = time.strftime("%B %d, %Y")
	current_time = time.strftime("%I:%M %p")
	db.insert("entries", {"title": request.form["title"], "text": request.form["text"], "date":current_date, "time": current_time });
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['POST', 'GET'])
def login():
	""" Login processing """
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid Username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Password'
		else:
			session['logged_in'] = True
			flash('You are logged in successfully')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	""" Session logout """
	session.pop('logged_in', None)
	flash('You are successfully logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()