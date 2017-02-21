import json
from os import listdir
from os.path import isfile, join
import csv
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
    boxScore = {}
    advanced = {}
    shotCharts = {}
    fourFactors = {}
    misc = {}
    usage = {}
    def addBoxScore(self,d):
        self.boxScore = d
    def addAdvanced(self,d):
        self.advanced = d
    def addShotCharts(self,d):
        self.shotCharts = d
    def addFourFactor(self,d):
        self.fourFactors = d
    def addMisc(self,d):
        self.misc = d
    def addUsage(self,d):
        self.usage = d
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
def jsonToList(path):
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
        d = jsonToList(directory + '/' + path)
        players[id].addAdvanced(d)
def addFourFactor(players):
    directory = 'nbaStats/playerFourFactor'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToList(directory + '/' + path)
        players[id].addShotCharts(d)
def addMisc(players):
    directory = 'nbaStats/playerMisc'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToList(directory + '/' + path)
        players[id].addMisc(d)
def addShotCharts(players):
    directory = 'nbaStats/playerShot'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToList(directory + '/' + path)
        players[id].addShotCharts(d)
def addUsage(players):
    directory = 'nbaStats/playerUsage'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToList(directory + '/' + path)
        players[id].addUsage(d)
def addBoxScore(players):
    directory = 'nbaStats/playerBoxScore'
    for path in getFiles(directory):
        id = int(path[:-5])
        d = jsonToList(directory + '/' + path)
        players[id].addBoxScore(d)
def loadPlayers():
    playerDict = jsonToList('nbaStats/player.txt')
    players = {}
    for d in playerDict:
        player = Player(d)
        players[player.id] = player
    addBoxScore(players)
    addAdvanced(players)
    addFourFactor(players)
    addMisc(players)
    addShotCharts(players)
    addUsage(players)
    return players
def loadGames():
    games = {}
    gameList = jsonToList('nbaStats/game.txt')
    for game in gameList:
        id = game['id']
        games[game['id']] = game
    return games
def groupByPosition(players):
    grouped = {}
    junkPos = ['RP','TE','RP','D']
    for player in players.values():
        pos = player.getPosition()
        if pos in junkPos:
            continue
        if pos in grouped:
            grouped[pos][player.id] = player
        else:
            group = {}
            group[player.id] = player
            grouped[pos] = group
    return grouped
def getAverage(d,key,seasons):
    total = 0.0
    count = 0
    for val in d:
        if val['season'] in seasons:
            try:
                total += float(val[key])
            except ValueError:
                total += 0
            count += 1
    if count > 0:
        return total / float(count)
    else:
        return 0
boxScoreCategories = ['fgm','fga','fg3m','fg3a','ftm','fta','oreb','dreb',
                      'ast','blk','stl','to','pf','pts','plus_minus',]
def getBoxScoreAverages(player,seasons):
    result = []
    for category in boxScoreCategories:
        result.append(getAverage(player.boxScore,category,seasons))
    return result
advancedCategories = ['off_rating','def_rating','ast_pct','ast_tov','ast_ratio',
                      'oreb_pct','dreb_pct','treb_pct','tm_tov_pct','efg_pct',
                      'ts_pct','usg_pct','pace','pie']
def getAdvancedAverages(player,seasons):
    result = []
    for category in advancedCategories:
        result.append(getAverage(player.advanced,category,seasons))
    return result
def getAveStats(players,games,seasons):
    result = []
    for player in players.values():
        playerStats = [player.id,player.name,player.getPosition()]
        playerStats.extend(getBoxScoreAverages(player,seasons))
        playerStats.extend(getAdvancedAverages(player,seasons))
        result.append(playerStats)
    return result
def getOutputName(seasons):
    result = 'averages/'
    result += seasons[0]
    if len(seasons) > 1:
        result += '-' + seasons[len(seasons)-1]
    result += '.csv'
    return result
def outputStatsCsv(allPlayers,games,seasons):
    outputName = getOutputName(seasons)
    aveStats = getAveStats(allPlayers,games,seasons)
    header = ['id','name','position']
    header.extend(boxScoreCategories)
    header.extend(advancedCategories)
    with open(outputName,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in aveStats:
            writer.writerow(item)
def main():
    games = loadGames()
    allPlayers = loadPlayers()
    outputStatsCsv(allPlayers,games,['2010'])
    outputStatsCsv(allPlayers,games,['2011'])
    outputStatsCsv(allPlayers,games,['2012'])
    outputStatsCsv(allPlayers,games,['2013'])
    outputStatsCsv(allPlayers,games,['2014'])
    outputStatsCsv(allPlayers,games,['2015'])
    outputStatsCsv(allPlayers,games,['2016'])
    outputStatsCsv(allPlayers,games,['2010','2011','2012','2013','2014','2015','2016'])

    #grouped_by_position = groupByPosition(allPlayers)
    #for position in grouped_by_position:
    #    print(position + ': ' + str(len(grouped_by_position[position])))
if __name__ == '__main__':
    main()
