import argparse
from returns.instrument_return import merge_instru_return
from returns.available_universe import cal_available_universe
from returns.market_return import cal_market_return
from returns.test_return import cal_test_return
from returns.test_return_neutral import cal_test_return_neutral

from setup_factor_and_portfolio import major_return_dir, \
    instruments_return_dir, available_universe_dir, \
    test_return_dir, test_return_neutral_dir
from setup_factor_and_portfolio import calendar_path
from config_factor import concerned_instruments_universe, sector_classification, \
    available_universe_options, test_windows, neutral_method
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
            "returns/test_return": "20130101",
            "returns/test_return_neutral": "20130101",
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
    run_mode = args.mode.upper() if switch in ["AU", "TR", "TRN"] else None
    bgn_date, stp_date = args.bgn, args.stp
    proc_num = args.process
    factor = args.factor.lower()

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
        cal_test_return(
            test_windows=test_windows,
            run_mode=run_mode, bgn_date=bgn_date, stp_date=stp_date,
            instruments_return_dir=instruments_return_dir,
            test_return_dir=test_return_dir,
            calendar_path=calendar_path,
            database_structure=database_structure
        )
    elif switch in ["TRN"]:  # "TEST RETURN NEUTRAL"
        cal_test_return_neutral(
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
    else:
        print(f"... switch = {switch} is not a legal option, please check again.")
