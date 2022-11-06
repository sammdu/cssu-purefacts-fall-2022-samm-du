#!/usr/bin/env python3.10
import point_coverage as pc


def data_to_rep_total_dist(input_data: list, reps: list) -> float:
    """
    Return the sum of all distances from a point to all reps.
    """
    distance_sum = 0
    for i in input_data:
        for j in reps:
            distance_sum += pc.point_distance(i, j)
    return distance_sum


def dists_to_closest_rep(input_data: list, reps) -> tuple[float, float, float]:
    """
    Return min, max, average of distances from all points to a closest rep.
    """
    dists_to_closest_rep = []
    for point in input_data:
        if point not in reps:
            closest_rep = min(reps, key=lambda rep: pc.point_distance(point, rep))
            dists_to_closest_rep.append(pc.point_distance(point, closest_rep))
    return (
        min(dists_to_closest_rep),
        max(dists_to_closest_rep),
        (sum(dists_to_closest_rep) / len(dists_to_closest_rep)),
    )


def min_dist_between_reps(reps) -> float:
    """
    Return the minimum distance between all rep points.
    """
    dist = float("inf")
    for i in reps:
        for j in reps:
            if i != j and (dist_self := pc.point_distance(i, j)) < dist:
                dist = dist_self
    return dist
