import urllib
import urllib2
import json

def ajaxRequest(values=None, url=None):
	"""
	Makes an ajax request. If values == POST, if not == GET.

	values- data values (dict)
	url - endpoint(string)
	"""
	if values: #then POST
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
	else: #then GET
		req = urllib2.Request(url)
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	return response	
