import requests
import json
def jsonToList(path):
    with open(path) as f:
        t = f.read()
        return json.loads(t)

def playerBoxScore(id):
    api_key = 'M0YtlgZ5C4aKSA3rm8WdcL7DsQpknqf6'
    url = 'http://api.probasketballapi.com/boxscore/player'
    query = {'api_key': api_key,'player_id':id}
    r = requests.post(url,data=query)
    f = open('nbaStats/playerBoxScore/{}.json'.format(id),'w')
    f.write(r.text)

players = jsonToList('nbaStats/player.txt')
for player in players:
    id = int(player['id'])
    playerBoxScore(id)
    print(id)
