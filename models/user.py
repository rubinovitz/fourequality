from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import csv
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('dbUrl')
db = SQLAlchemy(app)

class User(db.Model):
	"""
	A database class for each company
	"""
	__tablename__ = 'Users'
	id = db.Column(db.Integer, primary_key=True)
	userId = db.Column(db.String(30), unique=False,primary_key=True)
	oToken = db.Column(db.String(60), primary_key=True)

	def __init__(self, userId, oToken):
		self.userId = userId
		self.oToken = oToken

	def __repr__(self):
		return '<User %r>'  %self.userId
