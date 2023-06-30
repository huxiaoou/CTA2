import argparse
from returns.instrument_return import merge_instru_return
from returns.available_universe import cal_available_universe
from returns.market_return import cal_market_return
from returns.test_return import cal_test_return_mp
from returns.test_return_neutral import cal_test_return_neutral_mp
from factors.factors_algorithm_BASIS import cal_factors_exposure_basis_mp
from factors.factors_algorithm_BETA import cal_factors_exposure_beta_mp
from factors.factors_algorithm_CSP import cal_factors_exposure_csp_mp
from factors.factors_algorithm_CSR import cal_factors_exposure_csr_mp
from factors.factors_algorithm_CTP import cal_factors_exposure_ctp_mp
from factors.factors_algorithm_CTR import cal_factors_exposure_ctr_mp
from factors.factors_algorithm_CV import cal_factors_exposure_cv_mp
from factors.factors_algorithm_CVP import cal_factors_exposure_cvp_mp
from factors.factors_algorithm_CVR import cal_factors_exposure_cvr_mp
from factors.factors_algorithm_HP import cal_factors_exposure_hp_mp
from factors.factors_algorithm_MTM import cal_factors_exposure_mtm_mp
from factors.factors_algorithm_RSW import cal_factors_exposure_rsw_mp
from factors.factors_algorithm_SGM import cal_factors_exposure_sgm_mp
from factors.factors_algorithm_SIZE import cal_factors_exposure_size_mp
from factors.factors_algorithm_SKEW import cal_factors_exposure_skew_mp
from factors.factors_algorithm_TO import cal_factors_exposure_to_mp
from factors.factors_algorithm_TS import cal_factors_exposure_ts_mp
from factors.factors_algorithm_VOL import cal_factors_exposure_vol_mp
from factors.factors_neutral import cal_factors_neutral_mp

from setup_factor_and_portfolio import major_return_dir, major_minor_dir, md_by_instru_dir, fundamental_by_instru_dir, \
    instruments_return_dir, available_universe_dir, \
    test_return_dir, test_return_neutral_dir, \
    factors_exposure_dir, factors_exposure_neutral_dir, \
    factors_return_dir, \
    calendar_path
from config_factor import concerned_instruments_universe, sector_classification, \
    available_universe_options, test_windows, factors_args, factors, neutral_method
