from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from stock.models import Hero, mastery, Rune
import json, requests, grequests

# Create your procedures here.




def searchSummonerStats(summoner_id):
    context = {}

    if type(summoner_id) != list:
        url = 'https://na.api.pvp.net/api/lol/'+ settings.LOL_REGION +'/v1.3/stats/by-summoner/'+ str(summoner_id) +'/summary?api_key=' + settings.LOL_API_KEY2
    else:
        urls = []
        for summoner in summoner_id:
            urls.append('https://na.api.pvp.net/api/lol/'+ settings.LOL_REGION +'/v1.3/stats/by-summoner/'+ str(summoner) +'/summary?api_key=' + settings.LOL_API_KEY2)

    rs = (grequests.get(u) for u in urls)
    resp = grequests.map(rs)

    stat_success = 1
    for response in resp:
        values_json = json.loads(response.text)
        context[values_json['summonerId']] = values_json
        if str(response) != '<Response [200]>':
            stat_success = '0'

    return (context, stat_success)




def searchSummonnerId(summoner_name):
    context = {}
    summoner_name = summoner_name.lower()
    summoner_name = summoner_name.replace(" ", "")
    url = 'https://na.api.pvp.net/api/lol/'+ settings.LOL_REGION +'/v1.4/summoner/by-name/'+ summoner_name +'?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)

    if resp.status_code == 200:   

        data = json.loads(resp.text)

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
    else:
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




def searchSummonerChampionMastery(summoner_id, champion_id):
    url = 'https://na.api.pvp.net/championmastery/location/'+ settings.LOL_PLATFORM_ID +'/player/'+ str(summoner_id) +'/champion/'+ str(champion_id) +'?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)
    try:
        data = json.loads(resp.text)
    except ValueError, e:
        data = {}
        data['championLevel'] = 0
    return data




def searchTierImage(tier):
    tier = tier.lower()
    tier = tier.title()
    imgage_dict = {
        'Unranked': 'http://s18.postimg.org/5t36g8pf9/unranked_1_92a5f4dfbb5ffab13f901c80a9d14384.png',
        'Bronze': 'https://s3.amazonaws.com/f.cl.ly/items/3q1f0B2j1E0Y0a3P310V/Bronze.png',
        'Silver': 'https://s3.amazonaws.com/f.cl.ly/items/0J253J1z3o1d2Z152M2b/Silver.png',
        'Gold': 'https://s3.amazonaws.com/f.cl.ly/items/1Y360o3N261b020g0h1r/Gold.png',
        'Platinum': 'https://s3.amazonaws.com/f.cl.ly/items/3F2j1u2d3f0w0l260m3E/Platinum.png',
        'Diamond': 'https://s3.amazonaws.com/f.cl.ly/items/2X2F2r192B3K1j0p0n3d/Diamond.png',
        'Master': 'https://s3.amazonaws.com/f.cl.ly/items/083C392i0t1p1a3h1C3i/Master.png',
        'Challenger': 'https://s3.amazonaws.com/f.cl.ly/items/0K350Q2C0b0E0n043e0L/Challenger.png',
    }

    return imgage_dict.get(tier, 'http://s18.postimg.org/5t36g8pf9/unranked_1_92a5f4dfbb5ffab13f901c80a9d14384.png')




