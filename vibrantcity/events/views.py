from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from events.search import Events

import json

def index(request):
    # result = Events('DOID', 'asthm').find()
    # context = {'result': result}
    # return render(request, 'index.html', context)
    # res = Events().geocode_event_location('quebec city, canada')
    jsonstr = """[
				  {
				    "point": {"lon": 7.459717, "lat": 9.053277},
				    "title": "Nigeria",
				    "start": "2008-06-01",
				    "options": {
				      "theme": "TimeMapDataset.blueTheme()",
				      "description": "A protest over the price of water in Abuja results in violence."
				    }
				  },

				  {
				    "point": {"lon": 91.274414, "lat": 29.439598},
				    "title": "Tibet",
				    "start": "2008-07-15",
				    "options": {
				      "theme": "TimeMapDataset.redTheme()",
				      "description": "China launcheds a political crackdown in Tibet."
				    }
				  },

				  {
				    "point": {"lon": 71.474991, "lat": 34.163807},
				    "title": "Pakistan",
				    "start": "2008-10-19",
				    "options": {
				      "theme": "TimeMapDataset.blueTheme()",
				      "description": "The Taliban threaten to blow up Warsak Dam."
				    }
				  }
				]"""

    resp = StreamingHttpResponse(jsonstr, content_type='application/json')
    resp['Access-Control-Allow-Origin'] = '*'
    return resp

def geocode_debug(request):
	result = Events().geocode_event_location(request.GET['address'])
	result = json.loads(result)
	latlng = '%s,%s'%(result['lat'], result['lng'])
	return HttpResponse(latlng)