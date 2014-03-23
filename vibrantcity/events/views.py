from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from events.search import Events

import requests
import json

def index(request):
    search_param = ""
    try:
        search_param = request.GET['param']
    except Exception:
        search_param = ""
    return render(request, "index.html", {'key':search_param})

def geocode_debug(request):
	result = Events().geocode_event_location(request.GET['address'])
	result = json.loads(result)
	latlng = '%s,%s'%(result['lat'], result['lng'])
	return HttpResponse(latlng)

def list_events(request):
    url = 'http://107.170.117.164:8890/sparql?default-graph-uri=&query=select+distinct+%3Fa+%3Fsc+%3Fc+%3Fdd+%3Fdf+%3Fla+%3Fll+%3Fadr+%3Flat+%3Flo%0D%0Awhere+{%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FDateDebut%3E+%3Fdd+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FDateFin%3E+%3Fdf+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxCategorie%3E+%3Fc+.%0D%0A%3Fa+rdfs%3Alabel+%3Fla+.%0D%0A%3Fc+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxSuperCategorie%3E+%3Fsc+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxLieu%3E+%3Fl+.%0D%0A%3Fl+rdfs%3Alabel+%3Fll+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FAdresse%3E+%3Fadr+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FLatitude%3E+%3Flat+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FLongitude%3E+%3Flo+.%0D%0AFILTER%28regex%28%3Fdd%2C%272014-04%27%29%29.%0D%0A}%0D%0Aorder+by+1+2+3+4&format=application%2Fsparql-results%2Bjson&timeout=0&debug=on'

    search_param = request.GET['param']
    print "Search params"
    print search_param;
    if len(search_param) != 0:
        url = 'http://107.170.117.164:8890/sparql?default-graph-uri=&query=select+distinct+%3Fa+%3Fsc+%3Fc+%3Fdd+%3Fdf+%3Fla+%3Fll+%3Fadr+%3Flat+%3Flo%0D%0Awhere+{%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FDateDebut%3E+%3Fdd+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FDateFin%3E+%3Fdf+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxCategorie%3E+%3Fc+.%0D%0A%3Fa+rdfs%3Alabel+%3Fla+.%0D%0A%3Fa+%3Fp+%3Fo+.%0D%0A%3Fc+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxSuperCategorie%3E+%3Fsc+.%0D%0A%3Fa+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FxLieu%3E+%3Fl+.%0D%0A%3Fl+rdfs%3Alabel+%3Fll+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FAdresse%3E+%3Fadr+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FLatitude%3E+%3Flat+.%0D%0A%3Fl+%3Chttp%3A%2F%2Fdonnees.ville.qc.ca%2FLongitude%3E+%3Flo+.%0D%0AFILTER%28bif%3Acontains%28%3Fo%2C%22%27__search_param__%27%22%29%29.%0D%0A}%0D%0Aorder+by+1+2+3+4&format=application%2Fsparql-results%2Bjson&timeout=0&debug=on'
        url = url.replace('__search_param__',search_param)
        print url

    #print url
    result = requests.get(url)
    #print result.text
    responseJson = result.json()
    #print responseJson
    events = []
    data = responseJson.get('results')
    bindings = data.get('bindings')
    for binding in bindings:
        events.append(dict(
		    point = dict(lon=float(binding['lo']['value']), lat=float(binding['lat']['value'])),
		    title = binding['la']['value'],
		    start = binding['dd']['value'],
		    #end = binding['df']['value'] if binding['df']['value'] != binding['dd']['value'] else "",
		    options = dict(theme='TimemapDataset.blueTheme()', description='%s - %s<br/>%s - <a href=http://107.170.117.164:8890/describe/?url=%s>Lien vers l&#146;&eacute;v&egrave;nement</a>'%(binding['ll']['value'],binding['adr']['value'],binding['dd']['value'],binding['a']['value']))
		    ))

    resp = StreamingHttpResponse(json.dumps(events), content_type='application/json')
    resp['Access-Control-Allow-Origin'] = '*'
    return resp