import requests
import json

BASE_URL = 'http://mobile.bio2rdf.org/ontobee/search_ns/json-ld?'

BASE_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=true&key=AIzaSyAiISY5HzTcu7eMGB9_zefJtR-8eqenBfw'

class EventLocation:
	Montreal = 0
	Quebec = 1
	Sherbrook = 2

class Events:
	def __init__(self, location = '', keyword = ''):
		self.location = location
		self.keyword = keyword

	def find(self):
		url = '%sparm2=%s&parm1=%s'%(BASE_URL, self.location, self.keyword)
		print 'Searching for events: ' + url
		response = requests.get(url);
		# geolocation = self.geocode_event_location('Quebec city, canada');
		return response.json();

	def geocode_event_location(self, address):
		url = '%s&address=%s'%(BASE_GEOCODE_URL, address)
		response = requests.get(url).json();

		# check if the status is ok
		if response['status'] == 'OK':
			data = response['results'][0]['geometry']['location']
			data = dict(lat = data['lat'], lng = data['lng'])
			return json.dumps(data)
		else:
			print 'Failed to geocode address: %s'%(address)
			return {}