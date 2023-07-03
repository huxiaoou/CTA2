import numpy as np
import pandas as pd
import scipy.stats as sps
from itertools import product
import subprocess


# -------------------------------------------
# --- Part I: factor exposure calculation ---


def cal_rolling_corr(t_major_return_df: pd.DataFrame, t_x: str, t_y: str, t_rolling_window: int, t_corr_lbl: str):
    t_major_return_df["xy"] = (t_major_return_df[t_x] * t_major_return_df[t_y]).rolling(window=t_rolling_window).mean()
    t_major_return_df["xx"] = (t_major_return_df[t_x] * t_major_return_df[t_x]).rolling(window=t_rolling_window).mean()
    t_major_return_df["yy"] = (t_major_return_df[t_y] * t_major_return_df[t_y]).rolling(window=t_rolling_window).mean()
    t_major_return_df["x"] = t_major_return_df[t_x].rolling(window=t_rolling_window).mean()
    t_major_return_df["y"] = t_major_return_df[t_y].rolling(window=t_rolling_window).mean()

    t_major_return_df["cov_xy"] = t_major_return_df["xy"] - t_major_return_df["x"] * t_major_return_df["y"]
    t_major_return_df["cov_xx"] = t_major_return_df["xx"] - t_major_return_df["x"] * t_major_return_df["x"]
    t_major_return_df["cov_yy"] = t_major_return_df["yy"] - t_major_return_df["y"] * t_major_return_df["y"]

    t_major_return_df.loc[np.abs(t_major_return_df["cov_xx"]) <= 1e-8, "cov_xx"] = 0
    t_major_return_df.loc[np.abs(t_major_return_df["cov_yy"]) <= 1e-8, "cov_yy"] = 0

    t_major_return_df["sqrt_cov_xx_yy"] = np.sqrt(t_major_return_df["cov_xx"] * t_major_return_df["cov_yy"]).fillna(0)
    t_major_return_df[t_corr_lbl] = t_major_return_df[["cov_xy", "sqrt_cov_xx_yy"]].apply(
        lambda z: 0 if z["sqrt_cov_xx_yy"] == 0 else -z["cov_xy"] / z["sqrt_cov_xx_yy"], axis=1)
    return 0


def transform_dist(t_exposure_srs: pd.Series):
    """

    :param t_exposure_srs:
    :return: remap an array of any distribution to the union distribution
    """

    return sps.norm.ppf(t_exposure_srs.rank() / (len(t_exposure_srs) + 1))


def neutralize_by_sector(t_raw_data: pd.Series, t_sector_df: pd.DataFrame, t_weight=None):
    """

    :param t_raw_data: A pd.Series with length = N. Its value could be exposure or return.
    :param t_sector_df: A 0-1 matrix with size = (M, K). And M >=N, make sure that index of
                        t_raw_data is a subset of the index of t_sector_df before call this
                        function.
                        Element[m, k] = 1 if Instruments[m] is in Sector[k] else 0.
    :param t_weight: A pd.Series with length = N1 >= N, make sure that index of t_raw_data
                     is a subset of the index of t_weight. Each element means relative weight
                     of corresponding instrument when regression.
    :return:
    """
    n = len(t_raw_data)
    idx = t_raw_data.index
    if t_weight is None:
        _w: np.ndarray = np.ones(n) / n
    else:
        _w: np.ndarray = t_weight[idx].values

    _w = np.diag(_w)  # It is allowed that sum of _w may not equal 1
    _x: np.ndarray = t_sector_df.loc[idx].values
    _y: np.ndarray = t_raw_data.values

    xw = _x.T.dot(_w)
    xwx_inv = np.linalg.inv(xw.dot(_x))
    xwy = xw.dot(_y)
    b = xwx_inv.dot(xwy)  # b = [XWX]^{-1}[XWY]
    _r = _y - _x.dot(b)  # r = Y - bX
    return pd.Series(data=_r, index=idx)