def refreshRuneDatabase(request):
    context ={}
    # request the mastery list from the riot API
    url = 'https://na.api.pvp.net/api/lol/static-data/'+ settings.LOL_REGION +'/v1.2/rune?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    # delete all the existing masteries so the new information can be added
    old_runes = Rune.objects.all()
    old_runes.delete()

    for rune in data['data']:
        rune_id_riot = data['data'][rune]['id']
        rune_name = data['data'][rune]['name']
        rune_description = data['data'][rune]['description'].encode('ascii', 'ignore')
        rune_tier = data['data'][rune]['rune']['tier']
        rune_type_data = data['data'][rune]['rune']['type']
        rune_bonus = rune_description.split(' de')[0]
        rune_honest_text = rune_description.split(rune_bonus)[1]
        rune_honest_text = rune_honest_text.split(' (')[0]
        try:
            rune_bonus = rune_bonus.split('+')[1]
        except:
            rune_bonus = rune_bonus.split('-')[1]
        try:
            rune_is_percentage = rune_bonus.split('%')[1]
            rune_bonus = rune_bonus.split('%')[0]
            rune_is_percentage = 1
        except:
            rune_is_percentage = 0
        # rune_bonus = rune_bonus.replace(' ', '')
        rune_bonus = rune_bonus.split(' ')[0]
        rune_bonus = rune_bonus.replace(',', '.')
        rune_bonus = rune_bonus.replace(' ', '')
        new_rune = Rune(id_riot = rune_id_riot, name = rune_name, description = rune_description, tier = rune_tier, rune_type = rune_type_data, bonus = float(rune_bonus), honest_text = rune_honest_text, is_percentage = rune_is_percentage)
        new_rune.save()

    return render(request, 'refresh-rune-database.html', context)




