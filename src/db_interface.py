from src import app
from sqlite3 import dbapi2 as sqlite3
from flask import g, redirect, url_for, abort, flash, _app_ctx_stack

def init_db():
    #Creates the database tables.
    with app.app_context():
        db = get_db()
        with app.open_resource('db.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    #Opens a new database connection if there is none yet for the
    #current application context.
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return top.sqlite_db


@app.teardown_appcontext
def close_db_connection(exception):
    #Closes the database again at the end of the request.
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def show_entries():
	db = get_db()
	cur = db.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

def user_exist(email):
	db = get_db()
	cur = db.cursor()
	cur.execute('select id from users where email = ?', [email[0]])
	if len(cur.fetchall()) == 0:
		#Add user to database
		user_id = [add_user(email)]
		print user_id
		return user_id
	else:
		print cur.fetchall()
		return [row[0] for row in cur.fetchall()]

def add_email_message(email):
	db = get_db()
	db.execute('insert into emails (from_user_id, to_user_id, subject, datetime) values (?, ?, ?, ?)', [email['From'], email['TO'], email['Subject'], email['Received']])
	db.commit()
	return email#Still trying to figure out what the command for returning the whole last insert is, this will do for now.

def check_email_exists(email):
	db = get_db()
	cur = db.execute('select id from emails where from_user_id = ? AND to_user_id = ? AND datetime = ?', [email['From'],email['To'],email['Received']])
	if cur is None:
		return False
	else:
		return True
	
def add_user(data):
	db = get_db()
	cur = db.cursor()
	cur.execute('insert into users (name, email) values (?, ?)', [data[1], data[0]])
	cur.commit()
	return cur.lastrowid
