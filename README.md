# cssu-purefacts-fall-2022-samm-du

## 1. Prepared outputs:
:eye: See the [outputs](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/tree/main/outputs) folder.

## 2. Usage

#### Create a virtual environment & install the required packages

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

### 2.1. Python Script

👉 [point_coverage.py](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/blob/main/point_coverage.py)

#### Computing for a single N value:

The python program computes the required points for one N value, as such:

```
usage: point_coverage.py [-h] -n NUM_REPS -o OUTPUT input_file
```

Example:

```bash
python3.10 point_coverage.py -n 10 -o output.csv input.csv
```

#### Computing for all specified N values:

We can use the provided `run.sh` to produce output files for all N values specified in the handout:

```bash
bash ./run.sh input.csv
```

Output files will be generated in the current directory, named `output_%d.csv`.

### 2.2. Jupyter Notebook

👉 [experiment.ipynb](https://github.com/sammdu/cssu-purefacts-fall-2022-samm-du/blob/main/experiment.ipynb)

The Jupyter Notebook contains step-by-step computation and analysis.
Useful if you are interested in the details.
The same required packages apply.

## 3. Analysis

⚠️ TBD
