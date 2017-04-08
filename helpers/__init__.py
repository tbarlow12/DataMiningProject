import collections
from clustering import clustering as cl
import pdb
from itertools import chain
from itertools import combinations

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
            players[id] = [[id,name],position,stats]
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

def hierarchical_clusters(clusters, player_dict):
    return [[player_dict[i] for i in c] for c in clusters]

def assign_clusters(centers, points, player_dict):
    clusters = []
    for i in range(0,len(centers)):
        clusters.append([])
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


def print_cluster_stats(clustering_method,k,clusters,feature_set,writer,path_name,player_dict):
    #method,k,cluster,size,center,center-forward,forward-center,forward,forward-guard,guard-forward,guard
    positions = ['Center','Forward','Wing','Guard']
    i = 1
    for cluster in clusters:
        #print('\n\nCLUSTER {} - Size: {}'.format(i,len(l)))
        pos_dict = get_position_dict(cluster)
        line = '{},{},{},{},'.format(clustering_method,k,i,len(cluster))
        for position in positions:
            if position in pos_dict:
                line += '{},'.format(pos_dict[position])
            else:
                line += '0,'
        for item in feature_set:
            line += str(item) + ' '
        line = line[:-1]
        line += ','
        for player in cluster:
            id = int(player[0][0])
            line += str(id) + '-' + player_dict[id][0][1] + '/'
        line = line[:-1]
        line += ',{}\n'.format(path_name)
        writer.write(line)
        i += 1

def print_cluster_stats2(clustering_method,k,clusters,feature_set,writer,path_name,player_dict):
    #method,k,cluster,size,center,center-forward,forward-center,forward,forward-guard,guard-forward,guard
    positions = ['Center','Forward','Wing','Guard']
    i = 1
    for cluster in clusters:
        #print('\n\nCLUSTER {} - Size: {}'.format(i,len(l)))
        pos_dict = get_position_dict(cluster)
        line = '{},{},{},{},'.format(clustering_method,k,i,len(cluster))
        for position in positions:
            if position in pos_dict:
                line += '{},'.format(pos_dict[position])
            else:
                line += '0,'
        for item in feature_set:
            line += str(item) + ' '
        line = line[:-1]
        line += ','
        for player in cluster:
            id = int(player.index)
            line += str(id) + '-' + player_dict[id][0][1] + '/'
        line = line[:-1]
        line += ',{}\n'.format(path_name)
        writer.write(line)
        i += 1

def all_possible_combinations(possible_features):
    feature_sets = list(chain.from_iterable(combinations(possible_features, r) for r in range(len(possible_features)+1)))
    result = []
    for feature_set in feature_sets:
        result.append(list(feature_set))
    return result[1:]
