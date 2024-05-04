financial-time-series-prediction
==============================

EDA, showcasing different apporaches for time series forecast

Dataset
------------
**Its index** is a CE(S)T-localized DatetimeIndex in hourly resoluton startng from 2023-01-16 01:00 to 2023-09-25 00:00. It represents the target tme but is not necessarily contiguous.
- It has 6048 rows.
- It has 34 columns:
  - 30 columns named x01 … x30 are features known at prediction time.
  - 1 column named y is the target variable not known at prediction time,
corresponding to the dataset’s index, a.k.a. the target time.1 column named x_y_lagged is also a feature and represents a lagged value of the target variable y known at prediction time.
  - 1 column named z is neither a feature nor a target variable, but a helper column to calculate our evaluation metric, as explained later. It is not known at prediction time and therefore must not be used during modelling, only when evaluating the model.
  - 1 column x_z_lagged is also a feature and represents a lagged value of helper column z known at prediction time.

**To reiterate**, the dataset has three types of columns:
  - 32 features known at prediction time, named x01 … x30, x_y_lagged, and
x_z_lagged.
  - 1 target variable not known at prediction time named y.
  - 1 additional helper column named z, which is not a feature nor a target variable, and is not known at prediction time and should no be used during modelling, only when evaluating the model.

**The dataset** contains a multi-dimensional timeseries, but it is not a conventional timeseries. Target variables have to be predicted in batches but their realized value is known after their target times. This happens according to the below schedule:
  - On day D-1 at 11:30 CE(S)T, prediction is done at once for the below 24 hours (**SBA: of a next day, I assume?**):
    - Day D 01:00 … day D 23:00
    - Day D+1 00:00
o Then on the same day D-1 at 13:00 CE(S)T, the 24 realized z helper column values
for day D 01:00 … day D+1 00:00 are published at once. This means that realized
z values are not known as the target time (hours) pass one after another, but
they are known the day before (for target time day D+2 00:00, two days before).
o However, target variable y values are known one by one some time after the
target time (hour) is passed.
o This batch dynamic can be seen when looking at the values of x_y_lagged as
compared to y, and the values of x_z_lagged as compared to z.
o This schedule needs to be taken into consideration to correctly use lagged values
of other features, as illustrated by the following:
 On day D at prediction time, all 32 feature values corresponding to the 24
to-be-predicted hours day D 01:00 … day D+1 00:00 are available and
known at once.
 This means that for a given feature x corresponding to target time day D
hour n, not only “past” lagged values from before day D hour n-1 could be
used, but also “future” lagged values from day D hour n+1 to day D+1
00:00, but not further, because feature x’s value corresponding to day
D+1 01:00 and beyond is not known at prediction time on day D-1.
Page 3 of 4
 Of course, given the batch nature of the underlying timeseries, these
“future” values are not actually future values but are known at prediction
time.
 Just to reiterate, the above is true for x_y_lagged and x_z_lagged as they
are features, but is not the case for y and z.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

# How to create a project with coockie *cutter data science*

    cookiecutter https://github.com/babenyshevs/ccds-custom.git --checkout windows

# Steps to follow after creating a project
## create and activate virtual environment

    python -m venv .venv
    .venv/Scripts/activate

## create GIT repo

    git init
    git add .
    git commit -m "default initial commit"

## checkout develop branch (optional)

    git checkout -b develop

## install requirements

    python -m pip install -U pip setuptools wheel
    python -m pip install -r requirements.txt

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
