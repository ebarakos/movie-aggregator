from django.conf.urls import url, patterns,include
from backend import views

urlpatterns = patterns(
	url(r'^backend/', views.now_playing),
	url(r'^now_playing/', views.now_playing),
	url(r'^search/(?P<query>[^/]+)/$', views.search)
)
