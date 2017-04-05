from clustering import clustering as cl
import helpers as h
import pdb

def run_all_clustering(points,player_dict,k,feature_set):
    run_assignment_clustering(points,player_dict,k,feature_set)
    run_hierarchical_clustering(points,player_dict,k,feature_set)



def run_assignment_clustering(points,player_dict,k,feature_set,writer):
    #centers_gonzalez = cl.lloyds(points,k,cl.gonzalez)
    centers_kmplus = cl.lloyds(points,k,cl.kMeansPlus)
    #g_clusters = h.assign_clusters(centers_gonzalez,points,player_dict)
    k_clusters = h.assign_clusters(centers_kmplus,points,player_dict)
    #h.print_cluster_stats('Gonzalez', k, g_clusters, feature_set)
    h.print_cluster_stats('K-Means++', k, k_clusters, feature_set, writer)

def run_hierarchical_clustering(points,player_dict,k,feature_set,writer):
    #mean_link = cl.hierarchicalClustering(points,k,cl.meanLink)
    single_link = cl.hierarchicalClustering(points,k,cl.singleLink)
    #complete_link = cl.hierarchicalClustering(points,k,cl.completeLink)
    clusters = [[player_dict[i] for i in c] for c in single_link]
    h.print_cluster_stats('Single Link', k, clusters, feature_set, writer)


def run_all_possible_combinations(points,player_dict,k_range):
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

    combinations = h.all_possible_combinations([0,1,2,3,4,5,6])

    with open('assignment_output_full.csv','w') as f:

        f.write('Method,K,Cluster,Size,Center,Forward,Wing,Guard,Feature Set,Player IDs,Centroid\n')

        for feature_set in combinations:
            print(feature_set)
            features = []
            for group in feature_set:
                features.extend(grouped_cols_dict[group])
            limited = cl.limit_all_dims(points,features)

            run_assignment_clustering(points,player_dict,7,feature_set,f)



def main():
    path = 'averages/2010-2016.csv'
    data = h.get_data(path)
    player_dict = data[0]
    points = data[1]

    #see "ColumnKey.txt" for index of columns
    run_all_possible_combinations(points,player_dict,range(3,20))

if __name__ == '__main__':
    main()
