from setup_factor_and_portfolio import os, dt, pd
from setup_factor_and_portfolio import instruments_return_dir, test_return_dir
from config_factor import test_window_list, RETURN_SCALE
from lib_data_structure import database_structure
from custom.XFuns import cal_period_return
from skyrim.falkreath import CManagerLibWriterByDate
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

# load raw return
raw_return_file = "instruments.return.csv.gz"
raw_return_path = os.path.join(instruments_return_dir, raw_return_file)
raw_return_df = pd.read_csv(raw_return_path, dtype={"trade_date": str}).set_index("trade_date")
trailing_window = max(test_window_list) * 3
return_md_bgn_date = (dt.datetime.strptime(bgn_date, "%Y%m%d") - dt.timedelta(days=trailing_window)).strftime("%Y%m%d")
raw_return_df = raw_return_df.loc[raw_return_df.index >= return_md_bgn_date]
print(raw_return_df)

for test_window in test_window_list:
    # --- initialize lib
    test_return_lib_id = "test_return_{:03d}".format(test_window)
    test_return_lib_structure = database_structure[test_return_lib_id]
    test_return_lib = CManagerLibWriterByDate(t_db_name=test_return_lib_structure.m_lib_name, t_db_save_dir=test_return_dir)
    test_return_lib.initialize_table(t_table=test_return_lib_structure.m_tab, t_remove_existence=run_mode in ["O"])

    rolling_return_df = raw_return_df.rolling(window=test_window).apply(cal_period_return, args=(RETURN_SCALE,))
    test_rolling_return_df = rolling_return_df
    for trade_date, trade_date_df in test_rolling_return_df.groupby(by="trade_date"):
        if trade_date < bgn_date or trade_date >= stp_date:
            continue

        save_df = trade_date_df.T.dropna(axis=0)
        if len(save_df) > 0:
            test_return_lib.update_by_date(t_date=trade_date, t_update_df=save_df, t_using_index=True)

    test_return_lib.close()
    print("... @ {}, test return for TW = {:>3d} are calculated".format(dt.datetime.now(), test_window))
