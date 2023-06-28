import multiprocessing as mp
import datetime as dt
from setup_factor_and_portfolio import sys, ittl, calendar_path
from setup_factor_and_portfolio import available_universe_dir, factors_exposure_dir, factors_exposure_neutral_dir, factors_exposure_delinear_dir
from setup_factor_and_portfolio import test_return_dir, test_return_neutral_dir
from setup_factor_and_portfolio import test_ic_dir, factors_delinear_test_ic_dir, factors_exposure_corr_dir
from config_factor import factors_list, test_window_list, factors_return_lag_list
from config_factor import factors_bgn_date, test_lag, neutral_method
from config_factor import factors_pool_bgn_date, factors_pool_options
from struct_lib import database_structure
from custom.XFuns import fun_for_factors_return_agg
from ic_tests.ic_test_single_factor import ic_test_single_factor
from ic_tests.ic_test_single_factor_neutral import ic_test_single_factor_neutral
from ic_tests.ic_test_plot_single_factor import ic_test_plot_single_factor
from ic_tests.ic_test_plot_single_factor_neutral import ic_test_plot_single_factor_neutral
from ic_tests.ic_test_delinear_factors import ic_test_delinear_factors
from ic_tests.factors_exposure_corr import factors_exposure_corr
from ic_tests.ic_test_summary import ic_test_summary
from skyrim.whiterun import CCalendar


def process_target_fun_for_test_ic(t_group_id: int,
                                   t_gn: int, t_factors_list: list, t_test_window_list: list,
                                   t_factors_bgn_date: str, t_factors_stp_date: str, t_test_lag: int,
                                   t_test_ic_dir: str, t_available_universe_dir: str,
                                   t_factors_exposure_dir: str, t_test_return_dir: str,
                                   t_database_structure: dict,
                                   t_calendar_path: str,
                                   t_skip_if_exists: bool = True
                                   ):
    _trade_calendar = CCalendar(t_path=t_calendar_path)
    iter_list = ittl.product(t_factors_list, t_test_window_list)
    for it, (_factor_lbl, _test_window) in enumerate(iter_list):
        if it % t_gn == t_group_id:
            ic_test_single_factor(
                factor_lbl=_factor_lbl, test_window=_test_window,
                trade_calendar=_trade_calendar, factors_bgn_date=t_factors_bgn_date, factors_stp_date=t_factors_stp_date,
                test_lag=t_test_lag,
                test_ic_dir=t_test_ic_dir, available_universe_dir=t_available_universe_dir,
                factors_exposure_dir=t_factors_exposure_dir, test_return_dir=t_test_return_dir,
                database_structure=t_database_structure, skip_if_exists=t_skip_if_exists)
    return 0


def process_target_fun_for_test_ic_neutral(t_group_id: int,
                                           t_gn: int, t_factors_list: list, t_test_window_list: list, t_neutral_method: str,
                                           t_factors_bgn_date: str, t_factors_stp_date: str, t_test_lag: int,
                                           t_test_ic_dir: str, t_available_universe_dir: str,
                                           t_factors_exposure_neutral_dir: str, t_test_return_neutral_dir: str,
                                           t_database_structure: dict,
                                           t_calendar_path: str,
                                           t_skip_if_exists: bool = True
                                           ):
    _trade_calendar = CCalendar(t_path=t_calendar_path)
    iter_list = ittl.product(t_factors_list, t_test_window_list)
    for it, (_factor_lbl, _test_window) in enumerate(iter_list):
        if it % t_gn == t_group_id:
            ic_test_single_factor_neutral(
                factor_lbl=_factor_lbl, test_window=_test_window, neutral_method=t_neutral_method,
                trade_calendar=_trade_calendar, factors_bgn_date=t_factors_bgn_date, factors_stp_date=t_factors_stp_date,
                test_lag=t_test_lag,
                test_ic_dir=t_test_ic_dir, available_universe_dir=t_available_universe_dir,
                factors_exposure_neutral_dir=t_factors_exposure_neutral_dir, test_return_neutral_dir=t_test_return_neutral_dir,
                database_structure=t_database_structure, skip_if_exists=t_skip_if_exists)
    return 0


def ic_tests(t_gn: int, t_factors_list: list, t_test_window_list: list,
             t_factors_bgn_date: str, t_factors_stp_date: str, t_test_lag: int,
             t_test_ic_dir: str, t_available_universe_dir: str,
             t_factors_exposure_dir: str, t_test_return_dir: str,
             t_database_structure: dict,
             t_calendar_path: str,
             t_skip_if_exists: bool = True,
             ):
    to_join_list = []
    for group_id in range(t_gn):
        t = mp.Process(target=process_target_fun_for_test_ic, args=(
            group_id,
            t_gn, t_factors_list, t_test_window_list,
            t_factors_bgn_date, t_factors_stp_date, t_test_lag,
            t_test_ic_dir, t_available_universe_dir,
            t_factors_exposure_dir, t_test_return_dir,
            t_database_structure,
            t_calendar_path,
            t_skip_if_exists
        ))
        t.start()
        to_join_list.append(t)
    for t in to_join_list:
        t.join()
    return 0


