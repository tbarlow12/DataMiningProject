import json
from os import listdir
from os.path import isfile, join

class AdvancedTeam(object):
    def __init__(self,d):
        self.game_id = d['game_id']
        self.team_id = d['team_id']
        self.opponent_id = d['opponent_id']
        self.period = d['period']
        self.season = d['season']
        self.min = d['min']
        self.off_rating = d['off_rating']
        self.def_rating = d['def_rating']
        self.ast_pct = d['ast_pct']
        self.ast_tov = d['ast_tov']
        self.ast_ratio = d['ast_ratio']
        self.oreb_pct = d['oreb_pct']
        self.dreb_pct = d['dreb_pct']
        self.treb_pct = d['treb_pct']
        self.tm_tov_pct = d['tm_tov_pct']
        self.efg_pct = d['efg_pct']
        self.ts_pct = d['ts_pct']
        self.usg_pct = d['usg_pct']
        self.pace = d['pace']
        self.pie = d['pie']
class AdvancedPlayer(object):
    def __init__(self,d):
        self.game_id = d['game_id']
        self.player_id = d['player_id']
        self.opponent_id = d['opponent_id']
        self.period = d['period']
        self.season = d['season']
        self.min = d['min']
        self.off_rating = d['off_rating']
        self.def_rating = d['def_rating']
        self.ast_pct = d['ast_pct']
        self.ast_tov = d['ast_tov']
        self.ast_ratio = d['ast_ratio']
        self.oreb_pct = d['oreb_pct']
        self.dreb_pct = d['dreb_pct']
        self.treb_pct = d['treb_pct']
        self.tm_tov_pct = d['tm_tov_pct']
        self.efg_pct = d['efg_pct']
        self.ts_pct = d['ts_pct']
        self.usg_pct = d['usg_pct']
        self.pace = d['pace']
        self.pie = d['pie']
class Player(object):

    advanced = {}

    def addAdvanced(self,d):
        self.advanced[d['game_id']] = d

    def __init__(self,d):
        self.id = d['id']
        self.team_id = d['team_id']
        self.first = d['first_name']
        self.last = d['last_name']
        self.birth = d['birth_date']
        self.position = d['position']
        self.dk_position = d['dk_position']
        self.dk_id = d['dk_id']

def getFiles(folder):
    return [f for f in listdir(folder) if isfile(join(folder, f))]

def jsonToDict(path):
    with open(path) as f:
        t = f.read()
        return json.loads(t)

def distinctValues(d,value):
    s = set()
    for d1 in d:
        s.add(d1[value])
    return s

games = jsonToDict('nbaStats/game.txt')
players = jsonToDict('nbaStats/player.txt')
teams = jsonToDict('nbaStats/team.txt')


playerShotCharts = {}
directory = 'nbaStats/playerShot'
for path in getFiles(directory):
    id = int(path[:-5])
    d = jsonToDict(directory + '/' + path)
    playerShotCharts[id] = d


exampleShotChart = playerShotCharts[203145]
for d in exampleShotChart:
    for item in d:
        print(item)
