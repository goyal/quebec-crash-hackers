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
    result = requests.get('http://107.170.117.164:8890/sparql?default-graph-uri=&query=select+distinct+%3Fa+%3Fsc+%3Fc+%3Fdd+%3Fdf+%3Fla+%3Fll+%3Fadr+%3Flat+%3Flo%0D%0Awhere+{%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FDateDebut%3E+%3Fdd+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FDateFin%3E+%3Fdf+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxCategorie%3E+%3Fc+.%0D%0A%3Fa+rdfs%3Alabel+%3Fla+.%0D%0A%3Fc+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxSuperCategorie%3E+%3Fsc+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxLieu%3E+%3Fl+.%0D%0A%3Fl+rdfs%3Alabel+%3Fll+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FAdresse%3E+%3Fadr+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FLatitude%3E+%3Flat+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FLongitude%3E+%3Flo+.%0D%0AFILTER%28bif%3Acontains%28%3Fla%2C%22Mise%22%29%29.%0D%0A}%0D%0Aorder+by+1+2+3+4&format=application%2Fsparql-results%2Bjson&timeout=0&debug=on')
    responseJson = result.json()
    events = []
    data = responseJson.get('results')
    bindings = data.get('bindings')

    for binding in bindings:
        events.append(dict(
		    point = dict(lon=float(binding['lo']['value']), lat=float(binding['lat']['value'])),
		    title = binding['la']['value'],
		    start = binding['dd']['value'],
		    #end = binding['df']['value'] if binding['df']['value'] != binding['dd']['value'] else "",
		    options = dict(theme='TimemapDataset.blueTheme()', description='%s - %s<br/><a href=http://107.170.117.164:8890/describe/?url=%s>Lien vers l&#146;&eacute;v&egrave;nement</a>'%(binding['ll']['value'],binding['adr']['value'],binding['a']['value']))
		    ))

    resp = StreamingHttpResponse(json.dumps(events), content_type='application/json')
    resp['Access-Control-Allow-Origin'] = '*'
    return resp