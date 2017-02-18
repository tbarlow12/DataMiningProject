import json
from os import listdir
from os.path import isfile, join

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

    def __init__(self,d):
        self.id = int(d['id'])
        self.team_id = int(d['team_id'])
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

def main():
    gameDict = jsonToDict('nbaStats/game.txt')
    playerDict = jsonToDict('nbaStats/player.txt')
    teamDict = jsonToDict('nbaStats/team.txt')
    players = {}
    for d in playerDict:
        player = Player(d)
        players[player.id] = player

    addAdvanced(players)
    addFourFactor(players)
    addMisc(players)
    addShotCharts(players)
    addUsage(players)

    print(players[203120].shotCharts.values())

'''
    exampleShotChart = playerShotCharts[203145]
    for d in exampleShotChart:
        for item in d:
            print(item)
'''

if __name__ == '__main__':
    main()