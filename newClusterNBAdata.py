from clustering import clustering as cl
import helpers as h
import pdb

def run_all_clustering(points,player_dict,k,feature_set):
    run_assignment_clustering(points,player_dict,k,feature_set)
    run_hierarchical_clustering(points,player_dict,k,feature_set)



def run_assignment_clustering(points,player_dict,k,feature_set,writer,path_name):
    #centers_gonzalez = cl.lloyds(points,k,cl.gonzalez)
    centers_kmplus = cl.lloyds(points,k,cl.kMeansPlus)
    #g_clusters = h.assign_clusters(centers_gonzalez,points,player_dict)
    k_clusters = h.assign_clusters(centers_kmplus,points,player_dict)
    #h.print_cluster_stats('Gonzalez', k, g_clusters, feature_set)
    h.print_cluster_stats('K-Means++', k, k_clusters, feature_set, writer,path_name,player_dict)

def run_hierarchical_clustering(points,player_dict,k,top_k,feature_set,writer,path_name):
    #mean_link = cl.hierarchicalClustering(points,k,cl.meanLink)
    single_link = cl.hierarchicalClustering(points,k,top_k,cl.singleLink,feature_set,writer,path_name,player_dict)
    #complete_link = cl.hierarchicalClustering(points,k,cl.completeLink)

box_score_cols = range(1,16)
advanced_cols = range(16,31)
shot_zone_basic_cols = range(37,44)
shot_zone_range_cols = range(108,113)
shot_zone_area_cols = range(113,117)
action_type_cols = range(44,108)
shot_type_cols = [117,118]

grouped_cols_dict = {
    0: box_score_cols,
    1: advanced_cols,
    2: shot_zone_basic_cols,
    3: shot_zone_range_cols,
    4: shot_zone_area_cols,
    5: action_type_cols,
    6: shot_type_cols
}

def run_all_possible_combinations(points,player_dict,k_range,f,path_name):


    combinations = h.all_possible_combinations([0,1,2,3,4,5,6])


    for k in k_range:
        for feature_set in combinations:
            print(feature_set)
            features = []
            for group in feature_set:
                features.extend(grouped_cols_dict[group])
            limited = cl.limit_all_dims(points,features)

            run_assignment_clustering(points,player_dict,k,feature_set,f,path_name)

def run_stuff():

    seasons = ['2010-2016','2010','2011','2012','2013','2014','2015','2016']
    with open('hierarchical_output2.csv','w') as f:
        f.write('Method,K,Cluster,Size,Center,Forward,Wing,Guard,Feature Set,Player IDs,Season\n')
        for season in seasons:
            path = 'averages/{}.csv'.format(season)
            data = h.get_data(path)
            player_dict = data[0]
            points = data[1]
            #feature_sets = [[0],[1],[2],[3],[4],[5],[6],[0,1,2,3,6],[2,3,4,5,6]]
            feature_sets = h.all_possible_combinations([0,1,2,3,6])
            for feature_set in feature_sets:
                features = []
                for group in feature_set:
                    features.extend(grouped_cols_dict[group])
                limited = cl.limit_all_dims(points,features)
                run_hierarchical_clustering(limited,player_dict,3,21,feature_set,f,season)

def run_other_stuff():
    files = ['2010-2016']
    with open('assignment_output_combined.csv','w') as f:
        f.write('Method,K,Cluster,Size,Center,Forward,Wing,Guard,Feature Set,Player IDs,Season\n')

        for path_name in files:
            path = 'averages/{}.csv'.format(path_name)
            data = h.get_data(path)
            player_dict = data[0]
            points = data[1]

            #see "ColumnKey.txt" for index of columns
            run_all_possible_combinations(points,player_dict,range(3,9),f,path_name)


def main():

    run_stuff()

    #run_other_stuff()


if __name__ == '__main__':
    main()
