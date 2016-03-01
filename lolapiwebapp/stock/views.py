from django.shortcuts import render
from django.http import HttpResponse
import json, requests

# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)

def getSummonerId(request):
    context = {}
    return render(request, 'getid.html', context)

def requestId(request):
    template_form = request.POST['requestId']
    summoner_name = str(template_form)

    api_key='93ecac97-49b3-4639-a4b8-51421bd89855'
    region='br'
    
    url = 'https://na.api.pvp.net/api/lol/'+ region +'/v1.4/summoner/by-name/'+ summoner_name +'?api_key=' + api_key
    
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    context = {}

    try:
    	context['success'] = 1
    	context['summonerName'] = summoner_name
    	context['summonerLevel'] = data[summoner_name]['summonerLevel']
    	context['id'] = data[summoner_name]['id']
    	context['profileIcon'] = data[summoner_name]['profileIconId']
    	print context
    	print url
    	return render(request, 'requestid.html', context)
    except KeyError, e:
    	context['success'] = 0
    	return render(request, 'requestid.html', context)


#https://na.api.pvp.net/api/lol/br/v1.4/summoner/by-name/HelloKitter?api_key=93ecac97-49b3-4639-a4b8-51421bd89855