# -----------------------------------------
# --- Part III: factor exposure process ---


def cal_risk_factor_return_colinear(t_r: np.ndarray, t_x: np.ndarray, t_instru_wgt: np.ndarray, t_sector_wgt: np.ndarray):
    """

    :param t_r: n x 1, n: number of instruments
    :param t_x: n x K, K = 1 + k, k = p + q; p = number of sectors; q = number of style factors; 1 = market; K: number of all risk factors
    :param t_instru_wgt: n x 1, weight (market value) for each instrument
    :param t_sector_wgt: p x 1, weight (market value) of each sector
    :return:
    """
    _n, _K = t_x.shape
    _p = len(t_sector_wgt)
    _q = _K - 1 - _p
    _R11_up_ = np.diag(np.ones(_p))  # p x p
    _R11_dn_ = np.concatenate(([0], -t_sector_wgt[:-1] / t_sector_wgt[-1]))  # 1 x p, linear constrain: \sum_{i=1}^kw_iR_i = 0, R_i: sector return, output of this function
    _R11 = np.vstack((_R11_up_, _R11_dn_))  # (p + 1) x p
    _R12 = np.zeros(shape=(_p + 1, _q))
    _R21 = np.zeros(shape=(_q, _p))
    _R22 = np.diag(np.ones(_q))
    _R = np.vstack((np.hstack((_R11, _R12)), np.hstack((_R21, _R22))))  # (p + q + 1) x (p + q) = K x (K - 1)
    _v_raw = np.sqrt(t_instru_wgt)
    _v = np.diag(_v_raw / np.sum(_v_raw))  # n x n

    #
    # Omega = R((XR)'VXR)^{-1} (XR)'V # size = K x n
    # f = Omega * r
    # Omega * X = E_{kk} # size = K x K
    # Omega *XR = R

    _XR = t_x.dot(_R)  # n x (K-1)
    _P = _XR.T.dot(_v).dot(_XR)  # (K-1) x (K-1)
    _Omega = _R.dot(np.linalg.inv(_P).dot(_XR.T.dot(_v)))  # K x n
    _f = _Omega.dot(t_r)  # K x 1
    return _f, _Omega


def check_for_factor_return_colinear(t_r: np.ndarray, t_x: np.ndarray, t_instru_wgt: np.ndarray, t_factor_ret: np.ndarray):
    """

    :param t_r: same as the t_r in cal_risk_factor_return_colinear
    :param t_x: same as the t_x in cal_risk_factor_return_colinear
    :param t_instru_wgt: same as the t_instru_wgt in cal_risk_factor_return_colinear
    :param t_factor_ret: _f in cal_risk_factor_return_colinear
    :return:
    """
    _rh = t_x @ t_factor_ret
    _residual = t_r - _rh
    _w = np.sqrt(t_instru_wgt)
    _r_wgt_mean = t_r.dot(_w)
    _sst = np.sum((t_r - _r_wgt_mean) ** 2 * _w)
    _ssr = np.sum((_rh - _r_wgt_mean) ** 2 * _w)
    _sse = np.sum(_residual ** 2 * _w)
    _rsq = _ssr / _sst
    _err = np.abs(_sst - _ssr - _sse)
    return _residual, _sst, _ssr, _sse, _rsq, _err


# -----------------------------------------
# --- Part IV: Regression ---
def fun_for_factors_return(t_pid_list: list, t_test_window_list: list, t_factors_return_lag_list: list,
                           t_run_mode: str, t_bgn_date: str, t_stp_date: str):
    for pid, test_window, factors_return_lag in product(t_pid_list, t_test_window_list, t_factors_return_lag_list):
        subprocess.run(["python", "07_factors_return.py",
                        "--pid", pid, "--testWin", str(test_window), "--lag", str(factors_return_lag),
                        "--mode", t_run_mode, "--bgn", t_bgn_date, "--stp", t_stp_date])
    return 0


