from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name='index'),
	url(r'^geocode/', views.geocode_debug, name='geocode_debug'),
	url(r'^list/', views.list_events, name='list_events')
)