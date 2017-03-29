import collections
from clustering import clustering as cl

def get_players(csv_path):
    players = {}
    with open(csv_path) as f:
        p_lines = [line.split(',') for line in f.readlines()]
        stat_headers = p_lines[0][3:]
        for p in p_lines[1:]:
            id = int(p[0])
            name = p[1]
            position = p[2]
            stats = p[3:]
            players[id] = [name,position,stats]
    return players, stat_headers

def get_data(csv_path):
    player_list = get_players(csv_path)
    player_dict = player_list[0]
    stat_headers = player_list[1]

    points_list = []

    for id in player_dict:
        val = player_dict[id]
        point = [id]
        point.extend(val[2])
        points_list.append(point)

    points = cl.get_points_from_list(points_list)

    return player_dict, points

def assign_clusters(centers, points, player_dict):
    clusters = {}
    for i in range(0,len(centers)):
        clusters[i] = []
    for p in points:
        closest_center = cl.index_closest_point(p, centers)
        clusters[closest_center].append(player_dict[p.index])
    return clusters

def get_position_dict(l):
    pos_dict = {}
    for item in l:
        position = item[1]
        if position in pos_dict:
            pos_dict[position] += 1
        else:
            pos_dict[position] = 1
    return pos_dict

def print_cluster_stats(clusters):
    i = 1
    for l in clusters.values():
        print('\n\nCLUSTER {} - Size: {}'.format(i,len(l)))
        pos_dict = get_position_dict(l)
        ordered = collections.OrderedDict(sorted(pos_dict.items()))
        for item in ordered:
            print('{} : {}%'.format(item, ((ordered[item] / len(l)) * 100)))
        i += 1