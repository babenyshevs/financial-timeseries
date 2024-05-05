import pandas as pd


def split_train_test_ts(
    df: pd.DataFrame, datetime_column: str = "date", train_size: float = 0.8
) -> tuple:
    """
    Split a DataFrame into train and test sets based on the datetime column.

    Parameters:
    - df: DataFrame containing the datetime column.
    - datetime_column: Name of the datetime column.
    - train_size: Percentage of data to be included in the training set (default is 0.8).

    Returns:
    - train_set: DataFrame containing the training set.
    - test_set: DataFrame containing the test set.
    """
    df_sorted = df.sort_values(datetime_column)

    dates = df_sorted[datetime_column].dt.date.unique()

    num_days_train = int(train_size * len(dates))

    train_dates = dates[:num_days_train]
    test_dates = dates[num_days_train:]

    train_set = df_sorted[df_sorted[datetime_column].dt.date.isin(train_dates)]
    test_set = df_sorted[df_sorted[datetime_column].dt.date.isin(test_dates)]

    return train_set, test_set
