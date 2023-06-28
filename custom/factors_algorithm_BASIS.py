import os
import datetime as dt
import pandas as pd
from typing import List, Dict
from skyrim.falkreath import CManagerLibWriterByDate, CLib1Tab1


def factors_algorithm_BASIS(
        basis_window: int,
        concerned_instruments_universe: List[str],
        database_structure: Dict[str, CLib1Tab1],
        factors_exposure_dir: str,
        md_bgn_date: str,
        md_stp_date: str,
        fundamental_dir: str,
        major_minor_dir: str,
):
    factor_lbl = "BASIS{:03d}".format(basis_window)

    # --- calculate factors by instrument
    all_factor_data = {}
    for instrument in concerned_instruments_universe:
        instrument_file = "{}.BASIS.csv.gz".format(instrument)
        instrument_path = os.path.join(fundamental_dir, instrument_file)
        instrument_df = pd.read_csv(instrument_path, dtype={"trade_date": str}).set_index("trade_date")

        major_minor_file = "major_minor.{}.csv.gz".format(instrument)
        major_minor_path = os.path.join(major_minor_dir, major_minor_file)
        major_minor_df = pd.read_csv(major_minor_path, dtype={"trade_date": str}).set_index("trade_date")

        instrument_df: pd.DataFrame = pd.merge(left=major_minor_df, right=instrument_df, how="left", left_index=True, right_index=True)

        instrument_df = instrument_df.fillna(method="ffill").fillna(0)
        # instrument_df[factor_lbl] = instrument_df["ANAL_BASISPERCENT2"].rolling(window=basis_window).mean()
        instrument_df[factor_lbl] = instrument_df["basis_rate"].rolling(window=basis_window).mean()
        all_factor_data[instrument] = instrument_df[factor_lbl]

    # --- reorganize
    all_factor_df = pd.DataFrame(all_factor_data)

    # --- save
    factor_lib_structure = database_structure[factor_lbl]
    factor_lib = CManagerLibWriterByDate(
        t_db_name=factor_lib_structure.m_lib_name,
        t_db_save_dir=factors_exposure_dir
    )
    factor_lib.initialize_table(t_table=factor_lib_structure.m_tab)
    factor_lib.save_factor_by_date(
        t_all_factor_df=all_factor_df,
        t_bgn_date=md_bgn_date, t_stp_date=md_stp_date,
    )
    factor_lib.close()

    print("... @ {} factor = {:>12s} calculated".format(dt.datetime.now(), factor_lbl))
    return 0
