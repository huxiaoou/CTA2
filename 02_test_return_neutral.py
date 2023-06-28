from setup_factor_and_portfolio import dt, np, pd
from setup_factor_and_portfolio import calendar_path, available_universe_dir, test_return_dir, test_return_neutral_dir
from config_factor import test_window_list, instruments_universe_options, universe_id, neutral_method
from config_factor import sector_classification
from lib_data_structure import database_structure
from skyrim.falkreath import CManagerLibReader, CManagerLibWriterByDate
from skyrim.whiterun import CCalendar
from custom.XFuns import neutralize_by_sector
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

# --- calendar
cne_calendar = CCalendar(t_path=calendar_path)

# --- available universe
available_universe_lib_structure = database_structure["available_universe"]
available_universe_lib = CManagerLibReader(t_db_name=available_universe_lib_structure.m_lib_name, t_db_save_dir=available_universe_dir)
available_universe_lib.set_default(available_universe_lib_structure.m_tab.m_table_name)

# --- mother universe
mother_universe = instruments_universe_options[universe_id]
mother_universe_df = pd.DataFrame({"instrument": mother_universe})

# --- sector df
sector_df = pd.DataFrame.from_dict({z: {sector_classification[z]: 1} for z in mother_universe}, orient="index").fillna(0)

for test_window in test_window_list:
    weight_id = "WGT{:02d}".format(test_window)

    # --- test return library
    test_return_lib_id = "test_return_{:03d}".format(test_window)
    test_return_lib_structure = database_structure[test_return_lib_id]
    test_return_lib = CManagerLibReader(t_db_name=test_return_lib_structure.m_lib_name, t_db_save_dir=test_return_dir)
    test_return_lib.set_default(test_return_lib_structure.m_tab.m_table_name)

    # --- test return neutral library
    test_return_neutral_lib_id = "test_return_{:03d}.{}".format(test_window, neutral_method)
    test_return_neutral_lib_structure = database_structure[test_return_neutral_lib_id]
    test_return_neutral_lib = CManagerLibWriterByDate(t_db_name=test_return_neutral_lib_structure.m_lib_name, t_db_save_dir=test_return_neutral_dir)
    test_return_neutral_lib.initialize_table(t_table=test_return_neutral_lib_structure.m_tab, t_remove_existence=run_mode in ["O"])

    # --- update by date
    for trade_date in cne_calendar.get_iter_list(t_bgn_date=bgn_date, t_stp_date=stp_date, t_ascending=True):
        test_return_df = test_return_lib.read_by_date(
            t_trade_date=trade_date,
            t_value_columns=["instrument", "value"]
        )
        if len(test_return_df) == 0:
            continue

        weight_df = available_universe_lib.read_by_date(
            t_trade_date=trade_date,
            t_value_columns=["instrument", weight_id]
        )
        if len(weight_df) == 0:
            continue

        input_df = mother_universe_df.merge(
            right=weight_df, on=["instrument"], how="inner"
        ).merge(
            right=test_return_df, on=["instrument"], how="inner"
        ).set_index("instrument")

        if neutral_method == "WE":
            input_df[weight_id] = 1
        elif neutral_method == "WS":
            input_df[weight_id] = np.sqrt(input_df[weight_id])

        test_return_neutral_srs = neutralize_by_sector(
            t_raw_data=input_df["value"],
            t_sector_df=sector_df,
            t_weight=input_df[weight_id]
        )

        test_return_neutral_lib.update_by_date(
            t_date=trade_date,
            t_update_df=pd.DataFrame({"value": test_return_neutral_srs}),
            t_using_index=True
        )

    test_return_lib.close()
    test_return_neutral_lib.close()

    print("... @ {} Neutralization for test return {:03d} of {} calculated".format(dt.datetime.now(), test_window, neutral_method))

available_universe_lib.close()
