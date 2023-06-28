from setup_factor_and_portfolio import os, dt, pd
from setup_factor_and_portfolio import factors_return_reformat_dir, calendar_path
from setup_factor_and_portfolio import factors_portfolio_dir, signals_dir
from config_factor import neutral_method, RETURN_SCALE
from config_portfolio import pid, factors_return_lag
from config_portfolio import available_factors_list
from struct_lib_portfolio import database_structure
from skyrim.whiterun import CCalendar
from skyrim.falkreath import CManagerLibReader, CManagerLibWriterByDate
import argparse

args_parser = argparse.ArgumentParser(description="To update available universe")
args_parser.add_argument("-t", "--testWin", type=int, help="test window or hold period, must be one of [3,5,10,15,20]")
args_parser.add_argument("-m", "--mode", type=str, help="A string, must be one of ['o', 'a'], 'o' for 'overwrite', 'a' for 'append'")
args_parser.add_argument("-b", "--bgn", type=str, help="format = [YYYYMMDD], must be provided in any case")
args_parser.add_argument("-s", "--stp", type=str, help="format = [YYYYMMDD], can be omit if mode = 'o'", default="")

args = args_parser.parse_args()
test_window = args.testWin
run_mode = args.mode.upper()
bgn_date, stp_date = args.bgn, args.stp
if stp_date == "":
    stp_date = (dt.datetime.strptime(bgn_date, "%Y%m%d") + dt.timedelta(days=1)).strftime("%Y%m%d")

print("... pure factors signals VANILLA ", pid, neutral_method, "TW{:03d}".format(test_window), "T{}".format(factors_return_lag))
test_id = "{}.{}.TW{:03d}.T{}".format(pid, neutral_method, test_window, factors_return_lag)

# --- load calendar
cne_calendar = CCalendar(t_path=calendar_path)

# --- load lib: factors_return/instruments_residual
factors_return_lib_id = "factors_return.{}".format(test_id)
factors_return_agg_file = "{}.csv.gz".format(factors_return_lib_id)
factors_return_agg_path = os.path.join(factors_return_reformat_dir, factors_return_agg_file)
factors_return_agg_df = pd.read_csv(factors_return_agg_path, dtype={"trade_date": str}).set_index("trade_date") / RETURN_SCALE
factors_return_agg_df = factors_return_agg_df[available_factors_list]
factors_return_agg_cumsum_df = factors_return_agg_df.cumsum()

# --- pure factor portfolio data
factors_portfolio_lib_id = "factors_portfolio.{}".format(test_id)
factors_portfolio_lib = CManagerLibReader(t_db_save_dir=factors_portfolio_dir, t_db_name=database_structure[factors_portfolio_lib_id].m_lib_name)
factors_portfolio_lib.set_default(database_structure[factors_portfolio_lib_id].m_tab.m_table_name)

# --- signals writer
signals_writers = {}
for factor in available_factors_list:
    signal_lib_id = "pure_factors_VANILLA.{}.TW{:03d}".format(factor, test_window)
    signal_lib = CManagerLibWriterByDate(t_db_save_dir=signals_dir, t_db_name=database_structure[signal_lib_id].m_lib_name)
    signal_lib.initialize_table(t_table=database_structure[signal_lib_id].m_tab, t_remove_existence=run_mode in ["O"])
    signals_writers[factor] = {
        "id": signal_lib_id,
        "lib": signal_lib,
    }

# --- main loop
for trade_date in cne_calendar.get_iter_list(
        t_bgn_date=max(factors_return_agg_df.dropna(axis=0).index[0], bgn_date),
        t_stp_date=stp_date, t_ascending=True):

    factors_portfolio_df = factors_portfolio_lib.read_by_date(
        t_trade_date=trade_date,
        t_value_columns=["instrument"] + available_factors_list
    ).set_index("instrument")

    wgt_abs_sum = factors_portfolio_df.abs().sum()
    wgt_norm_df = factors_portfolio_df / wgt_abs_sum
    wgt_df = wgt_norm_df

    for factor in available_factors_list:
        signal_lib_id = signals_writers[factor]["id"]
        signal_lib = signals_writers[factor]["lib"]
        signal_lib.update_by_date(
            t_date=trade_date,
            t_update_df=wgt_df[[factor]],
            t_using_index=True
        )

for factor in available_factors_list:
    signals_writers[factor]["lib"].close()

factors_portfolio_lib.close()
