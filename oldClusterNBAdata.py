from clustering import clustering as cl
import sys
import collections


def cluster_cost(points,k):
    clusters = {}
    #km = cl.kMeansPlus(points,k)
    centers = cl.lloyds(points,k,cl.gonzalez,None)
    center_coords = [p.coords for p in centers]
    for i in range(0,len(centers)):
        clusters[i] = []
    for p in points:
        closest_center = cl.index_closest_coords(p, center_coords)
        clusters[closest_center].append(p.index)
    return cl.cost1(points,centers)

def min_cluster_cost(points,start,end):
    min_cost = float('inf')
    min_k = 0
    for k in range(start,end):
        c = cluster_cost(points,k)
        print('{}: {}'.format(k,c))
        if c < min_cost:
            min_cost = c
            min_k = k
    return [min_k,min_cost]


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
    #path = sys.argv[1]
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

    return player_dict, stat_headers, points


def assign_clusters(centers, points, player_dict):
    clusters = {}
    for i in range(0,len(centers)):
        clusters[i] = []
    for p in points:
        closest_center = cl.index_closest_point(p, centers)
        clusters[closest_center].append(player_dict[p.index])
    return clusters


def cluster_points(points,player_dict,k,picker_func):
    #km = cl.kMeansPlus(points,k)
    centers = cl.lloyds(points,k,picker_func,None)
    return centers, assign_clusters(centers,points,player_dict)


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


def run_clustering(picker_function,k,title,points,player_dict):


    print('\n' + title)

    clusters = cluster_points(points,player_dict,k,cl.kMeansPlus)
    centers = clusters[0]
    assigned_dict = clusters[1]
    print_cluster_stats(assigned_dict)
    print('\n\nCost 1')
    print(cl.cost1(centers,points))

def main():
    path = 'averages/2010-2016.csv'
    data = get_data(path)
    player_dict = data[0]
    stat_headers = data[1]
    points = data[2]


    k = 6

    for k in range(4,10):
        print('K: {}'.format(k))
        run_clustering(cl.kMeansPlus,k,'K-MEANS++',points,player_dict)
        run_clustering(cl.gonzalez,k,'GONZALEZ',points,player_dict)







        #result = min_cluster_cost(points,5,20)
    #print('Min: ' + str(result))


if __name__ == '__main__':
    main()