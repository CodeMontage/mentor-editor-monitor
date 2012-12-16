#from __future__ import with_statement #<-necessary if server uses python 2.5
from flask import Flask, request, render_template
import os, sys, email_fetch, db_interface
from contextlib import closing
from src import app

#app = Flask(__name__)
app.config.from_object('monitor_app_config')

@app.route("/")
def main():
	emails = email_fetch.get_messages()
	return render_template('messages.html', msg=emails)


if __name__ == "__main__":
    app.run(debug=True)