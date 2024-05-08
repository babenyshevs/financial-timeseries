financial-time-series-prediction
==============================

EDA, showcasing different apporaches for time series forecast

## What's done:
- stationariness analysis
- EDA (multivariate analysis)
- baseline Time series pridctions with SARIMAX

## Work in progress
- prediction with sequantial models


Comments to the task
------------
## I
**SBA: TL;DR: Task description seems to be mixture of dataset description (columns, idecies and their meanings) and description of how this dataset is collected, i.e. order in which data arrive from traiding platform (or whatever is a source). Clarification is needed.**

1. Index is a CE(S)T-localized (**SBA: removed it below to make text more readable**) DatetimeIndex in hourly resoluton startng from 2023-01-16 01:00 to 2023-09-25 00:00. It represents the target time (**SBA: why *target* time? Is it different from *feature* time?**) but is not necessarily contiguous.
2. It has 6048 rows.
3. It has 34 columns:
    1. 30 columns named *x01* … *x30* are features known at prediction time.
    2. 1 column named *y* is the target variable not known at prediction time, corresponding to the dataset’s index, a.k.a. the target time.
    3. column named *x_y_lagged* is also a feature and represents a lagged value of the target variable *y* known at prediction time.
    4. column named *z* is neither a feature nor a target variable, but a helper column to calculate our evaluation metric, as explained later. It is not known at prediction time and therefore must not be used during modelling, only when evaluating the model.
    5. 1 column *x_z_lagged* is also a feature and represents a lagged value of helper column *z* known at prediction time.

## II
To reiterate, the dataset has three types of columns:
1. 32 features known at prediction time, named *x01* … *x30*, *x_y_lagged*, and *x_z_lagged*.
2. 1 target variable not known at prediction time named *y*.
3. 1 additional helper column named *z*, which is not a feature nor a target variable, and is *not known at prediction time* and should no be used during modelling, only when evaluating the model.

## III
The dataset contains a multi-dimensional timeseries, but it is not a conventional timeseries. Target variables have to be predicted in batches but their realized value is known after their target times (**SBA: Target, when it comes to training data, is a *realized value*. Otherwise it's not a target. Perhaps, here *target* is used in some other meaning.**). This happens according to the below schedule:
1. On day D-1 at 11:30, prediction is done at once for the below 24 hours (**SBA: hereinafter *prediction window* for short**):
    1. Day *D 01:00 - D 23:00*
    2. Day *D+1 00:00*
2. Then on the same day *D-1 13:00*, the 24 realized *z* helper column values for day *D 01:00 … D+1 00:00* are published at once. This means that realized *z* values are not known as the target time (hours) pass one after another, but they are known the day before (**SBA: the day before WHAT? Day D? It's not entirely true, because as 1st sentence states they are published at 13:00 (not 00:00)**) (for target time day D+2 00:00, two days before). (**SBA: *z* values are published for *D 01:00 … D+1 00:00*. Which D+2?**)
3. However, target variable *y* values are known one by one some time (**SBA: how much is "some time"?**) after the target time (hour) is passed (**SBA: What's the definition of target time? Expected that *target time* is when we know the value of a target.**).
4. This batch dynamic can be seen when looking at the values of *x_y_lagged* as compared to *y*, and the values of *x_z_lagged* as compared to *z*. (**SBA: According to data *y*<sub>D</sub> == *x_y_lagged*<sub>D+2</sub>. Quite straightforward.**)
5. This schedule needs to be taken into consideration to correctly use lagged values of other features, as illustrated by the following:
    1. On day D (**SBA: typo? it should be D-1 according to section III, 1**) at prediction time, all 32 feature values corresponding to the 24 to-be-predicted hours day D 01:00 … day D+1 00:00 are available and known at once. (**SBA: those 32 feature values are for timestamp D-1 11:30. What about other 23 hours?**)
    2. This means that for a given feature *x* corresponding to target time day *D* hour *n*, not only “past” lagged values from before day *D* hour *n-1* could be used, but also “future” lagged values from day *D* hour *n+1* to day *D+1 00:00*, but not further, because feature *x*’s value corresponding to day *D+1 01:00* and beyond is not known at prediction time on day *D-1.*
    3. Of course, given the batch nature of the underlying timeseries, these “future” values are not actually future values but are known at prediction time.
    4. Just to reiterate, the above is true for *x_y_lagged* and *x_z_lagged* as they are features, but is not the case for *y* and *z*.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model summaries (MLFlow artifacts)
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-sba-initial-data-exploration`.
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

for windows use

    .venv/Scripts/activate

for mac use
    
    source .venv/bin/activate

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
