import json
from os import listdir
from os.path import isfile, join
from player import player
import csv


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
        p = player.Player(d)
        players[p.id] = p
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


def get_float_minutes(s):
    vals = s.split(':')
    minutes = float(vals[0])
    seconds = float(vals[0])
    return minutes + (seconds / 60)


def getAverage(d,key,seasons):
    total = 0.0
    count = 0
    for val in d:
        if val['season'] in seasons:
            try:
                if key == 'min':
                    total += get_float_minutes(val[key])
                else:
                    total += float(val[key])
            except ValueError:
                total += 0
            count += 1
    if count > 0:
        return total / float(count)
    else:
        return 0
boxScoreCategories = ['min','fgm','fga','fg3m','fg3a','ftm','fta','oreb','dreb',
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


shotChartCategories = ['minutes_remaining','seconds_remaining','event_type','action_type','shot_type',
                       'shot_distance','loc_x','loc_y','shot_attempted_flag','shot_made_flag',
                       'shot_zone_basic','shot_zone_area','shot_zone_range']
valuesDict = {}

def getDistinctValues(keys,l):
    for v in l:
        for k in keys:
            if k in valuesDict:
                valuesDict[k].add(v[k])
            else:
                s = set()
                s.add(v[k])
                valuesDict[k] = s

numericalShotCategories = ['shot_distance','shot_made_flag','loc_x','loc_y']

categoricalShotCategories = {
    'shot_zone_area': ['Right Side(R)',
                       'Center(C)',
                       'Left Side(L)',
                       'Left Side Center(LC)',
                       'Back Court(BC)',
                       'Right Side Center(RC)'],
    'action_type': ['Fadeaway Bank shot',
                    'Running Layup Shot',
                    'Jump Bank Hook Shot',
                    'Driving Floating Jump Shot',
                    'Step Back Jump shot',
                    'Slam Dunk Shot',
                    'Tip Layup Shot',
                    'Driving Dunk Shot',
                    'Hook Shot',
                    'Running Alley Oop Layup Shot',
                    'Running Tip Shot',
                    'Running Pull-Up Jump Shot',
                    'Fadeaway Jump Shot',
                    'Putback Dunk Shot',
                    'Tip Dunk Shot',
                    'Running Reverse Layup Shot',
                    'Running Finger Roll Layup Shot',
                    'Putback Layup Shot',
                    'Step Back Bank Jump Shot',
                    'No Shot',
                    'Turnaround Jump Shot',
                    'Floating Jump shot',
                    'Jump Shot',
                    'Layup Shot',
                    'Reverse Layup Shot',
                    'Turnaround Fadeaway shot',
                    'Hook Bank Shot',
                    'Driving Jump shot',
                    'Cutting Dunk Shot',
                    'Driving Hook Shot',
                    'Running Alley Oop Dunk Shot',
                    'Alley Oop Layup shot',
                    'Turnaround Bank Hook Shot',
                    'Jump Bank Shot',
                    'Reverse Dunk Shot',
                    'Driving Floating Bank Jump Shot',
                    'Turnaround Fadeaway Bank Jump Shot',
                    'Running Dunk Shot',
                    'Tip Shot',
                    'Running Jump Shot',
                    'Running Hook Shot',
                    'Putback Slam Dunk Shot',
                    'Driving Bank Hook Shot',
                    'Turnaround Hook Shot',
                    'Cutting Finger Roll Layup Shot',
                    'Running Bank shot',
                    'Pullup Jump shot',
                    'Alley Oop Dunk Shot',
                    'Reverse Slam Dunk Shot',
                    'Running Slam Dunk Shot',
                    'Driving Bank shot',
                    'Driving Slam Dunk Shot',
                    'Running Reverse Dunk Shot',
                    'Pullup Bank shot',
                    'Jump Hook Shot',
                    'Driving Reverse Dunk Shot',
                    'Driving Finger Roll Layup Shot',
                    'Dunk Shot',
                    'Turnaround Bank shot',
                    'Driving Layup Shot',
                    'Cutting Layup Shot',
                    'Driving Reverse Layup Shot',
                    'Running Bank Hook Shot',
                    'Finger Roll Layup Shot'],
    'shot_zone_range': ['16-24 ft.',
                        'Back Court Shot',
                        '24+ ft.',
                        'Less Than 8 ft.',
                        '8-16 ft.'],
    'shot_zone_basic': ['Left Corner 3',
                        'Right Corner 3',
                        'Mid-Range',
                        'In The Paint (Non-RA)',
                        'Restricted Area',
                        'Backcourt',
                        'Above the Break 3'],
    'event_type': ['Missed Shot',
                   'Made Shot'],
    'shot_type': ['3PT Field Goal',
                  '2PT Field Goal']
}


def getCategoricalShotCategories():
    result = []
    for category in categoricalShotCategories:
        for c_type in categoricalShotCategories[category]:
            result.append('{}-{}'.format(category,c_type))
    return result

def getShotChartAverages(player,seasons):
    result = []
    for category in numericalShotCategories:
        result.append(getAverage(player.shotCharts,category,seasons))

    player_category_stats = {}

    for category in categoricalShotCategories:
        category_dict = {}
        for c_type in categoricalShotCategories[category]:
            category_dict[c_type] = 0
            player_category_stats[category] = category_dict

    for shot_chart in player.shotCharts:
        for category in categoricalShotCategories:
            c_type = shot_chart[category]
            player_category_stats[category][c_type] += 1

    shot_chart_count = float(len(player.shotCharts))

    for category in player_category_stats:
        category_dict = player_category_stats[category]
        for c_type in category_dict:
            val = category_dict[c_type]
            if shot_chart_count > 0:
                result.append(float(val) / shot_chart_count)
            else:
                result.append(0)




    #getDistinctValues(shotChartCategories,player.shotCharts)
    return result


def getTotalGamesPlayed(player, seasons):
    games = set()
    for val in player.boxScore:
        if val['season'] in seasons:
            games.add(val['game_id'])
    return len(games)


def getAveStats(players,games,seasons):
    result = []
    for player in players.values():
        playerStats = [player.id,player.name,player.getPosition()]
        playerStats.append(getTotalGamesPlayed(player,seasons))
        playerStats.extend(getBoxScoreAverages(player,seasons))
        playerStats.extend(getAdvancedAverages(player,seasons))
        playerStats.extend(getShotChartAverages(player,seasons))
        result.append(playerStats)
    return result
def getOutputName(seasons):
    result = 'averages/'
    result += seasons[0]
    if len(seasons) > 1:
        result += '-' + seasons[len(seasons)-1]
    result += '.csv'
    return result


def clean_row(row):
    row[1] = row[1].replace(',','')
    return row


def outputStatsCsv(allPlayers,games,seasons):
    outputName = getOutputName(seasons)
    aveStats = getAveStats(allPlayers,games,seasons)
    header = ['id','name','position','recorded_games']
    header.extend(boxScoreCategories)
    header.extend(advancedCategories)
    header.extend(numericalShotCategories)
    header.extend(getCategoricalShotCategories())
    for i in range(0,len(header)):
        print('#{} : {}'.format(i-3,header[i]))
    with open(outputName,'w',newline='') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow(header)
        for item in aveStats:
            row = clean_row(item)
            if row[3] > 0:
                writer.writerow(row)


def main():
    games = loadGames()
    allPlayers = loadPlayers()
    for player in allPlayers.values():
        getShotChartAverages(player,['2010','2011','2012','2013','2014','2015','2016'])
    with open('shotChartValues.txt','w',newline='') as f:
        for v in valuesDict:
            f.write(v + ': ' + str(valuesDict[v]) + '\n')
    print('done')
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
