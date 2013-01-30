from flask import Flask, redirect, url_for, request, render_template, send_from_directory
from werkzeug import SharedDataMiddleware, secure_filename
import os
import pyfoursquare as foursquare
from pyfoursquare import OAuthHandler, FoursquareError
import json
from models.company import Company
from models.user import User
from modules.generatePush import * 
from modules.ajaxRequest import *
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv('secretKey')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('dbUrl')
db = SQLAlchemy(app)

@app.route('/')
def index():
	"""
	Render homepage
	"""
	return render_template('index.html')

@app.route('/handlepush', methods=['POST'])
def handlepush():
	"""
	Handles push notifications from Foursquare checkins
	"""
	# get the checkin json	
	data =  request.form['checkin']
  # make the checkin json parseable by python
	pushData = json.loads(data)	
	# get userId
	userId = pushData['user']['id']
	# get the checkinId to use for our reply
	checkinId = pushData['id'] 
	# get user object by id from database	
	user = User.query.filter_by(userId=userId)[0]
	# get user's oauth token
	userOToken = user.oToken
	# get the venue name from the push data and make it lc to match db
	venueName = pushData['venue']['name'].lower()
	# get the first letter of the venue name
	venueFirstLetter = venueName[0]
	#get all companies with the same first letter as checkin venue
	companyChoices = Company.query.filter_by(firstLetter=venueFirstLetter).all()
	
	score = False #start with no score
	for company in companyChoices: # for all companies starting with venue's first letter
					if company.name.strip() in venueName: # if the company name is a substring of the venue name
									score = company.score # that is the score
									break
	# if a score was found
	if score:
		# get the push message for that given score
		postMsg = generatePushMsg(int(score))
		url = 'https://api.foursquare.com/v2/checkins/'+checkinId+'/reply'
		values = {'text':postMsg, 'CHECKIN_ID':str(checkinId), 'oauth_token':userOToken}
		# post reply to reply endpoint
		postReply = ajaxRequest(values, url)

	# return 200 status to foursquare
	return 'hi foursquare'

@app.route('/callback', methods=['GET','POST'])
def callback():
	"""
	Foursquare calls this URL with our OAuth token. Get the token, get the userId, save them both in our database.
	"""
	verifier = request.args['code']
	clientId = os.getenv('clientId')
	clientSecret = os.getenv('clientSecret')
	callback = os.getenv('callback')
	# use callback code for oauth
	oauth = OAuthHandler(clientId, clientSecret, callback)
	# get the access token and store
	try:
		oauth.get_access_token(verifier)
	except FoursquareError:
		print 'Error, failed to get access token'
	oToken = oauth.access_token
	url='https://api.foursquare.com/v2/users/self?oauth_token='+str(oToken)
	# convert user information json to python dictionary
	userInfo = json.loads(ajaxRequest(url=url))
	userId= userInfo['response']['user']['id'] 
 	# create user model for db
	user= User(userId, oToken)
	# add user model
	db.session.add(user)
	# commit db model
	db.session.commit()	
	return render_template('callback.html')

@app.route('/oauth')
def oauth():
	"""
	Call the Foursquare Oauth url with our credentials so it can send /callback a token
	"""
	clientId = os.getenv('clientId')
	clientSecret = os.getenv('clientSecret')
	callback = os.getenv('callback')
	# call auth endpoint
	oauth = foursquare.OAuthHandler(clientId, clientSecret, callback)
	authUrl = oauth.get_authorization_url()
	# redirect to foursquare auth
	return redirect(authUrl) # redirect to foursquare oauth

@app.errorhandler(404)
def page_not_found(e):
	"""
	404 error, for now we go back to the index template
	"""
	return render_template('index.html')

# store static files on server for now
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
'/': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__' and os.getenv('environ')=='production':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

elif __name__ == '__main__' and os.getenv('environ')=='dev':
	app.run(port=8000, debug=True)
