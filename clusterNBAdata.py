from clustering import clustering as cl
import sys


def cluster_cost(points,k):
    #km = cl.kMeansPlus(points,k)
    centers = cl.lloyds(points,k,cl.gonzalez,None)
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


def main():
    #path = sys.argv[1]
    csv_path = 'averages/2010-2016.csv'
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

    result = min_cluster_cost(points,5,20)
    print('Min: ' + str(result))


if __name__ == '__main__':
    main()