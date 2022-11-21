import requests as req
import json

error_codes = {400:'The API key was probably malformed, delete the config.json file and restart the application with a valid API key',429:'yo,slow down!\ntoo many requests'}
url1 = 'https://api.football-data.org/v2/'
limit = '5'
def fixtures(key,team_id):
    url = url1+'teams/'+str(team_id)+'/matches?status=SCHEDULED'
    headers = {'X-Auth-Token':key}
    try:
        response = req.get(url,headers=headers)
        match = response.json()['matches'][0]
        data = {'mday':match['matchday'],'utc':match['utcDate'],
            'hteam':match['homeTeam']['name'],'ateam':match['awayTeam']['name']}
#        print(data)
        return data
    except req.exceptions.ConnectionError:
        return "ERROR: Can't connect to the internet"
    except KeyError:
        return error_codes[response.json()['errorCode']]
def standings(key,league_id):
    url = url1+'competitions/'+str(league_id)+'/standings?standingType=TOTAL'
    headers = {'X-Auth-Token':key}
    response = req.get(url,headers=headers)
    table = response.json()['standings'][0]['table']
    data = {}
    for i in range(1,5):
        data[i] = (table[i-1]['team']['name'],table[i-1]['playedGames'],
                table[i-1]['won'],table[i-1]['draw'],table[i-1]['lost'],
                table[i-1]['points'],table[i-1]['goalDifference'])
        if i<4:
            index = len(table)-i
            data[index+1] = (table[index]['team']['name'],table[index]['playedGames'],
                    table[index]['won'],table[index]['draw'],table[index]['lost'],
                    table[index]['points'],table[index]['goalDifference'])
    return data,len(table)
def results(key,team_id):
    url = url1+'teams/'+str(team_id)+'/matches?status=FINISHED&limit='+limit
    headers = {'X-Auth-Token':key}
    response = req.get(url,headers=headers)
    matches = response.json()['matches']
    data_all = []
    for i in range(int(limit)):
        homedata = (matches[i]['homeTeam']['name'],
                matches[i]['score']['fullTime']['homeTeam'])
        awaydata = (matches[i]['awayTeam']['name'],
                matches[i]['score']['fullTime']['awayTeam'])
        if matches[i]['score']['duration'] == 'PENALTY_SHOOTOUT':
            pen_data = ('['+str(matches[i]['score']['penalties']['homeTeam'])+':'+
                    str(matches[i]['score']['penalties']['awayTeam'])+']')
            data_all.append((homedata,awaydata,pen_data))
        else:
            data_all.append((homedata,awaydata,''))

    return data_all
