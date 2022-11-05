#!/usr/bin/env python3.10

import argparse
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

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
    "-o",
    "--output",
    required=True,
    help="Path to the output csv file. (e.g. output.csv)",
)
args: dict = vars(ap.parse_args())

# input file ingest and parameter configuration
data = []
with open(args["input_file"], "r") as input_file:
    csv_reader = csv.reader(input_file, delimiter=",")
    for line in csv_reader:
        data.append(tuple(int(x) for x in line))

NUM_REPS = int(args["num_reps"])


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


# perform complete/max hierarchical clustering

hcluster = AgglomerativeClustering(n_clusters=NUM_REPS, linkage="complete")
hcluster.fit(data)

hcluster_groups = [[] for i in range(NUM_REPS)]
for point, label in zip(data, hcluster.labels_):
    hcluster_groups[label].append(point)

hcluster_centroids = []
for group in hcluster_groups:
    hcluster_centroids.append(mean_of_points(group))


# find input data points closest to cluster centroids

knn = NearestNeighbors(n_neighbors=1).fit(data)
hcluster_neighbors_idx = knn.kneighbors(
    hcluster_centroids, n_neighbors=1, return_distance=False
)
hcluster_closest_points_set = set(data[x[0]] for x in hcluster_neighbors_idx)
hcluster_closest_points = list(hcluster_closest_points_set)


# write chosen points to output file path
with open(args["output"], "w") as output_file:
    csv_writer = csv.writer(output_file, delimiter=",")
    for point in hcluster_closest_points:
        csv_writer.writerow(point)
