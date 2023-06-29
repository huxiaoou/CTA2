import os
import datetime as dt
import pandas as pd
from skyrim.falkreath import CLib1Tab1, CManagerLibWriterByDate


def cal_available_universe(
        test_windows: list[int],
        run_mode: str, bgn_date: str, stp_date: str | None,
        instruments_universe: list[str],
        available_universe_options: dict[str, int | float],
        available_universe_dir: str,
        major_return_dir: str,
        database_structure: dict[str, CLib1Tab1],
        price_type: str = "close"):
    print("... {} available universe calculating".format(dt.datetime.now()))

    _wanyuan, _yiyuan = 1e4, 1e8
    rolling_win, amt_threshold = available_universe_options["rolling_window"], available_universe_options["amount_threshold"]

    # --- initialize lib
    available_universe_lib_structure = database_structure["available_universe"]
    available_universe_lib = CManagerLibWriterByDate(t_db_name=available_universe_lib_structure.m_lib_name, t_db_save_dir=available_universe_dir)
    available_universe_lib.initialize_table(t_table=available_universe_lib_structure.m_tab, t_remove_existence=run_mode in ["O"])

    # --- load all amount and return data
    amt_ma_data_for_available, amt_ma_data_for_test = {}, {test_window: {} for test_window in test_windows}
    amt_data, return_data = {}, {}
    for instrument in instruments_universe:
        major_return_file = "major_return.{}.{}.csv.gz".format(instrument, price_type)
        major_return_path = os.path.join(major_return_dir, major_return_file)
        major_return_df = pd.read_csv(major_return_path, dtype={"trade_date": str}).set_index("trade_date")
        amt_ma_data_for_available[instrument] = major_return_df["amount"].rolling(window=rolling_win).mean() * _wanyuan / _yiyuan
        for test_window in test_windows:
            amt_ma_data_for_test[test_window][instrument] = major_return_df["amount"].rolling(window=test_window).mean() * _wanyuan / _yiyuan
        amt_data[instrument] = major_return_df["amount"] * _wanyuan / _yiyuan
        return_data[instrument] = major_return_df["major_return"]

    # --- reorganize and save
    amt_ma_df_for_available = pd.DataFrame(amt_ma_data_for_available)
    amt_ma_df_for_test = {k: pd.DataFrame(v) for k, v in amt_ma_data_for_test.items()}
    amt_df = pd.DataFrame(amt_data)
    return_df = pd.DataFrame(return_data)
    filter_df = amt_ma_df_for_available >= amt_threshold
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
