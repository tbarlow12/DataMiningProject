import pdb
import math
import operator
import csv

def AddToClusters(clusters, split):
    method = split[0]
    k = int(split[1])
    feature_set = split[8]
    season = split[10]
    if method in clusters:
        method_dict = clusters[method]
        if k in method_dict:
            k_dict = method_dict[k]
            if feature_set in k_dict:
                feature_set_dict = k_dict[feature_set]
                if season in feature_set_dict:
                    feature_set_dict[season].append(split)
                else:
                    feature_set_dict[season] = [split]
            else:
                feature_set_dict = {season: [split]}
                k_dict[feature_set] = feature_set_dict
        else:
            feature_set_dict = {season: [split]}
            k_dict = {feature_set: feature_set_dict}
            method_dict[k] = k_dict
    else:
        feature_set_dict = {season: [split]}
        k_dict = {feature_set: feature_set_dict}
        method_dict = {k : k_dict}
        clusters[method] = method_dict

def GetPolarity(group,size_threshold):
    total = 0.0

    for cluster in group:
        size = float(cluster[3])
        if size >= size_threshold:
            c = int(cluster[4])
            f = int(cluster[5])
            w = int(cluster[6])
            g = int(cluster[7])
            m = max([c,f,w,g])
            if size != 0:
                total += float(m) / float(cluster[3])
    return float(total) / float(len(group))



clusters = {}

with open('clustering_all.csv') as f:
    lines = f.readlines()
    for line in lines[1:]:
        split = line.split(',')
        AddToClusters(clusters,split)

polarity_scores = []

k_limit = 8
for method in clusters:
    for k in clusters[method]:
        for feature_set in clusters[method][k]:
            for season in clusters[method][k][feature_set]:
                polarity = GetPolarity(clusters[method][k][feature_set][season],1)
                if k <= k_limit:
                    polarity_scores.append([polarity,method,k,feature_set,season[:-1]])


polarity_scores = sorted(polarity_scores, key=operator.itemgetter(0),reverse=True)

with open('polarity_output.csv','w',newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['Polarity','Method','K','Feature Set','Season'])
    wr.writerows(polarity_scores)
