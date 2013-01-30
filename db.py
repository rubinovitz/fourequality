from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

def createHerokuDb():
	"""
	Import this function and the database models into 'heroku run python' to create database on heroku
	"""
		app = Flask(__name__)
		app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['dbUrl']
		db = SQLAlchemy(app)
		db.create_all()
