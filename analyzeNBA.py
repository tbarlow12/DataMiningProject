import json
from os import listdir
from os.path import isfile, join
def normalizePosition(pos):
    d = {
        'SG':'Shooting Guard',
        'PG':'Point Guard',
        'G':'Guard',
        'SF':'Small Forward',
        'PF':'Power Forward',
        'C':'Center',
        '':'Unknown'
    }
    if pos in d:
        return d[pos]
    return pos
class Player(object):
    advanced = {}
    shotCharts = {}
    fourFactors = {}
    misc = {}
    usage = {}
    def addAdvanced(self,d):
        for game in d:
            self.advanced[game['game_id']] = game
    def addShotCharts(self,d):
        for game in d:
            self.shotCharts[game['game_id']] = game
    def addFourFactor(self,d):
        for game in d:
            self.fourFactors[game['game_id']] = game
    def addMisc(self,d):
        for game in d:
           self.misc[game['game_id']] = game
    def addUsage(self,d):
        for game in d:
            self.usage[game['game_id']] = game
    def toString(self):
        s = str(self.id) + '\nNAME:' + self.name + '\nPOS:' + self.position + \
            '\nDK_POS:' + self.dk_position + '\nDK_ID:' + self.dk_id + '\n'
        return s
    def getPosition(self):
        pos = self.position
        if len(pos) == 0:
            pos = self.dk_position
        return normalizePosition(pos)
    def __init__(self,d):
        self.id = int(d['id'])
        self.team_id = int(d['team_id'])
        self.first = d['first_name']
        self.last = d['last_name']
        self.name = self.first + ' ' + self.last
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
def addAdvanced(players):
    directory = 'nbaStats/advancedPlayer'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToDict(directory + '/' + path)
        players[id].addAdvanced(d)
def addFourFactor(players):
    directory = 'nbaStats/playerFourFactor'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToDict(directory + '/' + path)
        players[id].addShotCharts(d)
def addMisc(players):
    directory = 'nbaStats/playerMisc'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToDict(directory + '/' + path)
        players[id].addMisc(d)
def addShotCharts(players):
    directory = 'nbaStats/playerShot'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToDict(directory + '/' + path)
        players[id].addShotCharts(d)
def addUsage(players):
    directory = 'nbaStats/playerUsage'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToDict(directory + '/' + path)
        players[id].addUsage(d)
def loadPlayers():
    playerDict = jsonToDict('nbaStats/player.txt')
    players = {}
    for d in playerDict:
        player = Player(d)
        players[player.id] = player
    addAdvanced(players)
    addFourFactor(players)
    addMisc(players)
    addShotCharts(players)
    addUsage(players)
    return players
def groupByPosition(players):
    grouped = {}
    junkPos = ['RP','TE','RP','D']
    for player in players.values():
        pos = player.getPosition()
        if pos in junkPos:
            continue
        if pos in grouped:
            grouped[pos].append(player)
        else:
            group = [player]
            grouped[pos] = group
    return grouped
def main():
    allPlayers = loadPlayers()
    grouped_by_position = groupByPosition(allPlayers)
    for position in grouped_by_position:
        print(position + ': ' + str(len(grouped_by_position[position])))

if __name__ == '__main__':
    main()
