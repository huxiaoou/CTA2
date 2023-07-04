import sys
import datetime as dt
import itertools as ittl
from setup_factor_and_portfolio import calendar_path, instrument_info_path
from setup_factor_and_portfolio import md_by_instru_dir, major_minor_dir, available_universe_dir
from setup_factor_and_portfolio import signals_opt_dir
from setup_factor_and_portfolio import simulations_opt_dir
from setup_factor_and_portfolio import evaluations_opt_dir
from setup_factor_and_portfolio import by_year_dir
from config_factor import universe_id, instruments_universe_options
from config_portfolio import test_windows
from config_portfolio import available_factors, selected_sectors, selected_factors
from config_portfolio import allocation_options, synth_options
from config_portfolio import fast_n_slow_n_comb, timing_factors
from config_portfolio import risk_free_rate, cost_rate, cost_reservation, init_premium
from struct_lib_portfolio import database_structure
from simulations.XFuns import fun_for_simulation_factors
from simulations.evaluation import evaluation_single_factor
from simulations.evaluation_by_year import evaluation_single_factor_by_year
from simulations.evaluation_multiple_by_year import evaluation_multiple_by_year_plot_nav

if __name__ == "__main__":
    print("... All simulations begin @ {}".format(t0 := dt.datetime.now()))

    test_bgn_date, test_stp_date, GN = "20140902", sys.argv[1], int(sys.argv[2])
    switch = {
        "vanilla": sys.argv[3][0].upper() in ["T", "TRUE"],
        "ma": sys.argv[3][1].upper() in ["T", "TRUE"],
        "allocation": sys.argv[3][2].upper() in ["T", "TRUE"],
        "by_year": sys.argv[3][3].upper() in ["T", "TRUE"],
    }

    test_universe = instruments_universe_options[universe_id]

    # set factors
    vanilla_factors = ["{}VM{:03d}".format(factor_lbl, mov_ave_len)
                       for factor_lbl, mov_ave_len in ittl.product(available_factors, test_windows)]
    ma_factors = ["{}F{:03d}S{:03d}M{:03d}".format(factor_lbl, fn, sn, mov_ave_len)
                  for factor_lbl, mov_ave_len, (fn, sn) in
                  ittl.product(timing_factors, test_windows, fast_n_slow_n_comb)]
    alloc_id_opt_list = ["{}M{:03d}".format(aid, tw) for aid, tw in ittl.product(
        list(synth_options) + list(allocation_options), test_windows)]

    if switch["vanilla"]:
        fun_for_simulation_factors(
            t_gn=GN, t_factors_list=vanilla_factors, t_test_window_list=[1],
            calendar_path=calendar_path, instrument_info_path=instrument_info_path,
            md_by_instru_dir=md_by_instru_dir, major_minor_dir=major_minor_dir,
            available_universe_dir=available_universe_dir,
            sig_dir=signals_opt_dir, dst_dir=simulations_opt_dir,
            database_structure=database_structure,
            test_universe=test_universe, test_bgn_date=test_bgn_date, test_stp_date=test_stp_date,
            cost_reservation=cost_reservation, cost_rate=cost_rate, init_premium=init_premium,
            skip_if_exist=False
        )

        for factor_lbl in vanilla_factors:
            evaluation_single_factor(
                factor_lbl, [1], test_bgn_date, test_stp_date,
                risk_free_rate, simulations_opt_dir, evaluations_opt_dir, top_n=5
            )

    if switch["ma"]:
        fun_for_simulation_factors(
            t_gn=GN, t_factors_list=ma_factors, t_test_window_list=[1],
            calendar_path=calendar_path, instrument_info_path=instrument_info_path,
            md_by_instru_dir=md_by_instru_dir, major_minor_dir=major_minor_dir,
            available_universe_dir=available_universe_dir,
            sig_dir=signals_opt_dir, dst_dir=simulations_opt_dir,
            database_structure=database_structure,
            test_universe=test_universe, test_bgn_date=test_bgn_date, test_stp_date=test_stp_date,
            cost_reservation=cost_reservation, cost_rate=cost_rate, init_premium=init_premium,
            skip_if_exist=False
        )

        for factor_lbl in ma_factors:
            evaluation_single_factor(
                factor_lbl, [1], test_bgn_date, test_stp_date,
                risk_free_rate, simulations_opt_dir, evaluations_opt_dir, top_n=5
            )

    if switch["allocation"]:
        fun_for_simulation_factors(
            t_gn=GN, t_factors_list=alloc_id_opt_list, t_test_window_list=[1],
            calendar_path=calendar_path, instrument_info_path=instrument_info_path,
            md_by_instru_dir=md_by_instru_dir, major_minor_dir=major_minor_dir,
            available_universe_dir=available_universe_dir,
            sig_dir=signals_opt_dir, dst_dir=simulations_opt_dir,
            database_structure=database_structure,
            test_universe=test_universe, test_bgn_date=test_bgn_date, test_stp_date=test_stp_date,
            cost_reservation=cost_reservation, cost_rate=cost_rate, init_premium=init_premium,
            skip_if_exist=False
        )

        for allocation_id in alloc_id_opt_list:
            evaluation_single_factor(
                allocation_id, [1], test_bgn_date, test_stp_date,
                risk_free_rate, simulations_opt_dir, evaluations_opt_dir, top_n=5
            )

    if switch["by_year"]:
        evaluation_single_factor_by_year("R1M010", 1, risk_free_rate, evaluations_opt_dir, by_year_dir)
        evaluation_single_factor_by_year("R4M010", 1, risk_free_rate, evaluations_opt_dir, by_year_dir)
        evaluation_single_factor_by_year("A1M020", 1, risk_free_rate, evaluations_opt_dir, by_year_dir)
        evaluation_single_factor_by_year("A6M005", 1, risk_free_rate, evaluations_opt_dir, by_year_dir)
        evaluation_single_factor_by_year("A3M020", 1, risk_free_rate, evaluations_opt_dir, by_year_dir)
        evaluation_single_factor_by_year("A8M005", 1, risk_free_rate, evaluations_opt_dir, by_year_dir)
        evaluation_multiple_by_year_plot_nav(
            "comb",
            [
                ("R1M010", 1),
                ("R4M010", 1),
                ("A1M020", 1),
                ("A6M005", 1),
                ("A3M020", 1),
                ("A8M005", 1),
            ],
            evaluations_opt_dir, by_year_dir
        )

        evaluation_multiple_by_year_plot_nav(
            "comb_sector_VM005",
            [(z + "VM005", 1) for z in ["MARKET"] + selected_sectors],
            evaluations_opt_dir, by_year_dir
        )
        evaluation_multiple_by_year_plot_nav(
            "comb_sector_VM020",
            [(z + "VM020", 1) for z in ["MARKET"] + selected_sectors],
            evaluations_opt_dir, by_year_dir
        )

        evaluation_multiple_by_year_plot_nav(
            "comb_style_VM005",
            [(z + "VM005", 1) for z in selected_factors],
            evaluations_opt_dir, by_year_dir
        )
        evaluation_multiple_by_year_plot_nav(
            "comb_style_VM020",
            [(z + "VM020", 1) for z in selected_factors],
            evaluations_opt_dir, by_year_dir
        )

    print("... All simulations done @ {}".format(t1 := dt.datetime.now()))
    print("... total time consuming: {:>9.2f} seconds\n".format((t1 - t0).total_seconds()))
