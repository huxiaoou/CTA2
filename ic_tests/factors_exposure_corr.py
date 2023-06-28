import os
import pandas as pd
import itertools as ittl
from skyrim.whiterun import CCalendar
from skyrim.winterhold import plot_lines
from skyrim.falkreath import CManagerLibReader, CLib1Tab1
from typing import Dict


def factors_exposure_corr(neutral_method: str,
                          test_factor_list_l: list,
                          test_factor_list_r: list,
                          factors_exposure_dir: str,
                          factors_exposure_neutral_dir,
                          trade_calendar: CCalendar,
                          factors_bgn_date: str,
                          factors_stp_date: str,
                          database_structure: Dict[str, CLib1Tab1],
                          factors_exposure_corr_dir: str,
                          ):
    # --- get test factor list
    test_factor_list = test_factor_list_l + test_factor_list_r
    if test_factor_list_r:
        factor_comb_list = list(ittl.product(test_factor_list_l, test_factor_list_r))
    else:
        factor_comb_list = list(ittl.combinations(test_factor_list_l, 2))

    # --- set save id
    if neutral_method == "":
        save_id = "-".join(test_factor_list)
        src_dir = factors_exposure_dir
    else:
        save_id = "-".join(test_factor_list) + "." + neutral_method
        src_dir = factors_exposure_neutral_dir

    # --- initialize factor libs
    factor_libs_manager: Dict[str, dict] = {}
    for factor_lbl in test_factor_list:
        lib_id = factor_lbl if neutral_method == "" else factor_lbl + "." + neutral_method
        factor_libs_manager[factor_lbl] = {
            "structure": database_structure[lib_id],
            "reader": CManagerLibReader(
                t_db_name=database_structure[lib_id].m_lib_name,
                t_db_save_dir=src_dir
            )
        }
        factor_libs_manager[factor_lbl]["reader"].set_default(database_structure[lib_id].m_tab.m_table_name)

    # --- core loop
    factor_corr_by_date_data = {}
    for trade_date in trade_calendar.get_iter_list(t_bgn_date=factors_bgn_date, t_stp_date=factors_stp_date, t_ascending=True):
        test_factor_data = {}
        for factor_lbl in test_factor_list:
            factor_df = factor_libs_manager[factor_lbl]["reader"].read_by_date(
                t_trade_date=trade_date,
                t_value_columns=["instrument", "value"]
            ).set_index("instrument")
            test_factor_data[factor_lbl] = factor_df["value"]
        test_factor_df = pd.DataFrame(test_factor_data)
        if len(test_factor_df) > 0:
            test_corr = test_factor_df.corr()
            factor_corr_by_date_data[trade_date] = {
                "{}-{}".format(z[0], z[1]): test_corr.at[z[0], z[1]] if z[0] in test_corr.index and z[1] in test_corr.columns else 0
                for z in factor_comb_list}
    factor_corr_by_date_df = pd.DataFrame.from_dict(factor_corr_by_date_data, orient="index")
    factor_corr_by_date_df_cumsum = factor_corr_by_date_df.cumsum()
    for factor_lib in factor_libs_manager.values():
        factor_lib["reader"].close()

    # --- plot
    plot_lines(
        factor_corr_by_date_df_cumsum,
        t_fig_name="factors.corr.{}.cumsum".format(save_id), t_save_dir=factors_exposure_corr_dir,
        t_colormap="jet"
    )

    # --- save
    factor_corr_by_date_df.to_csv(
        os.path.join(factors_exposure_corr_dir, "factors.corr.{}.csv.gz".format(save_id)),
        index_label="trade_date",
        float_format="%.4f"
    )
    factor_corr_by_date_df_cumsum.to_csv(
        os.path.join(factors_exposure_corr_dir, "factors.corr.{}.cumsum.csv.gz".format(save_id)),
        index_label="trade_date",
        float_format="%.4f"
    )

    print("-" * 120)

    print("... cumulative IC of each factor-pair:")
    print(factor_corr_by_date_df_cumsum.iloc[-1, :].sort_values(ascending=False))

    print("-" * 120)

    print("... average daily IC of each factor-pair")
    print(factor_corr_by_date_df.mean().sort_values(ascending=False))

    return 0
