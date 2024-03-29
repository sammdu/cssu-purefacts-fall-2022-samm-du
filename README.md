<h1 align="center">CSSU x Purefacts Programming Challange</h1>
<h2 align="center">Geometric Point Sampling Problem</h2>

# Table of Contents

0. [Problem statement](#0-problem-statement)
1. [Prepared outputs](#1-prepared-outputs)
2. [Usage](#2-usage)  
   2.0. [Prerequisites](#prerequisites)  
   2.1. [Python Script](#21-python-script)  
   2.1. [Jupyter Notebook](#22-jupyter-notebook)
3. [Analysis](#3-analysis)  
   3.1. [General Approach](#31-general-approach)  
   3.2. [Point Coverage Efficacy Evaluation](#32-point-coverage-efficacy-evaluation)  
   3.3. [Computational Performance](#33-computational-performance)  
   3.4. [Conclusion](#34-conclusion)

# 0. Problem statement

Given a set A of points in a 2D space ([input.csv](input.csv) - provided), select an `N` number of random Representative Points from this set such that they best "cover" the *shape* of the point set (as opposed to its density).

Output should be the source code and 5 separate `output.csv` files where `N` = 10, 25, 63, 159, 380

<p align="center">
<img height="300px" src="https://user-images.githubusercontent.com/10665890/213011187-de28dcc9-66b5-4e9f-9374-d28042da8fab.png" />

</p>

# 1. Prepared outputs

:eye: See the [outputs](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/tree/main/outputs) folder.

🥇 [hierarchical_clustering](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/tree/main/outputs/hierarchical_clustering) contains results generated using the **hierarchical clustering** approach. It has the best rep-rep/**average-distance** ratio, and perform more consistently across different N values. This is the preferred set of outputs.

🥈 [graph_disconnect](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/tree/main/outputs/graph_disconnect) contains results generated using the **graph-disconnect** approach. It has the best rep-rep/**max-distance** ratio on small N values only.

See [Analysis](#3-analysis) section for more details.

# 2. Usage

### Prerequisites

[Create a virtual environment](https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment) & install the required packages
This program requires `Python3.10` or above.

Please install the necessary packages in [`requirements.txt`](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/blob/main/requirements.txt).

```bash
pip install -r requirements.txt
```

```
jupyter==1.0.0
matplotlib==3.6.2
matplotlib-inline==0.1.6
networkx==2.8.8
numpy==1.23.4
scikit-learn==1.1.3
```

## 2.1. Python Script

👉 [point_coverage.py](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/blob/main/point_coverage.py)

### 🟩 Computing for a single N value:

The python program computes the required points for one N value.

```
usage: point_coverage.py [-h] [-v] -n NUM_REPS -a ALGORITHM [-r RADIUS] [-b BRANCHING_FACTOR] -o OUTPUT input_file

positional arguments:
  input_file

options:
  -h, --help            show this help message and exit
  -v, --verbose         When set, print analytics.
  -n NUM_REPS, --num-reps NUM_REPS
                        Number of representative points to pick from the input data. Positive integer.
  -a ALGORITHM, --algorithm ALGORITHM
                        One of 'clustering', 'graph'.
  -r RADIUS, --radius RADIUS
                        If using 'graph' algorithm, select the max radius between connected points.
  -b BRANCHING_FACTOR, --branching-factor BRANCHING_FACTOR
                        If using 'graph' algorithm, select the branching factor for each point in the graph.
  -o OUTPUT, --output OUTPUT
                        Path to the output csv file. (e.g. output.csv)
```

➡️ Example with clustering algorithm:

```bash
python3.10 ./point_coverage.py -v -n 10 -a clustering -o out_c.csv input.csv
```

➡️ Example with graph algorithm:

```bash
python3.10 ./point_coverage.py -v -n 10 -a graph -r 6000 -b 180 -o out_g.csv input.csv
```

### 🟩 Computing for all specified N values:

We can use the provided `run.sh` to produce output files for all N values specified in the handout:

```bash
bash ./run.sh <algorithm> <input-file>
```

The script will also time the execution for each N value round.

Output files will be generated in the current directory, named `output_<algorithm>_%d.csv`.

➡️ Example with clustering algorithm:

```bash
./run.sh clustering input.csv
```

```
Computing for N = 10
Took 0.39 seconds.

Computing for N = 25
Took 0.41 seconds.

Computing for N = 63
Took 0.39 seconds.

Computing for N = 159
Took 0.39 seconds.

Computing for N = 380
Took 0.39 seconds.
```

➡️ Example with graph algorithm:

```bash
./run.sh graph input.csv
```

```
Computing for N = 10
Took 49.95 seconds.

Computing for N = 25
Took 91.06 seconds.

Computing for N = 63
Took 96.84 seconds.

Computing for N = 159
Took 99.31 seconds.

Computing for N = 380
Took 98.65 seconds.
```

## 2.2. Jupyter Notebook

👉 [experiment.ipynb](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/blob/main/experiment.ipynb)

The Jupyter Notebook contains step-by-step computation and analysis, as well as scatter plots to visualize results.
Useful if you are interested in the details.
The same required packages apply.

You can view and edit Jupyter Notebooks on your own computer using [Visual Studio Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).
For online editing, feel free to check out [Google Colaboratory](https://colab.research.google.com/).

# 3. Analysis

The following three approaches to sampling N representatives from a collection of input points in order to attain optimal geometric coverage are evaluated:

-   k-Means Clustering
-   Hierarchical Clustering
-   Graph-Disconnect

Out of the three, only "Hierarchical Clustering" and "Graph-Disconnect" are deemed acceptable, and only "Hierarchical Clustering" performs consistently across many N values.

We will look at the three approaches in detail below.

> If you would like to follow along with the analysis, please feel free to check out the [Jupyter Notebook](#22-jupyter-notebook), as it provides step-by-step computation. You can even tweak parameters if you download the notebook to your local computer.

## 3.1. General Approach

### 3.1.1. Classic Clustering Algorithms

Initially, the given problem appeared to me as a [clustering problem](https://en.wikipedia.org/wiki/Cluster_analysis). For this type of approach, we group the input points into N clusters, then find the geometric centroids for each cluster, and pick the closest point to the centroid as a representative.

I have evaluated [various clustering algorithms](https://scikit-learn.org/stable/modules/clustering.html#clustering) provided by the [`Scikit-Learn`](https://scikit-learn.org/stable/index.html) library. We must exclude the algorithms that do not allow specifying the number of clusters in the output, because they are not suitable for the given problem.

#### k-Means Clustering

> [Read more](https://scikit-learn.org/stable/modules/clustering.html#k-means)

This algorithm is perhaps the most well-known unsupervised clustering algorithm, so naturally, it became my first candidate.

It starts by picking N random points as centroids, tries to absorb adjacent points, and recomputes the centroids. This process repeats until the centroids no longer move significantly across iterations.

The [KMeans function provided by `Scikit-Learn`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans) returns cluster centroids at the end of the algorithm, which are ready to be [converted to input data points](#313-processing-centroids).

#### Hierarchical/Agglomerative Clustering

> [Read more](https://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering)

This class of clustering algorithms either start with one cluster containing all input points, and divide them repeatedly until forming N clusters, or they start with each point in their own cluster, and merge clusters repeatedly until forming N final clusters. When the bottom-up merging approach is used, it's called [agglomerative clustering](https://en.wikipedia.org/wiki/Hierarchical_clustering).

I found most success with agglomerative clustering using maximum/complete linkage. Linkage is the criterion by which the algorithm decides which clusters are most "linked" to each other, in order to merge them. Maximum linkage refers to taking the maximum distance between all points in two clusters, and clusters who are closest by this maximum distance are merged together.

The [AgglomerativeClustering function provided by `Scikit-Learn`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html#sklearn.cluster.AgglomerativeClustering) does not return a collection of cluster centroids. It instead returns a collection of labels for each input data point describing which of the N clusters the data point belongs to. As a result, I grouped the input data by their cluster label, and computed a centroid for each cluster, so that they are ready to be [converted to input data points](#313-processing-centroids).

#### Other Clustering Algorithms

I have also evaluated [Spectral clustering](https://scikit-learn.org/stable/modules/clustering.html#spectral-clustering) and [BIRCH](https://scikit-learn.org/stable/modules/clustering.html#birch) for the purpose of the given problem, but they have produced underwhelming results, therefore I will not discuss them in more detail.

### 3.1.2. Graph Connectivity

Rather than using existing clustering algorithms, another approach to this problem can be described in terms of graph splitting, which I will refer to as "Graph-Disconnect".

Consider the following:

-   Create a graph containing all input data points as vertices
-   Connect all vertices to each other, with the edge weight being their Euclidean distance.
-   Repeatedly remove the largest edge from the graph, until there are N connected components in the graph left
-   Compute the mean centroids for all vertices in each connected component

In order to build and operate on such a graph, I used the [NetworkX](https://networkx.org/documentation/stable/index.html) library.

The initial attempt following the steps described above suffered from major performance issues. The number of edges are exponential to the number of input data points, and the process of removing edges until N components are formed was taking in excess of 10 minutes, with no results.

To optimize performance, I first tried to use the [`geometric_edges`](https://networkx.org/documentation/stable/reference/generated/networkx.generators.geometric.geometric_edges.html#geometric-edges) function provided by the NetworkX library. It connects vertices that are within a certain radius of each other, which reduces the number of edges in the final graph. However, the resulting graph still contains way too many edges, since the input data contains dense regions with many points in a close distance from each other.

To further optimize performance, I modified the [source code of the `geometric_edges` function](https://networkx.org/documentation/stable/_modules/networkx/generators/geometric.html#geometric_edges) to also include a branching factor constraint. The branching factor is the number of edges that can be incident from a vertex (a.k.a. the size of the neighborhood). This allows the graph to remain reasonably sized even in dense regions of the input data.

The final optimization allowed the Graph-Disconnect algorithm to successfully complete within a few minutes. For the given input data, I found that a radius constraint of `6000` and branching factor constraint of `180` produces optimal results. However, these constraints will be different depending on the input data, and there are no trivial ways to compute them automatically.

### 3.1.3. Processing Centroids

The centroids returned from clustering are not part of the input dataset. We must find input data points that are closest to these centroids as points that represent their region ("reps"), in order to form the final output.

[Nearest neighbors algorithms](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors) are well suited for this task, as it tries to find k input points closest to a given set of reference points. The `Skikit-Learn` library [provides such a function](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html#sklearn-neighbors-nearestneighbors). For our purpose, we find the 1 nearest neighbor from the input data to each of the computed centroids, which we return as representatives.

## 3.2. Point Coverage Efficacy Evaluation

### 3.2.1. Visual Inspection

In the following plots:

-   dark gray points are input data
-   blue points are floating-point centroids
-   red points are input points chosen as representatives, which are closest to the blue centroids

For the Graph-Disconnect algorithm, the radius is chosen to be `6000`, and branching factor is chosen to be `180`.

#### Scatter Plots for N=10

<table>
	<tbody>
		<tr>
			<th>k-Means</th>
			<td width="610"><img width="600" src="https://user-images.githubusercontent.com/10665890/200195614-6fedbc0f-f571-4210-a3a5-8ee012d7185d.png" />
</td>
			<td width="200">The reps appear to be concentrated in dense areas, rather than across the geometric span of the input points. </td>
		</tr>
		<tr>
			<th>Hierarchical</th>
			<td width="610"><img width="600" src="https://user-images.githubusercontent.com/10665890/200195739-91771e63-7779-469b-849c-ff575156a582.png" /></td>
			<td width="200">The reps are reasonably distributed across the geometric region of the input points, with a few outlier points being far from a rep.</td>
		</tr>
		<tr>
			<th>Graph-Disconnect</th>
			<td width="610"><img width="600" src="https://user-images.githubusercontent.com/10665890/200195751-54fa0a7b-0a86-44fc-b16e-b3b11f59dafc.png" /></td>
			<td width="200">The reps are dipersed far from each other, and most outlier points are close to a rep.</td>
		</tr>
	</tbody>
</table>

#### Scatter Plots for N=63

<table>
	<tbody>
		<tr>
			<th>k-Means</th>
			<td width="610"><img width="600" src="https://user-images.githubusercontent.com/10665890/200196227-229fa08b-f73d-41c7-8e10-ae0805b21553.png" />
</td>
			<td width="200">k-Means continues to favor dense regions, with many points on the exterior far from a rep.</td>
		</tr>
		<tr>
			<th>Hierarchical</th>
			<td width="610"><img width="600" src="https://user-images.githubusercontent.com/10665890/200196234-de078cfa-72ce-4aa0-923d-d392c526008f.png" /></td>
			<td width="200">Even coverage across the geometric span of the input data, with both dense and sparse regions reasonably covered. Few points are far from a rep.</td>
		</tr>
		<tr>
			<th>Graph-Disconnect</th>
			<td width="610"><img width="600" src="https://user-images.githubusercontent.com/10665890/200196241-ca5f4fdd-6c6e-490d-8018-925d4ffd30b7.png" /></td>
			<td width="200">Outlier points seem to be favored over densely congregated points. Many points in dense regions are not covered by an adjacent rep.</td>
		</tr>
	</tbody>
</table>

### 3.2.2. Quantitative Measures

I will discuss 4 ways to evaluate the point coverage for each of the three approaches described above.

#### 3.2.2.1. Naive Total Distance to Reps

-   Take all points in the input data, compute their distance to every selected rep point, and take the total sum.
-   For optimal point coverage, unselected points should be as close to rep points as possible. The total of such distances is therefore a general measure of how close are points to reps throughout the dataset.
-   Small values in this metric are desireable.
-   However, this metric favors dense input point distributions, since for dense inputs, more points will be closer to reps compared to sparse inputs.

#### 3.2.2.2. Distances to Closest Rep Points

-   Take all points not selected as a rep, find their closest rep, compute their distance. Take all these distances to the closest rep, and find the max, min, and average.
-   For optimal point coverage, unselected points should be as close to their rep as possible. This improves upon the naive total distance measure, by focusing on reps that are supposed to cover points in their region.
-   Small values in this metric are desireable.

#### 3.2.2.3. Closest Distance Between Reps

-   Take all points chosen as reps, find the minimum distance between any 2 reps.
-   For optimal point coverage, the selected reps should be as far from each other as possible, so that each rep can cover as many unselected points as possible.
-   Large values in this metric are desireable.

#### 3.2.2.4. Min-Rep-Rep to Point-Rep Ratios

-   The ratio of previous two measures ("3.2.2.3. closest distance between reps" and "3.2.2.2. max|average distance from a point to a rep")
-   The greater this ratio, the farthest apart are reps to each other, and closer the unselected points to a rep.
-   Large values in this ratio are desireable.
-   The min distance between reps to max distance from point to rep (`rr/max`) is a summary measure of point coverage in the worst case, and favors outlier input points.
-   The min distance between reps to average distance from point to rep (`rr/avg`) is a summary measure of point coverage in the average case, and should be considered the optimal measure.

### 3.2.3. Comparing Efficacy Quantitatively

#### Compare all metrics on N=10

<table>
    <thead>
    <tr>
			<th>Algorithm</th>
			<th colspan="3">k-Means</th>
			<th colspan="3">Hierarchical</th>
			<th colspan="3">Graph-Disconnect</th>
		</tr>
    </thead>
	<tbody>
		<tr>
			<td>Total<br>Distance</td>
			<td colspan="3">29272141.3949</td>
			<td colspan="3">34850046.2278</td>
			<td colspan="3">37936438.9315</td>
		</tr>
		<tr>
			<td rowspan="2">Dist-Rep</td>
			<td>Min</td>
			<td>Max</td>
			<td>Avg</td>
			<td>Min</td>
			<td>Max</td>
			<td>Avg</td>
			<td>Min</td>
			<td>Max</td>
			<td>Avg</td>
		</tr>
		<tr>
			<td>7.2111</td>
			<td>3246.6056</td>
			<td>525.7065</td>
			<td>43.8406</td>
			<td>1976.1905</td>
			<td>639.4779</td>
			<td>59.4811</td>
			<td>2120.6284</td>
			<td>895.2549</td>
		</tr>
		<tr>
			<td>Rep-Rep</td>
			<td colspan="3">997.0245</td>
			<td colspan="3">1411.0978</td>
			<td colspan="3">1880.5130</td>
		</tr>
		<tr>
			<td rowspan="2">Ratio</td>
			<td>rr/max</td>
			<td>rr/avg</td>
			<td rowspan="2">Worst</td>
			<td>rr/max</td>
			<td>rr/avg</td>
			<td rowspan="2">Best Average</td>
			<td>rr/max</td>
			<td>rr/avg</td>
			<td rowspan="2">Best Max</td>
		</tr>
		<tr>
			<td>0.3071</td>
			<td>1.8965</td>
			<td>0.7140</td>
			<td>2.2066</td>
			<td>0.8868</td>
			<td>2.1005</td>
		</tr>
	</tbody>
</table>

As we can see, the k-Means approach does not live up to standard both visually and quantitatively, as it is too biased toward point density, and produces suboptimal rep-rep/dist-rep ratios.

We will exclude k-Means from now on and focus on the other two methods.

#### Compare ratios for all given N values

<table>
	<tbody>
		<tr>
			<th>Algorithm</th>
			<th colspan="2">Hierarchical</th>
			<th colspan="2">Graph-Disconnect</th>
		</tr>
		<tr>
			<th>N</th>
			<th>rr/avg</th>
			<th>rr/max</th>
			<th>rr/avg</th>
			<th>rr/max</th>
		</tr>
		<tr>
			<td>10</td>
			<td>2.2066</td>
			<td>0.7140</td>
			<td>2.1005</td>
			<td>0.8868</td>
		</tr>
		<tr>
			<td>25</td>
			<td>1.5561</td>
			<td>0.6281</td>
			<td>0.2790</td>
			<td>0.1034</td>
		</tr>
		<tr>
			<td>63</td>
			<td>1.1474</td>
			<td>0.3402</td>
			<td>0.1688</td>
			<td>0.0426</td>
		</tr>
		<tr>
			<td>159</td>
			<td>0.9536</td>
			<td>0.3582</td>
			<td>0.2131</td>
			<td>0.0779</td>
		</tr>
        <tr>
			<td>380</td>
			<td>1.1536</td>
			<td>0.4710</td>
			<td>0.1439</td>
			<td>0.0456</td>
		</tr>
	</tbody>
</table>

We can see that, for both Hierarchical Clustering and Graph-Disconnect, their efficacy ratios seem to decrease with larger N values.

For N=10, Graph-Disconnect has superior worst-case coverage, while Hierarchical Clustering has superior average-case coverage.

For N>10, Graph-Disconnect suffers from a sharp drop in efficacy ratios, while Hierarchical Clustering continues to perform consistently well, and beats Graph-Disconnect on all measures.

> It is worth nothing that, in my trials, the coverage efficacy of Graph-Disconnect is highly influenced by its performance constraint parameters (radius and branching factor). Increasing these parameters tend to improve coverage ratios, but will cause exponential performance degradation. For large N, I have not found performance parameters that allow Graph-Disconnect to outperform Hierarchical Clustering in coverage while completing in a practical amount of time.

In summary, Hierarchical Clustering produces better point coverage for scenarios.

## 3.3. Computational Performance

The following are recorded execution times for both algorithms on the same computer, measured in seconds.

For the Graph-Disconnect algorithm, the radius is chosen to be `6000`, and branching factor is chosen to be `180`. These parameters have a significant impact of the execution time of the algorithm.

<table>
	<tbody>
		<tr>
			<th>N</th>
			<th>Hierarchical</th>
			<th>Graph-Disconnect</th>
		</tr>
		<tr>
			<td>10</td>
			<td>0.41</td>
			<td>49.89</td>
		</tr>
		<tr>
			<td>25</td>
			<td>0.44</td>
			<td>86.59</td>
		</tr>
		<tr>
			<td>63</td>
			<td>0.49</td>
			<td>92.02</td>
		</tr>
		<tr>
			<td>159</td>
			<td>0.60</td>
			<td>96.90</td>
		</tr>
		<tr>
			<td>380</td>
			<td>0.82</td>
			<td>96.15</td>
		</tr>
	</tbody>
</table>

As seen here, Hierarchical Clustering is far superior to Graph-Disconnect when it comes to computational performance.

## 3.4. Conclusion

Across different approaches to selecting representative points for optimal point coverage given a collection of input points, **Hierarchical Clustering** is overwhelmingly successful, both in terms of coverage metrics, and in computational performance.

The only case to favor Graph-Disconnect is for very small N values, and if long execution times are acceptable.
