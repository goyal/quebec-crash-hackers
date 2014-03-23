from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from events.search import Events

import requests
import json

def index(request):
    return HttpResponse('test')

def geocode_debug(request):
	result = Events().geocode_event_location(request.GET['address'])
	result = json.loads(result)
	latlng = '%s,%s'%(result['lat'], result['lng'])
	return HttpResponse(latlng)

def list_events(request):
    result = requests.get('http://107.170.117.164:8890/sparql?default-graph-uri=&query=select+%3Fdd+%3Fle+%3Fla+%3Flo%0D%0Awhere+%7B%0D%0A%3Fa+rdfs%3Alabel+%3Fle+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FDateDebut%3E+%3Fdd+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxLieu%3E+%3Fl+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FLatitude%3E+%3Fla+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FLongitude%3E+%3Flo+.%0D%0AFILTER%28regex%28%3Fdd%2C%272014-03%27%29%29.%0D%0A%7D+%0D%0Aorder+by+1+2+3+4%0D%0A&format=json&timeout=0&debug=on')
    responseJson = result.json()
    events = []
    data = responseJson.get('results')
    bindings = data.get('bindings')

    for binding in bindings:
        events.append(dict(
		    point = dict(lon=float(binding['lo']['value']), lat=float(binding['la']['value'])),
		    title = binding['le']['value'],
		    start = binding['dd']['value'],
		    options = dict(theme='TimeMapDataset.blueTheme()', description='<strong>bla</strong>')
		    ))

    resp = StreamingHttpResponse(json.dumps(events), content_type='application/json')
    resp['Access-Control-Allow-Origin'] = '*'
    return resp