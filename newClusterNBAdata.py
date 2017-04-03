from clustering import clustering as cl
import helpers as h

def run_all_clustering(points,player_dict,k):
    run_assignment_clustering(points,player_dict,k)
    run_hierarchical_clustering(points,player_dict,k)



def run_assignment_clustering(points,player_dict,k):
    centers_gonzalez = cl.lloyds(points,k,cl.gonzalez)
    centers_kmplus = cl.lloyds(points,k,cl.kMeansPlus)

    g_clusters = h.assign_clusters(centers_gonzalez,points,player_dict)
    k_clusters = h.assign_clusters(centers_kmplus,points,player_dict)
    print('\nGONZALEZ\n')
    h.print_cluster_stats('Gonzalez',k,g_clusters)
    h.print_cluster_stats('K-Means++',k,k_clusters)



def run_hierarchical_clustering(points,player_dict,k):
    print('in hierarchicalClustering')
    mean_link = cl.hierarchicalClustering(points,k,cl.meanLink)
    print(mean_link)
    single_link = cl.hierarchicalClustering(points,k,cl.singleLink)
    print(single_link)
    complete_link = cl.hierarchicalClustering(points,k,cl.completeLink)
    print(complete_link)



def main():
    path = 'averages/2016.csv'
    data = h.get_data(path)
    player_dict = data[0]
    points = data[1]

    #see "ColumnKey.txt" for index of columns
    limited = cl.limit_all_dims(points,[0,1,2])

    box_score_cols = range(1,16)

    advanced_cols = range(16,31)

    shot_zone_basic_cols = range(37,44)

    shot_zone_range_cols = range(108,113)

    shot_zone_area_cols = range(113,119)

    action_type_cols = range(44,108)

    shot_type_cols = [119,120]



    #run_all_clustering(limited,player_dict,20)
    #run_hierarchical_clustering(limited,player_dict,10)
    run_assignment_clustering(cl.limit_all_dims(points,box_score_cols),player_dict,10)

if __name__ == '__main__':
    main()
