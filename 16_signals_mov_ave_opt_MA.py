import pandas as pd
import itertools as ittl
import datetime as dt
from setup_factor_and_portfolio import calendar_path
from setup_factor_and_portfolio import signals_dir, signals_opt_dir
from skyrim.whiterun import CCalendar
from skyrim.falkreath import CManagerLibReader, CManagerLibWriterByDate
from config_factor import test_windows
from config_portfolio import minimum_abs_weight
from config_portfolio import timing_factors, fast_n_slow_n_comb
from struct_lib_portfolio import database_structure
import argparse

args_parser = argparse.ArgumentParser(description="To update available universe")
args_parser.add_argument("-m", "--mode", type=str, help="A string, must be one of ['o', 'a'], 'o' for 'overwrite', 'a' for 'append'")
args_parser.add_argument("-b", "--bgn", type=str, help="format = [YYYYMMDD], must be provided in any case")
args_parser.add_argument("-s", "--stp", type=str, help="format = [YYYYMMDD], can be omit if mode = 'o'", default="")

args = args_parser.parse_args()
run_mode = args.mode.upper()
bgn_date, stp_date = args.bgn, args.stp
if stp_date == "":
    stp_date = (dt.datetime.strptime(bgn_date, "%Y%m%d") + dt.timedelta(days=1)).strftime("%Y%m%d")
trailing_window = max(test_windows) * 3
ahead_bgn_date = (dt.datetime.strptime(bgn_date, "%Y%m%d") - dt.timedelta(days=trailing_window)).strftime("%Y%m%d")

# --- init calendar
cne_calendar = CCalendar(t_path=calendar_path)

for factor_lbl, mov_ave_len, (fn, sn) in ittl.product(timing_factors, test_windows, fast_n_slow_n_comb):
    src_id = "pure_factors_MA.{}.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(factor_lbl, mov_ave_len, fn, sn)
    dst_id = "{}F{:03d}S{:03d}M{:03d}".format(factor_lbl, fn, sn, mov_ave_len)
    src_dir = signals_dir

    # --- init src lib
    src_lib = CManagerLibReader(
        t_db_save_dir=src_dir, t_db_name=database_structure[src_id].m_lib_name)
    src_lib.set_default(database_structure[src_id].m_tab.m_table_name)

    # --- init allocation opt lib
    dst_opt_lib = CManagerLibWriterByDate(
        t_db_save_dir=signals_opt_dir, t_db_name=database_structure[dst_id].m_lib_name)
    dst_opt_lib.initialize_table(database_structure[dst_id].m_tab, t_remove_existence=run_mode in ["O"])

    # --- main
    signal_queue = []
    for trade_date in cne_calendar.get_iter_list(t_bgn_date=ahead_bgn_date, t_stp_date=stp_date, t_ascending=True):
        signal_df = src_lib.read_by_date(t_trade_date=trade_date, t_value_columns=["instrument", "value"]).set_index("instrument")
        if len(signal_df) > 0:
            signal_srs = signal_df["value"]
            signal_srs.name = trade_date

            # update queue, save the last mov_ave_len days' signal
            signal_queue.append(signal_srs)
            if len(signal_queue) > mov_ave_len:
                signal_queue.pop(0)

            # moving average of signals
            opt_df = pd.DataFrame(signal_queue).T
            opt_df["raw_ave"] = opt_df.fillna(0).mean(axis=1)
            filter_wgt_minimum = opt_df["raw_ave"].abs() > minimum_abs_weight
            opt_df = opt_df.loc[filter_wgt_minimum]
            opt_df["value"] = opt_df["raw_ave"] / opt_df["raw_ave"].abs().sum()

            # save
            if trade_date >= bgn_date:
                dst_opt_lib.update_by_date(
                    t_date=trade_date,
                    t_update_df=opt_df[["value"]],
                    t_using_index=True
                )

    src_lib.close()
    dst_opt_lib.close()

    print("... {} MOV_AVE = {:>2d} optimized @ {}".format(dst_id, mov_ave_len, dt.datetime.now()))
