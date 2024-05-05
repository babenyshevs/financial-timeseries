import matplotlib.pyplot as plt


def plot_line(df, x, y, title="Time Series Plot"):
    """
    Plot a line using Matplotlib.

    Parameters:
        df (DataFrame): DataFrame containing time series data.
        x (str): Name of the column containing dates.
        y (str): Name of the column containing values.
        title (str): Title of the plot (default is 'Time Series Plot').
        x_label (str): Label for the x-axis (default is 'Date').
        y_label (str): Label for the y-axis (default is 'Value').
    """
    plt.figure(figsize=(15, 5))
    plt.plot(df[x], df[y])
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    plt.show()
