from setup_factor_and_portfolio import np, pd, dt
from setup_factor_and_portfolio import calendar_path
from setup_factor_and_portfolio import available_universe_dir, factors_exposure_dir
from setup_factor_and_portfolio import signals_allocation_dir
from config_portfolio import instruments_universe_options, universe_id
from config_portfolio import synth_options
from struct_lib_portfolio import database_structure
from typing import Dict
from skyrim.whiterun import CCalendar
from skyrim.falkreath import CManagerLibReader, CManagerLibWriterByDate
import argparse


def get_weight_from_factor_head_tail_equal(t_raw_factor_srs: pd.Series, t_single_hold_prop: float):
    tot_size = len(t_raw_factor_srs)
    k0 = max(min(int(np.ceil(tot_size * t_single_hold_prop)), int(tot_size / 2)), 1)
    k1 = tot_size - 2 * k0
    t_weight_srs = pd.Series(
        data=[1 / 2 / k0] * k0 + [0.0] * k1 + [-1 / 2 / k0] * k0,
        index=t_raw_factor_srs.sort_values(ascending=False).index
    )
    return t_weight_srs


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

test_universe = instruments_universe_options[universe_id]
test_universe_srs = pd.Series(data=1, index=test_universe)

# --- load available universe
available_universe_lib_structure = database_structure["available_universe"]
available_universe_lib = CManagerLibReader(t_db_name=available_universe_lib_structure.m_lib_name, t_db_save_dir=available_universe_dir)
available_universe_lib.set_default(available_universe_lib_structure.m_tab.m_table_name)

for synth_factor, synth_factor_details in synth_options.items():
    weight_srs = pd.Series({k: v["weight"] for k, v in synth_factor_details.items()})

    # --- initialize
    allocation_lib = CManagerLibWriterByDate(
        t_db_save_dir=signals_allocation_dir, t_db_name=database_structure[synth_factor].m_lib_name)
    allocation_lib.initialize_table(t_table=database_structure[synth_factor].m_tab, t_remove_existence=run_mode in ["O"])

    # --- load component factors
    signal_readers: Dict[str, CManagerLibReader] = {}
    for comp_factor in synth_factor_details:
        signal_readers[comp_factor] = CManagerLibReader(
            t_db_save_dir=factors_exposure_dir, t_db_name=database_structure[comp_factor].m_lib_name)
        signal_readers[comp_factor].set_default(database_structure[comp_factor].m_tab.m_table_name)

    for trade_date in cne_calendar.get_iter_list(t_bgn_date=bgn_date, t_stp_date=stp_date, t_ascending=True):
        # Load available universe
        available_universe_df = available_universe_lib.read_by_date(
            t_trade_date=trade_date,
            t_value_columns=["instrument", "amount"]
        ).set_index("instrument")
        if len(available_universe_df) == 0:
            continue

        # get intersection with test universe
        available_universe_df["target"] = test_universe_srs
        available_universe_df = available_universe_df.loc[available_universe_df["target"] == 1]

        # load weight for each factor
        weight_data = {}
        for comp_factor, comp_factor_config in synth_factor_details.items():
            factor_df = signal_readers[comp_factor].read_by_date(
                t_trade_date=trade_date,
                t_table_name=database_structure[comp_factor].m_tab.m_table_name,
                t_value_columns=["instrument", "value"]
            ).set_index("instrument")
            available_universe_df[comp_factor] = factor_df["value"]  # use this to drop instruments that are not available
            weight_data[comp_factor] = get_weight_from_factor_head_tail_equal(
                t_raw_factor_srs=available_universe_df[comp_factor],
                t_single_hold_prop=comp_factor_config["SHP"]
            )

        weight_df = pd.DataFrame(weight_data)
        weight_df["weighted_sum"] = weight_df.dot(weight_srs)
        wgt_abs_sum = weight_df["weighted_sum"].abs().sum()
        weight_df[synth_factor] = weight_df["weighted_sum"] / wgt_abs_sum

        allocation_lib.update_by_date(
            t_date=trade_date,
            t_update_df=weight_df[[synth_factor]],
            t_using_index=True
        )

    # --- close component factors library
    for comp_factor, comp_factor_lib in signal_readers.items():
        comp_factor_lib.close()

    allocation_lib.close()
    print("... {}  raw synth factors = {} is calculated".format(dt.datetime.now(), synth_factor))

available_universe_lib.close()
