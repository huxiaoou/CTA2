from setup_factor_and_portfolio import os, pd, dt
from setup_factor_and_portfolio import calendar_path
from setup_factor_and_portfolio import signals_dir, misc_dir
from setup_factor_and_portfolio import signals_allocation_dir
from config_portfolio import allocation_options
from lib_data_structure_portfolio import database_structure
from skyrim.whiterun import CCalendar
from skyrim.falkreath import CManagerLibReader, CManagerLibWriterByDate
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

cne_calendar = CCalendar(t_path=calendar_path)

for allocation_id, allocation_subsets in allocation_options.items():
    # --- initialize
    allocation_lib = CManagerLibWriterByDate(
        t_db_save_dir=signals_allocation_dir, t_db_name=database_structure[allocation_id].m_lib_name)
    allocation_lib.initialize_table(t_table=database_structure[allocation_id].m_tab, t_remove_existence=run_mode in ["O"])

    # --- load component factors
    signal_readers = {}
    for allocation_details in allocation_subsets.values():
        for comp_factor, comp_factor_id in allocation_details.items():
            if comp_factor not in signal_readers:
                signal_readers[comp_factor] = CManagerLibReader(
                    t_db_save_dir=signals_dir, t_db_name=database_structure[comp_factor_id].m_lib_name)
                signal_readers[comp_factor].set_default(database_structure[comp_factor_id].m_tab.m_table_name)

    # --- init before loop
    key_dates = list(allocation_subsets)
    key_dates.sort(reverse=True)
    win_i = 0
    while (win_bgn_date := key_dates[win_i]) > bgn_date:
        win_i += 1

    # --- core daily loop
    allocation_details = allocation_subsets[key_dates[win_i]]
    for trade_date in cne_calendar.get_iter_list(t_bgn_date=bgn_date, t_stp_date=stp_date, t_ascending=True):
        if trade_date >= key_dates[win_i - 1]:
            win_i -= 1
            allocation_details = allocation_subsets[key_dates[win_i]]

        comp_weight_data = {}
        for comp_factor, comp_factor_id in allocation_details.items():
            comp_factor_df = signal_readers[comp_factor].read_by_date(
                t_trade_date=trade_date, t_value_columns=["instrument", "value"]
            ).set_index("instrument")
            comp_weight_data[comp_factor] = comp_factor_df["value"]
        comp_weight_df = pd.DataFrame(comp_weight_data)

        allocation_weight_srs = comp_weight_df.mean(axis=1)
        allocation_weight_abs_sum = allocation_weight_srs.abs().sum()
        allocation_weight_srs = allocation_weight_srs / allocation_weight_abs_sum
        allocation_weight_df = pd.DataFrame({"value": allocation_weight_srs})
        allocation_lib.update_by_date(
            t_date=trade_date,
            t_update_df=allocation_weight_df,
            t_using_index=True
        )

    # --- close component factors library
    for comp_factor, comp_factor_lib in signal_readers.items():
        comp_factor_lib.close()

    allocation_lib.close()
    print("... {} solution factors are calculated".format(dt.datetime.now()))
