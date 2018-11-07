import os
import numpy as np
from scipy.spatial.distance import directed_hausdorff
import hdbscan

import pickle
from multiprocessing import Pool

cwd = os.path.dirname(os.path.realpath(__file__))

###############################################################################
save_dist_data = 0
save_cluster_data = 1

splines_save_location = "/data/splines.gpickle"
distances_save_location = "/data/distances.gpickle"
clusters_save_location = "/data/clusters.gpickle"
###############################################################################

###############################################################################


def multi_run_wrapper(args):
    return compute_distance(*args)


def compute_distance(i, j, u, v):
    return (i, j, directed_hausdorff(u, v)[0])
################################################################################


def organizer(distance_matrix):
    clusterer = hdbscan.HDBSCAN(metric='precomputed')
    clusterer.fit(distance_matrix)
    return clusterer.labels_


def main():

    # Bake or Read Data ########################################################
    n = 0

    if(save_dist_data == 1):
        print("Compute distances...")
        hair_strands = pickle.load(open(cwd + splines_save_location, "rb"))
        print("Loaded "+str(len(hair_strands)))

        n = len(hair_strands)

        data = []
        for i in range(n-1):
            for j in range(i+1, n):
                data.append([i, j, hair_strands[i], hair_strands[j]])

        pool = Pool()
        result = pool.map(multi_run_wrapper, data)

        distance_matrix = np.zeros([n, n])
        for e in result:
            distance_matrix[e[0], e[1]] = e[2]

        for i in range(n-1):
            for j in range(i+1, n):
                distance_matrix[j, i] = distance_matrix[i, j]

        print("Bake %: 100")
        pickle.dump(distance_matrix, open(cwd + distances_save_location, "wb"))
    else:
        distance_matrix = pickle.load(open(cwd + distances_save_location, "rb"))
        n = len(distance_matrix[0])
################################################################################

# Clusters #####################################################################
    print("\nCreating clusters...")

    clusters = []
    nested_clusters = []
    labels = organizer(distance_matrix)

    no_clusters = max(labels) + 1

    for i in range(no_clusters+1):
        clusters.append([])

    for id in range(n):
        clusters[labels[id]+1].append(id)

    print("Number of clusters: " + str(len(clusters)))

    for sel_cluster_id in range(len(clusters)):
        mn = len(clusters[sel_cluster_id])

        sel_distance_matrix = np.zeros([mn, mn])
        for i in range(mn):
            for j in range(mn):
                sel_distance_matrix[i, j] = distance_matrix[clusters[sel_cluster_id]
                                                            [i], clusters[sel_cluster_id][j]]

        print("\ncreating strands...")

        mini_clusters = []

        mini_labels = organizer(sel_distance_matrix)
        no_mclusters = max(mini_labels) + 1
        print("- number of strands: " + str(no_mclusters))
        print("")

        for i in range(no_mclusters+1):
            mini_clusters.append([])

        for id in range(mn):
            mini_clusters[mini_labels[id]+1].append(clusters[sel_cluster_id][id])

        nested_clusters.append(mini_clusters)

    if(save_cluster_data != 0):
        print("Save clusters data...")
        pickle.dump((clusters, nested_clusters), open(cwd + clusters_save_location, "wb"))
################################################################################


if __name__ == '__main__':
    main()
    print("\nEND")
