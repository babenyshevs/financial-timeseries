from typing import Tuple

import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss


def adf_test(timeseries: pd.Series) -> None:
    """
    Perform Augmented Dickey-Fuller test for stationarity.

    The Augmented Dickey-Fuller (ADF) test is used to determine whether a given time series
    is stationary or not. The null hypothesis of the ADF test is that the time series has
    a unit root, indicating it is non-stationary. The alternative hypothesis suggests
    stationarity. The test statistic is compared to critical values at certain confidence
    levels to determine the result.

    Parameters:
        timeseries (pd.Series): A time series to be tested for stationarity.

    Returns:
        None: Prints the results of the Dickey-Fuller test along with indication of
        whether the null hypothesis should be rejected.
    """
    print("Results of Augmented Dickey-Fuller test:")
    dftest: Tuple[float, float, int, dict] = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(
        dftest[0:4],
        index=["Test Statistic", "p-value", "#Lags Used", "Number of Observations Used"],
    )

    # Interpretation
    if dfoutput["p-value"] < 0.05:
        print("H0 is rejected (time series is stationary)")
    else:
        print("H0 is not rejected (time series is non-stationary)")

    print(dfoutput)


def kpss_test(timeseries: pd.Series) -> None:
    """
    Perform Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test for stationarity.

    The KPSS test is used to determine whether a given time series is stationary
    around a deterministic trend. The null hypothesis of the KPSS test is that
    the time series is stationary. The alternative hypothesis suggests the presence
    of a unit root.

    Parameters:
        timeseries (pd.Series): A time series to be tested for stationarity.

    Returns:
        None: Prints the results of the KPSS test along with indication of
        whether the null hypothesis should be rejected.
    """
    print("Results of KPSS Test:")
    kpsstest: Tuple[float, float, int, dict] = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"])

    # Interpretation
    if kpss_output["p-value"] < 0.05:
        print("H0 is rejected (time series is non-stationary)")
    else:
        print("H0 is not rejected (time series is stationary)")

    print(kpss_output)
