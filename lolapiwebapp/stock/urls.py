from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getid/$', views.getSummonerId, name='getSummonerId'),
    url(r'^getid/requestid/$', views.requestId, name='requestId'),
    url(r'^getmatchhistory/$', views.getmatchhistory, name='getmatchhistory'),
    url(r'^getmatchhistory/requestmatchhistory/$', views.requestmatchhistory, name='requestmatchhistory'),
    url(r'^getcurrentgame/$', views.getcurrentgame, name='getcurrentgame'),
    url(r'^getcurrentgame/requestcurrentgame/$', views.requestcurrentgame, name='requestcurrentgame'),
]