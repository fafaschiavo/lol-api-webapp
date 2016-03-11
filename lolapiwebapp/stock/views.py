from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from stock.models import Hero
import json, requests

# Create your procedures here.



def searchSummonnerId(summoner_name):
    summoner_name = summoner_name.lower()
    summoner_name = summoner_name.replace(" ", "")
    url = 'https://na.api.pvp.net/api/lol/'+ settings.LOL_REGION +'/v1.4/summoner/by-name/'+ summoner_name +'?api_key=' + settings.LOL_API_KEY
    
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




def searchSummonerName(summoner_id):
    if type(summoner_id) != list:
        id_list = str(summoner_id)
    else:
        id_list = ''
        for summoner in summoner_id:
            id_list = id_list + str(summoner) + ','

    url = 'https://na.api.pvp.net/api/lol/'+ settings.LOL_REGION +'/v1.4/summoner/'+ id_list +'?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    return data

def searchSummonerRank(summoner_id):
    if type(summoner_id) != list:
        id_list = str(summoner_id)
    else:
        id_list = ''
        for summoner in summoner_id:
            id_list = id_list + str(summoner) + ','

    url = 'https://na.api.pvp.net/api/lol/'+ settings.LOL_REGION +'/v2.5/league/by-summoner/'+ id_list +'?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    return data



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
            champion_name = Hero.objects.filter(id_riot = match['champion'])
            try:
                match_data_to_context.append(champion_name[0].name)
            except IndexError:
                match_data_to_context.append('-')
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

    data_formated={}

    #search for the participant names based on their IDs
    players_ids_list = []
    for player in data['participants']:
        players_ids_list.append(player['summonerId'])

    player_objects = searchSummonerName(players_ids_list)
    player_ranks = searchSummonerRank(players_ids_list)

    # pprint(player_ranks['461912'][0]['name'])

    # pprint(data)

    # fill the data array with the name
    for player in player_objects:
        data_formated[player] ={}
        data_formated[player]['name'] = player_objects[player]['name']

    for player in data['participants']:
        data_formated[str(player['summonerId'])]['side'] = player['teamId']

    # fill the data array with the tier
    for player in player_ranks:
        data_formated[player]['tier'] = player_ranks[player][0]['tier']

    #fill the data array with the champion name
    for player in data['participants']:
        heroes_ids = player['championId']
        champion = Hero.objects.filter(id_riot = heroes_ids)
        data_formated[str(player['summonerId'])]['champion'] = champion[0].__str__()

    pprint(data_formated)
    context['game_info'] = data_formated
    return render(request, 'requestcurrentgame.html', context)




def refreshChampionDatabase(request):
    context ={}
    # request the champion list from the riot API
    url = 'https://na.api.pvp.net/api/lol/static-data/'+ settings.LOL_REGION +'/v1.2/champion?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    # delete all the existing heroes so the new information can be added
    old_heroes = Hero.objects.all()
    old_heroes.delete() 

    for champion in data['data']:
        champion_id_riot = data['data'][champion]['id']
        champion_name = data['data'][champion]['name']
        champion_title = data['data'][champion]['title']
        new_champion = Hero(id_riot = champion_id_riot, name = champion_name, title = champion_title)
        new_champion.save()

    return render(request, 'refresh-champion-database.html', context)

    #settings.LOL_PLATFORM_ID
    #str(summoner_info['id'])
    #settings.LOL_API_KEY
    #id do bazetinho 7523004
    #id do fafis 454451
    #id do leo 514850