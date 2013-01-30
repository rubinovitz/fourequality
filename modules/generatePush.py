def generatePushMsg(score):
	"""
	Write witty checkin reply
	"""
	scoreStr = str(score)
	prefix = "On a scale where 0 is the worst and 100 is the best, this venue has a HRC Corporate Equality score of "+scoreStr+"/100"
	if int(score) < 1:
		msg = prefix + " and therefore has a large-scale official or public anti-LGBT blemish on their recent records =/"
	
	elif 1 < score < 26:
		msg = prefix + ". They should try a bit harder next time."

	elif score == 50:
		msg = prefix + ". Halfway there?"

	elif score ==75:
		msg = prefix + ". Way to try!"

	elif score ==90:
		msg = prefix + ". Awesome!"

	elif score==100:
		msg = prefix + " which is perfect and we love them."
	
	else:
		msg = prefix + "."

	return msg
