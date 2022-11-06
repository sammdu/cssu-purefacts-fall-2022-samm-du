#!/usr/bin/env python3.10

import argparse
import csv
import numpy as np
import networkx as nx

from typing import Optional
from itertools import combinations
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import NearestNeighbors

# parse CLI arguments

ap = argparse.ArgumentParser()
ap.add_argument("input_file")
ap.add_argument(
    "-n",
    "--num-reps",
    required=True,
    help="Number of representative points to pick from the input data. Positive integer.",
)
ap.add_argument(
    "-a",
    "--algorithm",
    required=True,
    help="One of 'clustering', 'graph'.",
)
ap.add_argument(
    "-r",
    "--radius",
    required=False,
    help="If using 'graph' algorithm, select the max radius between connected points.",
)
ap.add_argument(
    "-b",
    "--branching-factor",
    required=False,
    help="If using 'graph' algorithm, select the branching factor for each point in the graph.",
)
ap.add_argument(
    "-o",
    "--output",
    required=True,
    help="Path to the output csv file. (e.g. output.csv)",
)
args: dict = vars(ap.parse_args())


# helper functions


def mean_of_points(points: list) -> tuple[float, float]:
    """
    Find the mean centroid for a list of points.
    Ref: https://stackoverflow.com/a/4355934
    """
    return (
        sum([p[0] for p in points]) / len(points),
        sum([p[1] for p in points]) / len(points),
    )


def point_distance(a: tuple[int, int], b: tuple[int, int]) -> float:
    """
    Return the Euclidean distance between two 2D input points.
    """
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** (1 / 2)


def points_1nn_to_centroids(input_data: list, centroids: list) -> set:
    """
    Return a set of input points closest to the given centroids.
    """
    knn = NearestNeighbors(n_neighbors=1).fit(input_data)
    neighbors_idxs = knn.kneighbors(centroids, n_neighbors=1, return_distance=False)

    return set(input_data[x[0]] for x in neighbors_idxs)


# point coverage algorithms


def hierarchical_clustering(input_data: list, num_reps: int) -> list:
    """
    Perform complete/max-linkage hierarchical clustering.
    Return the floating point mean centroids for each cluster.
    Doc: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html#sklearn.cluster.AgglomerativeClustering
    """

    hcluster = AgglomerativeClustering(n_clusters=num_reps, linkage="complete")
    hcluster.fit(input_data)

    hcluster_groups = [[] for i in range(num_reps)]
    for point, label in zip(input_data, hcluster.labels_):
        hcluster_groups[label].append(point)

    hcluster_centroids = []
    for group in hcluster_groups:
        hcluster_centroids.append(mean_of_points(group))

    return hcluster_centroids


def graph_disconnect(
    input_data: list, num_reps: int, max_radius: int, branching_factor: int
) -> list:
    """
    Construct a graph from input points, connect points within `max_radius` of each other,
    for up to `branching_factor` neighbors each point.
    Disconnect the largest edges by point distance, until the graph contains `num_reps`
    connected components.
    Return the floating point mean centroids for each connected component.
    """
    # create a graph of all points with their position as an attribute
    G = nx.Graph()
    for id, pos in enumerate(input_data):
        G.add_node(id, pos=pos)

    # Add edges between points within a certain radius, and limit the number of neighbors
    # each point can have
    # Ref: https://networkx.org/documentation/stable/_modules/networkx/generators/geometric.html#geometric_edges
    nodes_pos = G.nodes(data="pos")  # (node_id, (pos_x, pos_y)) for all nodes
    for (u, pu), (v, pv) in combinations(nodes_pos, 2):
        dist_sq = sum(abs(a - b) ** 2 for a, b in zip(pu, pv))
        if (
            (dist_sq <= max_radius**2)
            and (sum(1 for n in G.neighbors(u)) <= branching_factor)
            and (sum(1 for n in G.neighbors(v)) <= branching_factor)
        ):
            G.add_edge(u, v, dist=(dist_sq ** (1 / 2)))

    # sort all edges in the graph from short to long in a list
    edges_short_to_long = sorted(G.edges(data=True), key=lambda edge: edge[2]["dist"])

    # keep removing the largest edge from the graph, until the graph has num_reps
    # disconnected components
    while nx.number_connected_components(G) < num_reps:
        largest_edge = edges_short_to_long.pop()
        G.remove_edge(largest_edge[0], largest_edge[1])

    # compute and return centroids
    return [
        mean_of_points([input_data[i] for i in cluster])
        for cluster in nx.connected_components(G)
    ]


if __name__ == "__main__":
    # input file ingest and parameter configuration
    data = []
    with open(args["input_file"], "r") as input_file:
        csv_reader = csv.reader(input_file, delimiter=",")
        for line in csv_reader:
            data.append(tuple(int(x) for x in line))

    NUM_REPS = int(args["num_reps"])

    # find NUM_REPS coverage points for input data using the specified algorithm
    coverage_set: set
    coverage: list
    if args["algorithm"] == "clustering":
        hcluster_centroids = hierarchical_clustering(data, NUM_REPS)
        coverage_set = points_1nn_to_centroids(data, hcluster_centroids)
    elif args["algorithm"] == "graph":
        gd_centroids = graph_disconnect(
            data,
            NUM_REPS,
            int(r) if (r := args.get("radius")) else 6000,
            int(b) if (b := args.get("ranching_factor")) else 180,
        )
        coverage_set = points_1nn_to_centroids(data, gd_centroids)
    else:
        print("-a/--algorithm must be one of 'clustering' or 'graph'!")
        exit(1)
    coverage = list(coverage_set)

    # write chosen points to output file path
    with open(args["output"], "w") as output_file:
        csv_writer = csv.writer(output_file, delimiter=",")
        for point in coverage:
            csv_writer.writerow(point)
