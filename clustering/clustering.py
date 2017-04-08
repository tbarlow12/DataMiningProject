import numpy as np
import helpers as h
import random
import pdb
import bisect


class Point(object):

    def __init__(self,line):
        self.coords = []
        self.index = int(line[0])
        i = 1
        while i < len(line):
            self.coords.append(float(line[i]))
            i += 1

def min_dim(points,i):
    min = float('inf')
    for point in points:
        if point.coords[i] < min:
            min = point.coords[i]
    return min

def limit_dims(point,dims):
    temp_coords = []
    for dim in dims:
        temp_coords.append(point.coords[dim])
    new_point_line = [point.index]
    new_point_line.extend(temp_coords)
    p = Point(new_point_line)
    return p

def limit_all_dims(points,dims):
    point_copies = []
    for point in points:
        point_copies.append(limit_dims(point,dims))
    return point_copies


def max_dim(points,i):
    max = float('inf')
    for point in points:
        if point.coords[i] < min:
            min = point.coords[i]
    return max

#Finds minimum coordinates of all dimensions
def min_coords(points):
    coords = []
    dim = len(points[0].coords)
    for i in range(0,dim):
        coords.append(min_dim(points,i))
    return coords

#Returns max value of all dimensions
def max_coords(points):
    coords = []
    dim = len(points[0].coords)
    for i in range(0,dim):
        coords.append(max_dim(points,i))
    return coords

#Returns list of distances from point to all other points
def distances_from(point,points):
    distances = []
    for p in points:
        distances.append([p,euclidean(point.coords,p.coords)])
    return distances

#Returns list of square distances from point to all other points
def square_distances(point,points):
    distances = []
    for p in points:
        distances.append([p,np.square(euclidean(point.coords,p.coords))])
    return distances

#Returns farthest point (in points) from original point
def farthest_point(point,points):
    max_dist = 0
    f = None
    distances = distances_from(point,points)
    for item in distances:
        if item[1] > max_dist:
            max_dist = item[1]
            f = item[0]
    return [f,max_dist]

#Returns farthest point from current centers
def farthest_from_centers(centers, points):
    max_dist = 0
    f = None
    center_indices = [p.index for p in centers]
    for point in points:
        if point.index not in center_indices:
            closest_center = closest_point(point,centers)
            dist = closest_center[1]
            if dist > max_dist and dist < float('inf'):
                max_dist = dist
                f = point
    return f


#Returns closest point to current point (will not return itself)
def closest_point(point,points):
    min_dist = float('inf')
    c = None
    distances = distances_from(point,points)
    for item in distances:
        if item[0].index != point.index and item[1] < min_dist:
            min_dist = item[1]
            c = item[0]
    return [c,min_dist]

#Converts list of coordinates to points with dummy indices
def coords_to_points(coords):
    points = []
    for c in coords:
        t = [-1]
        t.extend(c)
        p = Point(t)
        points.append(p)
    return points

#Removes point from list l
def point_list_remove(l,point):
    for i in range(0,len(l)):
        if i < len(l):
            p = l[i]
            if p.index == point.index:
                del(l[i])

#Returns the index (in coords) of closest point
def index_closest_coords(point, coords):
    min_dist = float('inf')
    index = 0
    points = coords_to_points(coords)
    distances = distances_from(point,points)
    for i in range(0,len(distances)):
        item = distances[i]
        if item[1] < min_dist:
            min_dist = item[1]
            index = i
    return index

def index_closest_point(point, points):
    min_dist = float('inf')
    index = 0
    distances = distances_from(point,points)
    for i in range(0,len(distances)):
        item = distances[i]
        if item[1] < min_dist:
            min_dist = item[1]
            index = i
    return index





def get_points_from_list(l):
    points = []
    for item in l:
        p = Point(item)
        points.append(p)
    return points

#Gets list of points from path to file
def get_points_from_txt(path):
    points = []
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            p = Point(line.split())
            points.append(p)
    return points

#Returns centroid of list of coordinates by first converting them to points (with indices)
def get_centroid2(coords):
    dim = len(coords[0])
    points = coords_to_points(coords)
    return get_centroid(points)

#Returns centroid of list of points
def get_centroid(points):
    dim = len(points[0].coords)
    centroid = []
    i = 0
    while i < dim:
        centroid.append(average_dim(points, i))
        i += 1
    return centroid

#Returns the average value at dimension i in points
def average_dim(points, i):
    sum = 0.0
    count = 0
    for p in points:
        sum += p.coords[i]
        count += 1
    return sum / count

#Returns euclidean distance between to sets of coordinates. Dimensions must match
def euclidean(p1coords,p2coords):
    i = 0
    sum = 0
    while i < len(p1coords):
        sum += np.square(p1coords[i] - p2coords[i])
        i += 1
    return np.sqrt(sum)

#Returns the weighted probabilities proportional to distance for k-means++
def get_probabilities(c1,points):
    distances = square_distances(c1,points)
    sum_dist = 0
    for item in distances:
        sum_dist += item[1]
    return [item[1] / sum_dist for item in distances]

#Helper function for choosing random item with weighted probability
def cdf(weights):
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

#Choose random item with weighted probabilities
def choice(population, weights):
    assert len(population) == len(weights)
    cdf_vals = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]

#k-means++ algorithm for center initialization
def kMeansPlus(points,k):
    c1 = points[0]
    centers = []
    centers.append(c1)
    probs = get_probabilities(c1,points)
    for i in range(1,k):
        centers.append(choice(points,probs))
    return centers

