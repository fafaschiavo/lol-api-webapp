from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import json, requests

# Create your procedures here.
def searchSummonnerId(summoner_name):
    api_key=settings.LOL_API_KEY
    region=settings.LOL_REGION

    summoner_name = summoner_name.lower()
    summoner_name = summoner_name.replace(" ", "")
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
    	return context
    except KeyError, e:
    	context['success'] = 0
    	return context




# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)

def getSummonerId(request):
    context = {}
    return render(request, 'getid.html', context)

def requestId(request):
    #receive data from the template
    template_form = request.POST['requestId']

    #Transform the data into string, then transform into lowercase and remove all the whitespaces
    summoner_name = str(template_form)
    context = searchSummonnerId(summoner_name)

    return render(request, 'requestid.html', context)

def getmatchhistory(request):
    context = {}
    return render(request, 'getmatchhistory.html', context)

def requestmatchhistory(request):
    #receive data from the template
    template_form = request.POST['requestmatchhistory']

    #Transform the data into string, then transform into lowercase and remove all the whitespaces
    summoner_name = str(template_form)
    context = searchSummonnerId(summoner_name)
    url = 'https://na.api.pvp.net/api/lol/' + settings.LOL_REGION + '/v2.2/matchlist/by-summoner/' + str(context['id']) + '?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    #print data['matches'][0]['matchId']

    for match in data['matches']:
    	context['match'+str(match['matchId'])] = match

    print context
    return render(request, 'requestmatchhistory.html', context)   


#get id by name:
#https://na.api.pvp.net/api/lol/br/v1.4/summoner/by-name/HelloKitter?api_key=93ecac97-49b3-4639-a4b8-51421bd89855

#get history by id:
#https://na.api.pvp.net/api/lol/br/v2.2/matchlist/by-summoner/412770?api_key=93ecac97-49b3-4639-a4b8-51421bd89855