from struct_lib import database_structure

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(description="Entry point of this project")
    args_parser.add_argument("-w", "--switch", type=str, help="""
        use this to decide which parts to run, available options = {'ir', 'au', 'mr', 'tr', 'trn'}
        """)
    args_parser.add_argument("-m", "--mode", type=str, choices=("o", "a"), help="""
        run mode, available options = {'o', 'overwrite', 'a', 'append'}
        """)
    args_parser.add_argument("-b", "--bgn", type=str, help="""
        begin date, may be different according to different switches, suggestion of different switch:
        {   
            "returns/instrument_return": "20120101",
            
            "returns/available_universe": "20120301",
            "returns/market_return": None,
            "returns/test_return": "20120301",
            "returns/test_return_neutral": "20120301",
            
            "factors/exposure": "20130101",
            "factors/exposure_neutral": "20130101",
        }
        """)
    args_parser.add_argument("-s", "--stp", type=str, help="""
        stop date, not included, usually it would be the day after the last trade date, such as
        "20230619" if last trade date is "20230616"  
        """)
    args_parser.add_argument("-p", "--process", type=int, default=5, help="""
        number of process to be called when calculating, default = 5
        """)
    args_parser.add_argument("-f", "--factor", type=str, default="", help="""
        optional, must be provided if switch = {'factors_exposure'},
        use this to decide which factor, available options = {
        ''}
        """)

    args = args_parser.parse_args()
    switch = args.switch.upper()
    run_mode = args.mode.upper() if switch in ["AU", "TR", "TRN", "FE", "FEN"] else None
    bgn_date, stp_date = args.bgn, args.stp
    proc_num = args.process
    factor = args.factor.upper()

    if switch in ["IR"]:  # "INSTRUMENT RETURN":
        merge_instru_return(
            bgn_date=bgn_date, stp_date=stp_date,
            major_return_dir=major_return_dir, instruments_return_dir=instruments_return_dir,
            concerned_instruments_universe=concerned_instruments_universe,
        )
    elif switch in ["AU"]:  # "AVAILABLE UNIVERSE"
        cal_available_universe(
            test_windows=test_windows,
            run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
            instruments_universe=concerned_instruments_universe,
            available_universe_options=available_universe_options,
            available_universe_dir=available_universe_dir,
            major_return_dir=major_return_dir,
            calendar_path=calendar_path,
            database_structure=database_structure,
        )
    elif switch in ["MR"]:  # "MARKET RETURN"
        cal_market_return(
            instruments_return_dir=instruments_return_dir,
            available_universe_dir=available_universe_dir,
            database_structure=database_structure,
        )
    elif switch in ["TR"]:  # "TEST RETURN"
        cal_test_return_mp(
            proc_num=proc_num,
            test_windows=test_windows,
            run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
            instruments_return_dir=instruments_return_dir,
            test_return_dir=test_return_dir,
            calendar_path=calendar_path,
            database_structure=database_structure
        )
    elif switch in ["TRN"]:  # "TEST RETURN NEUTRAL"
        cal_test_return_neutral_mp(
            proc_num=proc_num,
            test_windows=test_windows, neutral_method=neutral_method,
            run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
            instruments_universe=concerned_instruments_universe,
            available_universe_dir=available_universe_dir,
            sector_classification=sector_classification,
            test_return_dir=test_return_dir,
            test_return_neutral_dir=test_return_neutral_dir,
            calendar_path=calendar_path,
            database_structure=database_structure,
        )
    elif switch in ["FE"]:
        if factor == "BASIS":
            cal_factors_exposure_basis_mp(proc_num=proc_num, basis_windows=factors_args["BASIS"],
                                          run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                          concerned_instruments_universe=concerned_instruments_universe,
                                          factors_exposure_dir=factors_exposure_dir,
                                          fundamental_dir=fundamental_by_instru_dir,
                                          major_minor_dir=major_minor_dir,
                                          calendar_path=calendar_path,
                                          database_structure=database_structure,
                                          )
        if factor == "BETA":
            cal_factors_exposure_beta_mp(proc_num=proc_num, beta_windows=factors_args["BETA"],
                                         run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                         concerned_instruments_universe=concerned_instruments_universe,
                                         factors_exposure_dir=factors_exposure_dir,
                                         instruments_return_dir=instruments_return_dir,
                                         major_return_dir=major_return_dir,
                                         calendar_path=calendar_path,
                                         database_structure=database_structure,
                                         )
        if factor == "CSP":
            cal_factors_exposure_csp_mp(proc_num=proc_num, csp_windows=factors_args["CSP"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "CSR":
            cal_factors_exposure_csr_mp(proc_num=proc_num, csr_windows=factors_args["CSR"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "CTP":
            cal_factors_exposure_ctp_mp(proc_num=proc_num, ctp_windows=factors_args["CTP"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "CTR":
            cal_factors_exposure_ctr_mp(proc_num=proc_num, ctr_windows=factors_args["CTR"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "CV":
            cal_factors_exposure_cv_mp(proc_num=proc_num, cv_windows=factors_args["CV"],
                                       run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                       concerned_instruments_universe=concerned_instruments_universe,
                                       factors_exposure_dir=factors_exposure_dir,
                                       major_return_dir=major_return_dir,
                                       calendar_path=calendar_path,
                                       database_structure=database_structure,
                                       )
        if factor == "CVP":
            cal_factors_exposure_cvp_mp(proc_num=proc_num, cvp_windows=factors_args["CVP"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "CVR":
            cal_factors_exposure_cvr_mp(proc_num=proc_num, cvr_windows=factors_args["CVR"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "HP":
            cal_factors_exposure_hp_mp(proc_num=proc_num, hp_windows=factors_args["HP"],
                                       run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                       concerned_instruments_universe=concerned_instruments_universe,
                                       factors_exposure_dir=factors_exposure_dir,
                                       major_return_dir=major_return_dir,
                                       calendar_path=calendar_path,
                                       database_structure=database_structure,
                                       )
        if factor == "MTM":
            cal_factors_exposure_mtm_mp(proc_num=proc_num, mtm_windows=factors_args["MTM"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "RSW":
            cal_factors_exposure_rsw_mp(proc_num=proc_num, rsw_windows=[252], half_life_windows=factors_args["RSW252HL"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        fundamental_dir=fundamental_by_instru_dir,
                                        major_minor_dir=major_minor_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "SGM":
            cal_factors_exposure_sgm_mp(proc_num=proc_num, sgm_windows=factors_args["SGM"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
        if factor == "SIZE":
            cal_factors_exposure_size_mp(proc_num=proc_num, size_windows=factors_args["SIZE"],
                                         run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                         concerned_instruments_universe=concerned_instruments_universe,
                                         factors_exposure_dir=factors_exposure_dir,
                                         major_return_dir=major_return_dir,
                                         calendar_path=calendar_path,
                                         database_structure=database_structure,
                                         )
        if factor == "SKEW":
            cal_factors_exposure_skew_mp(proc_num=proc_num, skew_windows=factors_args["SKEW"],
                                         run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                         concerned_instruments_universe=concerned_instruments_universe,
                                         factors_exposure_dir=factors_exposure_dir,
                                         major_return_dir=major_return_dir,
                                         calendar_path=calendar_path,
                                         database_structure=database_structure,
                                         )
        if factor == "TO":
            cal_factors_exposure_to_mp(proc_num=proc_num, to_windows=factors_args["TO"],
                                       run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                       concerned_instruments_universe=concerned_instruments_universe,
                                       factors_exposure_dir=factors_exposure_dir,
                                       major_return_dir=major_return_dir,
                                       calendar_path=calendar_path,
                                       database_structure=database_structure,
                                       )
        if factor == "TS":
            cal_factors_exposure_ts_mp(proc_num=proc_num, ts_windows=factors_args["TS"],
                                       run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                       concerned_instruments_universe=concerned_instruments_universe,
                                       factors_exposure_dir=factors_exposure_dir,
                                       major_minor_dir=major_minor_dir,
                                       md_dir=md_by_instru_dir,
                                       calendar_path=calendar_path,
                                       database_structure=database_structure,
                                       )
        if factor == "VOL":
            cal_factors_exposure_vol_mp(proc_num=proc_num, vol_windows=factors_args["VOL"],
                                        run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
                                        concerned_instruments_universe=concerned_instruments_universe,
                                        factors_exposure_dir=factors_exposure_dir,
                                        major_return_dir=major_return_dir,
                                        calendar_path=calendar_path,
                                        database_structure=database_structure,
                                        )
    elif switch in ["FEN"]:
        cal_factors_neutral_mp(
            proc_num=proc_num, factors=factors,
            neutral_method=neutral_method,
            run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
            concerned_instruments_universe=concerned_instruments_universe,
            sector_classification=sector_classification,
            available_universe_dir=available_universe_dir,
            factors_exposure_dir=factors_exposure_dir,
            factors_exposure_neutral_dir=factors_exposure_neutral_dir,
            database_structure=database_structure,
        )
    else:
        print(f"... switch = {switch} is not a legal option, please check again.")