def ic_tests_neutral(t_gn: int, t_factors_list: list, t_test_window_list: list, t_neutral_method: str,
                     t_factors_bgn_date: str, t_factors_stp_date: str, t_test_lag: int,
                     t_test_ic_dir: str, t_available_universe_dir: str,
                     t_factors_exposure_neutral_dir: str, t_test_return_neutral_dir: str,
                     t_database_structure: dict,
                     t_calendar_path: str,
                     t_skip_if_exists: bool = True,
                     ):
    to_join_list = []
    for group_id in range(t_gn):
        t = mp.Process(target=process_target_fun_for_test_ic_neutral, args=(
            group_id,
            t_gn, t_factors_list, t_test_window_list, t_neutral_method,
            t_factors_bgn_date, t_factors_stp_date, t_test_lag,
            t_test_ic_dir, t_available_universe_dir,
            t_factors_exposure_neutral_dir, t_test_return_neutral_dir,
            t_database_structure,
            t_calendar_path,
            t_skip_if_exists
        ))
        t.start()
        to_join_list.append(t)
    for t in to_join_list:
        t.join()

    return 0


if __name__ == "__main__":
    print("... All tests begin @ {}".format(t0 := dt.datetime.now()))

    md_stp_date, GN = sys.argv[1], int(sys.argv[2])
    sep = "-" * 120 + "\n"
    factors_stp_date = md_stp_date
    factors_pool_stp_date = md_stp_date
    trade_calendar = CCalendar(t_path=calendar_path)

    ic_tests(
        t_gn=GN, t_factors_list=factors_list, t_test_window_list=test_window_list,
        t_factors_bgn_date=factors_bgn_date, t_factors_stp_date=factors_stp_date, t_test_lag=test_lag,
        t_test_ic_dir=test_ic_dir, t_available_universe_dir=available_universe_dir,
        t_factors_exposure_dir=factors_exposure_dir, t_test_return_dir=test_return_dir,
        t_database_structure=database_structure,
        t_calendar_path=calendar_path,
        t_skip_if_exists=False
    )
    print(sep)

    ic_tests_neutral(
        t_gn=GN, t_factors_list=factors_list, t_test_window_list=test_window_list, t_neutral_method=neutral_method,
        t_factors_bgn_date=factors_bgn_date, t_factors_stp_date=factors_stp_date, t_test_lag=test_lag,
        t_test_ic_dir=test_ic_dir, t_available_universe_dir=available_universe_dir,
        t_factors_exposure_neutral_dir=factors_exposure_neutral_dir, t_test_return_neutral_dir=test_return_neutral_dir,
        t_database_structure=database_structure,
        t_calendar_path=calendar_path,
        t_skip_if_exists=False
    )
    print(sep)

    for factor_lbl in factors_list:
        ic_test_plot_single_factor(
            factor_lbl=factor_lbl, test_window_list=test_window_list,
            test_ic_dir=test_ic_dir
        )
    print(sep)

    for factor_lbl in factors_list:
        ic_test_plot_single_factor_neutral(
            factor_lbl=factor_lbl, neutral_method=neutral_method, test_window_list=test_window_list,
            test_ic_dir=test_ic_dir
        )
    print(sep)

    ic_test_summary(factors_list=factors_list, exception_list=[],
                    neutral_method=neutral_method, test_ic_dir=test_ic_dir)
    print(sep)

    for test_window, factors_return_lag in ittl.product(test_window_list, factors_return_lag_list):
        ic_test_delinear_factors(
            pid="P3", neutral_method=neutral_method, test_window=test_window, factors_return_lag=factors_return_lag,
            trade_calendar=trade_calendar,
            factors_pool_bgn_date=factors_pool_bgn_date, factors_pool_stp_date=factors_pool_stp_date,
            test_lag=test_lag, factors_pool_options=factors_pool_options,
            factors_delinear_test_ic_dir=factors_delinear_test_ic_dir,
            factors_exposure_delinear_dir=factors_exposure_delinear_dir,
            test_return_neutral_dir=test_return_neutral_dir,
            database_structure=database_structure
        )
    print(sep)

    test_factor_list_l, test_factor_list_r = ["MTM231", "TS126"], []
    factors_exposure_corr(
        neutral_method=neutral_method, test_factor_list_l=test_factor_list_l, test_factor_list_r=test_factor_list_r,
        factors_exposure_dir=factors_exposure_dir,
        factors_exposure_neutral_dir=factors_exposure_neutral_dir,
        trade_calendar=trade_calendar,
        factors_bgn_date=factors_bgn_date,
        factors_stp_date=factors_stp_date,
        database_structure=database_structure,
        factors_exposure_corr_dir=factors_exposure_corr_dir
    )
    print(sep)

    fun_for_factors_return_agg(
        t_pid_list=list(factors_pool_options.keys()),
        t_test_window_list=test_window_list,
        t_factors_return_lag_list=factors_return_lag_list,
    )
    print(sep)

    print("... All tests done @ {}".format(t1 := dt.datetime.now()))
    print("... total time consuming: {:>9.2f} seconds\n".format((t1 - t0).total_seconds()))
