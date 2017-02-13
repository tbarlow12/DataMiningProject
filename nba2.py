from urllib2 import Request, urlopen, URLError
import requests
import json
import os.path
api_key = '9LsHJP7EhGYdAlSeD3QIbWcitTafxpZM'


def basicPlayerStats(playerId):
    if os.path.isfile('basicPlayer/{}.json'.format(playerId)):
        return
    url = 'http://api.probasketballapi.com/player'
    query = {'api_key': api_key,'player_id':playerId}
    r = requests.post(url, data=query)
    with open('basicPlayer/{}.json'.format(playerId),'w') as f:
        f.write(r.text)

def advancedPlayerStats(playerId):
    if os.path.isfile('advancedPlayer/{}.json'.format(playerId)):
        return
    url = 'http://api.probasketballapi.com/advanced/player'
    query = {'api_key': api_key,'player_id':playerId}
    r = requests.post(url, data=query)
    with open('advancedPlayer/{}.json'.format(playerId),'w') as f:
        f.write(r.text)

def basicTeamStats(teamId):
    if os.path.isfile('basicTeam/{}.json'.format(teamId)):
        return
    url = 'http://api.probasketballapi.com/team'
    query = {'api_key': api_key,'team_id':teamId}
    r = requests.post(url, data=query)
    with open('basicTeam/{}.json'.format(teamId),'w') as f:
        f.write(r.text)

def advancedTeamStats(teamId):
    if os.path.isfile('advancedTeam/{}.json'.format(teamId)):
        return
    url = 'http://api.probasketballapi.com/advanced/team'
    query = {'api_key': api_key,'team_id':teamId}
    r = requests.post(url, data=query)
    with open('advancedTeam/{}.json'.format(teamId),'w') as f:
        f.write(r.text)

def teamBoxScore(teamId):
    if os.path.isfile('teamBoxscore/{}.json'.format(teamId)):
        return
    url = 'http://api.probasketballapi.com/boxcore/team'
    query = {'api_key': api_key,'team_id':teamId}
    r = requests.post(url, data=query)
    with open('teamBoxscore/{}.json'.format(teamId),'w') as f:
        f.write(r.text)

def playerBoxScore(playerId):
    if os.path.isfile('playerBoxscore/{}.json'.format(playerId)):
        return
    url = 'http://api.probasketballapi.com/boxcore/player'
    query = {'api_key': api_key,'player_id':playerId}
    r = requests.post(url, data=query)
    with open('playerBoxscore/{}.json'.format(playerId),'w') as f:
        f.write(r.text)

def teamFourFactor(teamId):
    if os.path.isfile('teamFourFactor/{}.json'.format(teamId)):
        return
    url = 'http://api.probasketballapi.com/four_factor/team'
    query = {'api_key': api_key,'team_id':teamId}
    r = requests.post(url, data=query)
    with open('teamFourFactor/{}.json'.format(teamId),'w') as f:
        f.write(r.text)

def playerFourFactor(playerId):
    if os.path.isfile('playerFourFactor/{}.json'.format(playerId)):
        return
    url = 'http://api.probasketballapi.com/four_factor/player'
    query = {'api_key': api_key,'player_id':playerId}
    r = requests.post(url, data=query)
    with open('playerFourFactor/{}.json'.format(playerId),'w') as f:
        f.write(r.text)

def playerMisc(playerId):
    if os.path.isfile('playerMisc/{}.json'.format(playerId)):
        return
    url = 'http://api.probasketballapi.com/misc/player'
    query = {'api_key': api_key,'player_id':playerId}
    r = requests.post(url, data=query)
    with open('playerMisc/{}.json'.format(playerId),'w') as f:
        f.write(r.text)
def teamMisc(teamId):
    if os.path.isfile('teamMisc/{}.json'.format(teamId)):
        return
    url = 'http://api.probasketballapi.com/misc/player'
    query = {'api_key': api_key,'team_id':teamId}
    r = requests.post(url, data=query)
    with open('teamMisc/{}.json'.format(teamId),'w') as f:
        f.write(r.text)
def playerShot(playerId):
    if os.path.isfile('playerShot/{}.json'.format(playerId)):
        return
    url = 'http://api.probasketballapi.com/shots'
    query = {'api_key': api_key,'player_id':playerId}
    r = requests.post(url, data=query)
    with open('playerShot/{}.json'.format(playerId),'w') as f:
        f.write(r.text)

def playerUsage(playerId):
    if os.path.isfile('playerUsage/{}.json'.format(playerId)):
        return
    url = 'http://api.probasketballapi.com/usage/player'
    query = {'api_key': api_key,'player_id':playerId}
    r = requests.post(url, data=query)
    with open('playerUsage/{}.json'.format(playerId),'w') as f:
        f.write(r.text)

def playerVU(playerId):
    if os.path.isfile('playerVU/{}.json'.format(playerId)):
        return
    url = 'http://api.probasketballapi.com/sportsvu/player'
    query = {'api_key': api_key,'player_id':playerId}
    r = requests.post(url, data=query)
    with open('playerVU/{}.json'.format(playerId),'w') as f:
        f.write(r.text)

def teamVU(teamId):
    if os.path.isfile('teamVU/{}.json'.format(teamId)):
        return
    url = 'http://api.probasketballapi.com/sportsvu/team'
    query = {'api_key': api_key,'team_id':teamId}
    r = requests.post(url, data=query)
    with open('teamVU/{}.json'.format(teamId),'w') as f:
        f.write(r.text)

def jsonToDict(path):
    with open(path) as f:
        t = f.read()
        return json.loads(t)

def getData(games,players,teams):
    for player in players:
        id = player['id']
        playerShot(id)
        playerUsage(id)
        basicPlayerStats(id)
        advancedPlayerStats(id)
        playerMisc(id)
        playerFourFactor(id)
        playerBoxScore(id)
        print 'player: ' + str(id)
    for team in teams:
        id = team['id']
        teamVU(id)
        basicTeamStats(id)
        advancedTeamStats(id)
        teamMisc(id)
        teamFourFactor(id)
        teamBoxScore(id)
        print 'team: ' + str(id)


def main():
    games = jsonToDict('game.txt')
    players = jsonToDict('player.txt')
    teams = jsonToDict('team.txt')

    getData(games,players,teams)





if __name__ == '__main__':
    main()
