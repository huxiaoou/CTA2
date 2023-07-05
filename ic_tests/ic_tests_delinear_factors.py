import os
import datetime as dt
import numpy as np
import pandas as pd
from skyrim.falkreath import CManagerLibReader, CManagerLibWriterByDate, CLib1Tab1
from skyrim.whiterun import CCalendar
from skyrim.winterhold import plot_lines
from typing import Dict


def ic_test_delinear_factors(pid: str, neutral_method: str, test_window: int, factors_return_lag: int,
                             trade_calendar: CCalendar, factors_pool_bgn_date: str, factors_pool_stp_date: str,
                             test_lag: int,
                             factors_pool_options: dict,
                             factors_delinear_test_ic_dir: str,
                             factors_exposure_delinear_dir: str,
                             test_return_neutral_dir: str,
                             database_structure: Dict[str, CLib1Tab1],
                             days_per_year: int = 252) -> int:
    # --- initialize output lib: factors_return/instruments_residual/factors_portfolio
    factors_delinear_test_ic_lib_id = "factors_delinear_test_ic.{}.{}.TW{:03d}.T{}".format(pid, neutral_method, test_window, factors_return_lag)
    factors_delinear_test_ic_lib = CManagerLibWriterByDate(t_db_save_dir=factors_delinear_test_ic_dir, t_db_name=database_structure[factors_delinear_test_ic_lib_id].m_lib_name)
    factors_delinear_test_ic_lib.initialize_table(t_table=database_structure[factors_delinear_test_ic_lib_id].m_tab)

    # --- load delinearized factors
    delinear_lib_id = "{}.{}.DELINEAR".format(pid, neutral_method)
    delinear_lib = CManagerLibReader(t_db_save_dir=factors_exposure_delinear_dir, t_db_name=database_structure[delinear_lib_id].m_lib_name)
    delinear_lib.set_default(database_structure[delinear_lib_id].m_tab.m_table_name)

    # --- load test return
    test_return_lib_id = "test_return_{:03d}.{}".format(test_window, neutral_method)
    test_return_lib_structure = database_structure[test_return_lib_id]
    test_return_lib = CManagerLibReader(t_db_name=test_return_lib_structure.m_lib_name, t_db_save_dir=test_return_neutral_dir)
    test_return_lib.set_default(test_return_lib_structure.m_tab.m_table_name)

    # --- load selected factors
    selected_factors_pool = factors_pool_options[pid]

    # --- core loop
    for trade_date in trade_calendar.get_iter_list(t_bgn_date=factors_pool_bgn_date, t_stp_date=factors_pool_stp_date, t_ascending=True):
        # load test return
        test_return_date = trade_calendar.get_next_date(t_this_date=trade_date, t_shift=(test_lag + test_window) * factors_return_lag)
        test_return_df = test_return_lib.read_by_date(
            t_table_name=database_structure[test_return_lib_id].m_tab.m_table_name,
            t_trade_date=test_return_date,
            t_value_columns=["instrument", "value"]
        ).set_index("instrument")
        if len(test_return_df) == 0:
            continue

        # load delinear factors
        delinearized_df = delinear_lib.read_by_date(
            t_table_name=database_structure[delinear_lib_id].m_tab.m_table_name,
            t_trade_date=trade_date,
            t_value_columns=["instrument"] + selected_factors_pool
        ).set_index("instrument")
        if len(delinearized_df) == 0:
            continue

        # corr between exposure and
        exposure_and_return_df: pd.DataFrame = pd.merge(
            left=test_return_df, right=delinearized_df,
            left_index=True, right_index=True,
            how="right"
        )
        test_ic_srs = exposure_and_return_df[selected_factors_pool].corrwith(
            exposure_and_return_df["value"], axis=0, method="spearman")

        # save factor return
        factors_delinear_test_ic_df = pd.DataFrame(data={"ic": test_ic_srs})
        factors_delinear_test_ic_lib.update_by_date(
            t_table_name=database_structure[factors_delinear_test_ic_lib_id].m_tab.m_table_name,
            t_date=trade_date,
            t_update_df=factors_delinear_test_ic_df,
            t_using_index=True,
        )

    # close all libs
    delinear_lib.close()
    test_return_lib.close()

    # extract IC
    all_ic_df = factors_delinear_test_ic_lib.read(
        t_table_name=database_structure[factors_delinear_test_ic_lib_id].m_tab.m_table_name,
        t_value_columns=["trade_date", "factor", "value"]
    )
    factors_delinear_test_ic_lib.close()

    # plot cumulative IC
    pivot_ic_df = pd.pivot_table(data=all_ic_df, index="trade_date", columns="factor", values="value", aggfunc=sum)
    pivot_ic_cumsum_df = pivot_ic_df[selected_factors_pool].cumsum()
    plot_lines(
        t_plot_df=pivot_ic_cumsum_df,
        t_save_dir=factors_delinear_test_ic_dir,
        t_fig_name=factors_delinear_test_ic_lib_id,
        t_colormap="jet"
    )

    # get IC statistics
    mu = pivot_ic_df.mean()
    sd = pivot_ic_df.std()
    icir = mu / sd * np.sqrt(days_per_year / test_window)
    delinear_factor_ic_test_summary_df = pd.DataFrame.from_dict({
        "IC-Mean": mu,
        "IC-Std": sd,
        "ICIR": icir,
    }, orient="index").sort_index(axis=1)

    print(delinear_factor_ic_test_summary_df)
    delinear_factor_ic_test_summary_file = factors_delinear_test_ic_lib_id + ".summary.csv"
    delinear_factor_ic_test_summary_path = os.path.join(factors_delinear_test_ic_dir, delinear_factor_ic_test_summary_file)
    delinear_factor_ic_test_summary_df.to_csv(delinear_factor_ic_test_summary_path, index_label="factor", float_format="%.3f")

    print("... factor return for pid = {1}, neutral_method = {2}, test_window = {3:>2d}, factor_return_lag = {4} are calculated @ {0}".format(
        dt.datetime.now(), pid, neutral_method, test_window, factors_return_lag))

    return 0
