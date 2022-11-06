# cssu-purefacts-fall-2022-samm-du

# Table of Contents

1. [Prepared outputs](#1-prepared-outputs)
2. [Usage](#2-usage)  
   2.0. [Prerequisites](#prerequisites)  
   2.1. [Python Script](#21-python-script)  
   2.1. [Jupyter Notebook](#22-jupyter-notebook)
3. [Analysis](#3-analysis)

# 1. Prepared outputs:

:eye: See the [outputs](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/tree/main/outputs) folder.

👉 [graph_disconnect](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/tree/main/outputs/graph_disconnect) contains results generated using the **graph-disconnect** approach. It has the best rep-rep/**max-distance** ratio. See [Analysis](#3-analysis) section for more details.

👉 [hierarchical_clustering](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/tree/main/outputs/hierarchical_clustering) contains results generated using the **hierarchical clustering** approach. It has the best rep-rep/**average-distance** ratio. See [Analysis](#3-analysis) section for more details.

# 2. Usage

### Prerequisites

Create a virtual environment & install the required packages
This program requires `Python3.10` or above.

Please install the necessary packages in [`requirements.txt`](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/blob/main/requirements.txt).

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
usage: point_coverage.py [-h] -n NUM_REPS -a ALGORITHM [-r RADIUS] [-b BRANCHING_FACTOR] -o OUTPUT input_file

positional arguments:
  input_file

options:
  -h, --help            show this help message and exit
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
python3.10 ./point_coverage.py -n 10 -a clustering -o out.csv input.csv
```

➡️ Example with graph algorithm:

```bash
python3.10 ./point_coverage.py -n 10 -a graph -r 6000 -b 180 -o out_g.csv input.csv
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

The Jupyter Notebook contains step-by-step computation and analysis.
Useful if you are interested in the details.
The same required packages apply.

# 3. Analysis

⚠️ TBD
