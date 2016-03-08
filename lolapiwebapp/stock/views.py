from pprint import pprint
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

def searchHeroName(championId):
    api_key=settings.LOL_API_KEY
    region=settings.LOL_REGION
    
    championId = str(championId)
    url = 'https://na.api.pvp.net/api/lol/static-data/'+ region +'/v1.2/champion/'+ championId +'?api_key=' + api_key
    resp = requests.get(url=url)
    try:
        data = json.loads(resp.text)
        return data['name']
    except ValueError:
        return championId



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
    summoner_info = searchSummonnerId(summoner_name)
    context = {}
    context['summoner_name'] = summoner_name

    try:
        url = 'https://na.api.pvp.net/api/lol/' + settings.LOL_REGION + '/v2.2/matchlist/by-summoner/' + str(summoner_info['id']) + '?api_key=' + settings.LOL_API_KEY
        resp = requests.get(url=url)
        data = json.loads(resp.text)

        context['header'] = []
        context['header'].append('Lane')
        context['header'].append('Champion')
        context['header'].append('Season')
        context['header'].append('Match ID')
        context['header'].append('Duration')

        context['matches'] = []
        match_data_to_context = []
        for match in data['matches']:
            match_data_to_context = []
            match_data_to_context.append(match['lane'])
            match_data_to_context.append(match['champion'])
            match_data_to_context.append(match['season'])
            match_data_to_context.append(match['matchId'])
            match_data_to_context.append(match['timestamp'])
            context['matches'].append(match_data_to_context)

        return render(request, 'requestmatchhistory.html', context) 

    except KeyError:
        context['success'] = 'false'
        return render(request, 'requestmatchhistory.html', context) 

def getcurrentgame(request):
    context = {}
    return render(request, 'getcurrentgame.html', context)

def requestcurrentgame(request):
    #receive data from the template
    template_form = request.POST['requestcurrentgame']

    #Transform the data into string, then transform into lowercase and remove all the whitespaces
    summoner_name = str(template_form)
    summoner_info = searchSummonnerId(summoner_name)
    context = {}
    context['summoner_name'] = summoner_name
    context['summoner_id'] = summoner_info

    url = 'https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/'+ settings.LOL_PLATFORM_ID +'/'+ str(summoner_info['id']) +'?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    pprint(data)
    context['game_info'] = data

    return render(request, 'requestcurrentgame.html', context)

    #settings.LOL_PLATFORM_ID
    #str(summoner_info['id'])
    #settings.LOL_API_KEY