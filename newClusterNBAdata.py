from clustering import clustering as cl
import helpers as h

def run_all_clustering(points,player_dict):
    k = 6

    centers_gonzalez = cl.lloyds(points,k,cl.gonzalez)
    centers_kmplus = cl.lloyds(points,k,cl.kMeansPlus)

    g_clusters = h.assign_clusters(centers_gonzalez,points,player_dict)
    k_clusters = h.assign_clusters(centers_kmplus,points,player_dict)

    h.print_cluster_stats(g_clusters)
    h.print_cluster_stats(k_clusters)

    #mean_link = cl.hierarchicalClustering(points,k,cl.meanLink)
    #single_link = cl.hierarchicalClustering(points,k,cl.singleLink)
    #complete_link = cl.hierarchicalClustering(points,k,cl.completeLink)




def main():
    path = 'averages/2016.csv'
    data = h.get_data(path)
    player_dict = data[0]
    points = data[1]

    #see "ColumnKey.txt" for index of columns
    limited = cl.limit_all_dims(points,[0,1,2])
    run_all_clustering(limited,player_dict)

if __name__ == '__main__':
    main()