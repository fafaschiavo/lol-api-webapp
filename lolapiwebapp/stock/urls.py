from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getid/$', views.getSummonerId, name='getSummonerId'),
    url(r'^getid/requestid/$', views.requestId, name='requestId'),
]