from setup_factor_and_portfolio import dt, os, pd
from setup_factor_and_portfolio import available_universe_dir, major_return_dir
from config_factor import concerned_instruments_universe, available_universe_rolling_window, available_universe_amt_threshold
from config_factor import price_type, WANYUAN, YIYUAN, test_window_list
from struct_lib import database_structure
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

print("... {} available universe calculating".format(dt.datetime.now()))

# --- initialize lib
available_universe_lib_structure = database_structure["available_universe"]
available_universe_lib = CManagerLibWriterByDate(t_db_name=available_universe_lib_structure.m_lib_name, t_db_save_dir=available_universe_dir)
available_universe_lib.initialize_table(t_table=available_universe_lib_structure.m_tab, t_remove_existence=run_mode in ["O"])

# --- load all amount and return data
amt_ma_data_for_available = {}
amt_ma_data_for_test = {test_window: {} for test_window in test_window_list}
amt_data = {}
return_data = {}
for instrument in concerned_instruments_universe:
    major_return_file = "major_return.{}.{}.csv.gz".format(instrument, price_type)
    major_return_path = os.path.join(major_return_dir, major_return_file)
    major_return_df = pd.read_csv(major_return_path, dtype={"trade_date": str}).set_index("trade_date")
    amt_ma_data_for_available[instrument] = major_return_df["amount"].rolling(window=available_universe_rolling_window).mean() * WANYUAN / YIYUAN
    for test_window in test_window_list:
        amt_ma_data_for_test[test_window][instrument] = major_return_df["amount"].rolling(window=test_window).mean() * WANYUAN / YIYUAN
    amt_data[instrument] = major_return_df["amount"] * WANYUAN / YIYUAN
    return_data[instrument] = major_return_df["major_return"]

# --- reorganize and save
amt_ma_df_for_available = pd.DataFrame(amt_ma_data_for_available)
amt_ma_df_for_test = {k: pd.DataFrame(v) for k, v in amt_ma_data_for_test.items()}
amt_df = pd.DataFrame(amt_data)
return_df = pd.DataFrame(return_data)
filter_df = amt_ma_df_for_available >= available_universe_amt_threshold
for trade_date, trade_date_filter_df in filter_df.groupby(by="trade_date"):
    if trade_date < bgn_date or trade_date >= stp_date:
        continue

    trade_date_filter = trade_date_filter_df.loc[trade_date]  # a list of instruments, use this as index to get available instruments
    available_universe_df = pd.DataFrame({
        "return": return_df.loc[trade_date, trade_date_filter],
        "amount": amt_df.loc[trade_date, trade_date_filter],
    })
    for k, v in amt_ma_df_for_test.items():
        available_universe_df["WGT{:02d}".format(k)] = v.loc[trade_date, trade_date_filter]

    # save to database
    available_universe_lib.update_by_date(
        t_date=trade_date,
        t_update_df=available_universe_df,
        t_using_index=True
    )

available_universe_lib.close()
print("... {} available universe calculated".format(dt.datetime.now()))