def fun_for_factors_return_agg(t_pid_list: list, t_test_window_list: list, t_factors_return_lag_list: list):
    for pid, test_window, factors_return_lag in product(t_pid_list, t_test_window_list, t_factors_return_lag_list):
        subprocess.run(["python", "07_factors_return_agg.py", pid, str(test_window), str(factors_return_lag)])
    return 0


def fun_for_derivative_factors_IV(t_pid_list: list, t_test_window_list: list, t_factors_return_lag_list: list):
    for pid, test_window, factors_return_lag in product(t_pid_list, t_test_window_list, t_factors_return_lag_list):
        subprocess.run(["python", "08_cal_derivative_factors.IV.py", pid, str(test_window), str(factors_return_lag)])
    return 0


if __name__ == "__main__":
    # ---- TEST EXAMPLE 0
    print("---- TEST EXAMPLE 0")
    sector_classification = {
        "CU.SHF": "METAL",
        "AL.SHF": "METAL",
        "ZN.SHF": "METAL",
        "A.DCE": "OIL",
        "M.DCE": "OIL",
        "Y.DCE": "OIL",
        "P.DCE": "OIL",
        "MA.CZC": "CHEM",
        "TA.CZC": "CHEM",
        "PP.DCE": "CHEM",
    }

    sector_df = pd.DataFrame.from_dict({z: {sector_classification[z]: 1} for z in sector_classification}, orient="index").fillna(0)
    print(sector_df)

    raw_factor = pd.Series({
        "CU.SHF": 10,
        "ZN.SHF": 8,
        "Y.DCE": 3,
        "P.DCE": 0,
        "MA.CZC": -2,
        "TA.CZC": -4,
    })

    weight = pd.Series({
        "Y.DCE": 2,
        "P.DCE": 1,
        "MA.CZC": 1,
        "TA.CZC": 1,
        "CU.SHF": 1,
        "ZN.SHF": 2,
    })

    new_factor = neutralize_by_sector(
        t_raw_data=raw_factor,
        t_sector_df=sector_df,
        t_weight=weight,
    )

    df = pd.DataFrame({
        "OLD": raw_factor,
        "WGT": weight,
        "NEW": new_factor,
    }).loc[raw_factor.index]

    print(df)

    # ---- TEST EXAMPLE 1
    print("---- TEST EXAMPLE 1")
    df = pd.DataFrame({
        "sector": ["I1", "I1", "I2", "I2"],
        "I1": [1, 1, 0, 0],
        "I2": [0, 0, 1, 1],
        "raw_factor": [100, 80, 32, 8],
        "raw_return": [24, 6, 45, 15],
        "ave_factor_by_sec": [90, 90, 20, 20],
        "ave_return_by_sec": [15, 15, 30, 30],
    }, index=["S1", "S2", "S3", "S4"])
    df.index.name = "资产"
    df["neu_factor"] = neutralize_by_sector(t_raw_data=df["raw_factor"], t_sector_df=df[["I1", "I2"]], t_weight=None)
    df["neu_return"] = neutralize_by_sector(t_raw_data=df["raw_return"], t_sector_df=df[["I1", "I2"]], t_weight=None)

    # wgt_srs = pd.Series({"S1": 1, "S2": 1, "S3": 2, "S4": 3})
    # df["neu_factor"] = neutralize_by_sector(t_raw_data=df["raw_factor"], t_sector_df=df[["I1", "I2"]], t_weight=wgt_srs)
    # df["neu_return"] = neutralize_by_sector(t_raw_data=df["raw_return"], t_sector_df=df[["I1", "I2"]], t_weight=wgt_srs)

    pd.set_option("display.width", 0)
    print(df)

    for x, y in product(["raw_factor", "neu_factor", "I1", "I2"], ["raw_return", "neu_return"]):
        r = df[[x, y]].corr().loc[x, y]
        # print("Corr({:4s},{:4s}) = {:>9.4f}".format(x, y, r))
        print("{} & {} & {:>.3f}\\\\".format(x, y, r))
