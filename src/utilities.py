import pickle
from typing import Any, Dict, List

import pandas as pd
import sweetviz as sv
import yaml


def eda_report(
    data: pd.DataFrame,
    filename: str,
    skip: list = None,
    force_cat: list = None,
    force_num: list = None,
    target: str = None,
) -> sv.DataframeReport:
    """
    Generate an Exploratory Data Analysis (EDA) report using Sweetviz.

    Args:
        data (DataFrame): The input DataFrame for analysis.
        filename (str): The filename (including path) to save the HTML report.
        skip (list, optional): List of column names to skip during analysis. Default is None.
        force_cat (list, optional): List of column names to force treat as categorical. Default is None.
        force_num (list, optional): List of column names to force treat as numerical. Default is None.
        target (str, optional): The target column for which analysis will be performed. Default is None.

    Returns:
        sv.DataframeReport: The Sweetviz DataframeReport object containing the analysis.

    """
    feat_cfg = sv.FeatureConfig(skip=skip, force_cat=force_cat, force_num=force_num)
    report = sv.analyze(data, target_feat=target, feat_cfg=feat_cfg)
    report.show_html(filepath=filename, open_browser=False)
    return report


def get_params(
    data: pd.DataFrame,
    feats: List[str],
    missings: List[str],
    target: str,
    categorical: List[str],
) -> Dict[str, Any]:
    """
    Get parameters for EDA reporter.

    Args:
        data (pd.DataFrame): The input DataFrame.
        feats (List[str]): List of feature columns.
        target (str): The target column.
        categorical (List[str]): List of categorical feature columns.
        binary (List[str]): List of binary feature columns.

    Returns:
        Dict[str, Any]: A dictionary containing the parameters:
            - "skip": list of features to skip
            - "force_cat": list of categorical features
            - "force_num": list of numerical features
            - "target": target column
    """
    skip_feat = list(set(data.columns) - set(feats) - {target})
    force_num = list((set(feats) - set(missings)) - set(categorical))
    force_cat = list((set(feats) & set(categorical)) - set(missings))
    params = {"skip": skip_feat, "force_cat": force_cat, "force_num": force_num, "target": target}

    return params


def get_config(filename: str = "config.yml") -> dict:
    """
    Read a YAML file and return its content as a dictionary.

    Args:
        filename (str): The path to the YAML file.

    Returns:
        dict: A dictionary containing the YAML content.
    """
    with open(filename, "r") as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content


def to_pickle(file, filename):
    """ "
    Saves given python object as binary file (handy to avoid problems with types etc)
    file: file object (e.g. dataframe)
    filename: saving destination (path + filename withou extention), str
    return: True (deafault)
    """
    if ".pkl" not in filename:
        filename = f"{filename}.pkl"
    with open(filename, "wb") as handle:
        pickle.dump(file, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return True


def from_pickle(filename):
    """ "
    Reads and returns a binary file
    filename: loading destination (path + filename withou extention), str
    return: python object (whatever was saved: dict, dataframe, etc)
    """
    if ".pkl" not in filename:
        filename = f"{filename}.pkl"
    with open(filename, "rb") as handle:
        file = pickle.load(handle)
    return file


import lime
import lime.lime_tabular
import matplotlib.pyplot as plt


def get_lime_explanation(dataset, pipeline, instance_index, num_features=5):
    """
    Generate a LIME explanation picture for a given instance in the dataset for regression tasks.

    Parameters:
        dataset (numpy array or pandas DataFrame): The dataset used for training the pipeline.
        pipeline (scikit-learn Pipeline): The trained scikit-learn pipeline.
        instance_index (int): Index of the instance in the dataset for which explanation is needed.
        num_features (int, optional): Number of features to include in the explanation. Default is 5.

    Returns:
        matplotlib figure: Lime explanation picture.
    """

    transformed = pipeline["preprocessor"].transform(dataset)

    numerical_features = pipeline.named_steps["preprocessor"].transformers_[0][2]
    categorical_features = pipeline.named_steps["preprocessor"].transformers_[1][2]
    feature_names = numerical_features + list(
        pipeline.named_steps["preprocessor"]
        .named_transformers_["cat"]
        .get_feature_names_out(categorical_features)
    )

    explainer = lime.lime_tabular.LimeTabularExplainer(
        transformed, feature_names=feature_names, mode="regression", discretize_continuous=False
    )

    instance = transformed[instance_index]
    explanation = explainer.explain_instance(
        instance, pipeline["regressor"].predict, num_features=num_features
    )

    fig = explanation.as_pyplot_figure()
    plt.close()

    return fig