def refreshMasteryDatabase(request):
    context ={}
    # request the mastery list from the riot API
    url = 'https://na.api.pvp.net/api/lol/static-data/'+ settings.LOL_REGION +'/v1.2/mastery?api_key=' + settings.LOL_API_KEY
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    # delete all the existing masteries so the new information can be added
    old_masteries = mastery.objects.all()
    old_masteries.delete()

    for mastery_item in data['data']:
        mastery_id_riot = data['data'][mastery_item]['id']
        mastery_name = data['data'][mastery_item]['name']
        mastery_description = data['data'][mastery_item]['description']
        table_position = str(mastery_id_riot)[1]
        for item in mastery_description:
                mastery_description_single_var = item
        new_mastery = mastery(id_riot = mastery_id_riot, name = mastery_name, description = mastery_description_single_var, position = table_position)
        new_mastery.save()

    return render(request, 'refresh-mastery-database.html', context)




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
    context2 = {}

    # check if the the player name was found in the lol database (1)
    if summoner_info['success'] == 1:

        url = 'https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/'+ settings.LOL_PLATFORM_ID +'/'+ str(summoner_info['id']) +'?api_key=' + settings.LOL_API_KEY
        resp = requests.get(url=url)

        # check if this player is currently in game (2)
        if resp.status_code == 200:
            data = json.loads(resp.text)

            data_formated={}

            #search for the participant names based on their IDs
            players_ids_list = []
            for player in data['participants']:
                players_ids_list.append(player['summonerId'])

            player_objects = searchSummonerName(players_ids_list)
            player_ranks = searchSummonerRank(players_ids_list)
            player_stats, stat_success = searchSummonerStats(players_ids_list)

            # fill the data array with the name
            for player in player_objects:
                data_formated[player] ={}
                data_formated[player]['name'] = player_objects[player]['name']

            for player in data['participants']:
                data_formated[str(player['summonerId'])]['side'] = player['teamId']
                if stat_success == 1:
                    for stat in player_stats[int(player['summonerId'])]['playerStatSummaries']:
                        if stat['playerStatSummaryType'] == 'Unranked':
                            data_formated[str(player['summonerId'])]['wins'] = stat['wins']

            # fill the data array with the tier
            for player in player_ranks:
                data_formated[player]['tier'] = player_ranks[player][0]['tier']

            #fill the data array with the champion name
            for player in data['participants']:
                heroes_ids = player['championId']
                champion = Hero.objects.filter(id_riot = heroes_ids)
                data_formated[str(player['summonerId'])]['champion'] = champion[0].__str__()
                champion_name_process = champion[0].__str__()
                champion_name_process = champion_name_process.replace(' ', '')
                champion_name_process = champion_name_process.replace('.', '')
                if champion_name_process == 'Bardo':
                    champion_name_process = 'Bard'
                data_formated[str(player['summonerId'])]['champion'] = '<span style="margin-left: 12px;"><img style="margin-right: 6px;" src="http://ddragon.leagueoflegends.com/cdn/6.6.1/img/champion/' + champion_name_process + '.png" class="rank--img tier-img">' +  data_formated[str(player['summonerId'])]['champion'] + '<span>'
                try:
                    data_formated[str(player['summonerId'])]['tier']
                    data_formated[str(player['summonerId'])]['tier'] = '<span style="margin-left: 12px;"><img style="margin-right: 2px;" src="'+ searchTierImage(data_formated[str(player['summonerId'])]['tier']) +'" class="rank--img tier-img">' + data_formated[str(player['summonerId'])]['tier'] + '<span>'
                except:
                    data_formated[str(player['summonerId'])]['tier'] = 'UNRANKED'
                    data_formated[str(player['summonerId'])]['tier'] = '<span style="margin-left: 12px;"><img style="margin-right: 2px;" src="'+ searchTierImage(data_formated[str(player['summonerId'])]['tier']) +'" class="rank--img tier-img">' + data_formated[str(player['summonerId'])]['tier'] + '<span>'


            mastery_set = {}
            # fill the data array with the masteries stats
            for player in data['participants']:
                mastery_set[1] = 0
                mastery_set[2] = 0
                mastery_set[3] = 0
                masteries = player['masteries']
                for diff_mastery in masteries:
                    mastery_object = mastery.objects.get(id_riot = diff_mastery['masteryId'])
                    mastery_set[mastery_object.__position__()] = mastery_set[mastery_object.__position__()] + diff_mastery['rank']
                data_formated[str(player['summonerId'])]['masteries'] = str(mastery_set[1]) + ' / ' + str(mastery_set[3]) + ' / ' +str(mastery_set[2])

            context['header'] = []
            context['header'].append('Champion')
            context['header'].append('Name')
            context['header'].append('Tier')
            if stat_success == 1:
                context['header'].append('Wins')
            context['header'].append('Masteries')

            context['players'] = []
            player_data_to_context = []
            for player in data_formated:
                if data_formated[player]['side'] == 100:
                    player_data_to_context = []
                    player_data_to_context.append(data_formated[player]['champion'])
                    player_data_to_context.append(data_formated[player]['name'])
                    player_data_to_context.append(data_formated[player]['tier'])
                    if stat_success == 1:
                        player_data_to_context.append(data_formated[player]['wins'])
                    player_data_to_context.append(data_formated[player]['masteries'])
                    context['players'].append(player_data_to_context)

            context2['header'] = []
            context2['header'].append('Champion')
            context2['header'].append('Name')
            context2['header'].append('Tier')
            if stat_success == 1:
                context2['header'].append('Wins')
            context2['header'].append('Masteries')

            context2['players'] = []
            player_data_to_context = []
            for player in data_formated:
                if data_formated[player]['side'] == 200:
                    player_data_to_context = []
                    player_data_to_context.append(data_formated[player]['champion'])
                    player_data_to_context.append(data_formated[player]['name'])
                    player_data_to_context.append(data_formated[player]['tier'])
                    if stat_success == 1:
                        player_data_to_context.append(data_formated[player]['wins'])
                    player_data_to_context.append(data_formated[player]['masteries'])
                    context2['players'].append(player_data_to_context)

            return render(request, 'requestcurrentgame.html', {'context': context, 'context2': context2, 'summoner_name': summoner_name, 'summoner_info': summoner_info})

        # check if this player is currently in game (2)
        else:
            return render(request, 'general-error.html', context)

    # check if the the player name was found in the lol database (1)
    else:
        return render(request, 'general-error.html', context)


    #settings.LOL_PLATFORM_ID
    #str(summoner_info['id'])
    #settings.LOL_API_KEY
    #id do bazetinho 7523004
    #id do fafis 454451
    #id do leo 514850