#Gonzalez algorithm for center initialization
def gonzalez(points,k):
    centers = [points[0]]
    for i in range(1,k):
        f = farthest_from_centers(centers, points)
        centers.append(f)
    return centers



def keys_with_value(d,v):
    result = []
    for item in d.values():
        if item[0] == v:
            result.append(item)
    return result


def get_points_by_index(ids, points):
    result = []
    for p in points:
        if p.index in ids:
            result.append(p)
    return result


def reval_center(C, index, assigned):
    ids = keys_with_value(assigned, index)
    coords = [a[1] for a in ids]
    C[index] = get_centroid2(coords)


def lloyds(points,k,initializer):
    centers = initializer(points,k)
    assigned = {}
    C = [p.coords for p in centers]
    for p in points:
        closest_center = index_closest_coords(p, C)
        assigned[p.index] = [closest_center,p.coords]
        reval_center(C, closest_center, assigned)
    changed = True
    while(changed):
        changed = False
        for point in points:
            old = assigned[point.index][0]
            closest_center = index_closest_coords(point, C)
            if old != closest_center:
                assigned[point.index] = [closest_center,point.coords]
                reval_center(C, old, assigned)
                reval_center(C, closest_center, assigned)
                changed = True
    return coords_to_points(C)


def getMinDistance(set,d):
    min = float('inf')
    minP1 = -1
    minP2 = -1
    for p1 in d:
        p1Dict = d[p1]
        for p2 in p1Dict:
            distance = p1Dict[p2]
            if distance < min:
                min = distance
                minP1 = p1
                minP2 = p2
    return [min,minP1,minP2]


def getMaxDistance(set,d):
    max = -1
    maxP1 = -1
    maxP2 = -1
    for p1 in d:
        p1Dict = d[p1]
        for p2 in p1Dict:
            distance = p1Dict[p2]
            if distance > max:
                max = distance
                maxP1 = p1
                maxP2 = p2
    return [max,maxP1,maxP2]

single_link_dist = {}

def singleLink(c1,c2):
    min = float('inf')
    for p1 in c1:
        for p2 in c2:
            if p1.index in single_link_dist:
                if p2.index in single_link_dist[p1.index]:
                    e = single_link_dist[p1.index][p2.index]
                else:
                    e = euclidean(p1.coords,p2.coords)
                    single_link_dist[p1.index][p2.index] = e
            else:
                e = euclidean(p1.coords,p2.coords)
                d = {p2.index: e}
                single_link_dist[p1.index] = d
            if e < min:
                min = e
    return min


def completeLink(c1,c2):
    max = 0
    for p1 in c1:
        for p2 in c2:
            e = euclidean(p1.coords,p2.coords)
            if e > max:
                max = e
    return max


def meanLink(c1,c2):
    s1 = get_centroid(c1)
    s2 = get_centroid(c2)
    return euclidean(s1,s2)



def merge(clusters,closest_pair):
    a = closest_pair[0]
    b = closest_pair[1]
    clusters[a].extend(clusters[b])
    del(clusters[b])


def closestClusters(clusters,distance):
    closest_dist = float('inf')
    closest_pair = []
    for i in range(0,len(clusters)):
        c1 = clusters[i]
        for j in range(0,len(clusters)):
            c2 = clusters[j]
            if c1[0].index != c2[0].index:
                d = distance(c1,c2)
                if d < closest_dist:
                    closest_dist = d
                    closest_pair = [i,j]
    return closest_pair

def ave_dist(clusters):
    total = 0.0
    count = 0.0
    for c in clusters:
        for p1 in c:
            for p2 in c:
                total += euclidean(p1.coords,p2.coords)
                count += 1
    return total / count


def hierarchicalClustering(set,k,top_k,distance_func,feature_set,writer,path_name,player_dict):

    clusters = [[p] for p in set]
    while len(clusters) != k:
        merge(clusters,closestClusters(clusters,distance_func))
        print(len(clusters))
        if len(clusters) <= top_k:
            player_clusters = []
            for cluster in clusters:
                player_cluster = []
                for p in cluster:
                    id = p.index
                    player_cluster.append(player_dict[id])
                player_clusters.append(player_cluster)
            h.print_cluster_stats('Single-Link',len(clusters),player_clusters,feature_set,writer,path_name,player_dict)
    #print(ave_dist(clusters))
    return [[p.index for p in c] for c in clusters]


#k means cost function
def cost2(points,centers):
    sum = 0.0
    for i in range(0,len(points)):
        sum += np.square(euclidean(points[i].coords,closest_point(points[i],centers)[0].coords))
    return sum


#k median cost function
def cost1(centers,points):
    sum = 0.0
    count = 0.0
    for i in range(0,len(points)):
        sum += euclidean(points[i].coords,closest_point(points[i],centers)[0].coords)
        count += 1
    return sum / count

#k center cost function
def cost_inf(points,centers):
    max = 0.0
    for i in range(0,len(points)):
        d = euclidean(points[i].coords,closest_point(points[i],centers)[0].coords)
        if d > max:
            max = d
    return d

#Detailed center cost function??
def center_cost(centers,points):
    max_dist = 0
    for point in points:
        closest_center = closest_point(point,centers)
        dist = euclidean(point.coords,closest_center[0].coords)
        if dist > max_dist:
            max_dist = dist
    return max_dist

#Detailed means cost function
def means_cost(centers,points):
    sum = 0.0
    count = 0.0
    for point in points:
        closest_center = closest_point(point,centers)
        dist = euclidean(point.coords,closest_center[0].coords)
        sum += np.square(dist)
        count += 1
    return np.sqrt(sum / count)
