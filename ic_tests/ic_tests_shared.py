import numpy as np
import pandas as pd


def corr_one_day(df: pd.DataFrame, x: str, y: str, method: str):
    if len(df) > 2:
        res = df[[x, y]].corr(method=method).at[x, y]
    else:
        res = 0
    return 0 if np.isnan(res) else res
