from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import csv
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('dbUrl')
db = SQLAlchemy(app)

class Company(db.Model):
	"""
	A database class for each company
	"""
	__tablename__ = 'Company'
	id = db.Column(db.Integer, primary_key=True)
	firstLetter = db.Column(db.String(1), unique=False,primary_key=True)
	name = db.Column(db.String(120), unique=True, primary_key=True)
	score = db.Column(db.Integer, primary_key=True)

	def __init__(self, firstLetter, name, score):
		self.firstLetter = firstLetter
		self.name = name
		self.score = score


