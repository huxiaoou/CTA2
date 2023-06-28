import os
import datetime as dt
import pandas as pd
from typing import List, Dict
from skyrim.falkreath import CManagerLibWriterByDate, CLib1Tab1


def factors_algorithm_BETA(
        beta_window: int,
        concerned_instruments_universe: List[str],
        database_structure: Dict[str, CLib1Tab1],
        factors_exposure_dir: str,
        md_bgn_date: str,
        md_stp_date: str,
        instruments_return_dir: str,
        major_return_dir: str,
        price_type: str = "close",
):
    factor_lbl = "BETA{:03d}".format(beta_window)

    # --- load market return
    market_index_file = "market.return.csv.gz"
    market_index_path = os.path.join(instruments_return_dir, market_index_file)
    market_index_df = pd.read_csv(market_index_path, dtype={"trade_date": str}).set_index("trade_date")

    # --- calculate factors by instrument
    all_factor_data = {}
    for instrument in concerned_instruments_universe:
        major_return_file = "major_return.{}.{}.csv.gz".format(instrument, price_type)
        major_return_path = os.path.join(major_return_dir, major_return_file)
        major_return_df = pd.read_csv(major_return_path, dtype={"trade_date": str}).set_index("trade_date")
        major_return_df["market"] = market_index_df["market"]
        major_return_df["xy"] = (major_return_df["major_return"] * major_return_df["market"]).rolling(window=beta_window).mean()
        major_return_df["xx"] = (major_return_df["market"] * major_return_df["market"]).rolling(window=beta_window).mean()
        major_return_df["y"] = major_return_df["major_return"].rolling(window=beta_window).mean()
        major_return_df["x"] = major_return_df["market"].rolling(window=beta_window).mean()

        major_return_df["cov_xy"] = major_return_df["xy"] - major_return_df["x"] * major_return_df["y"]
        major_return_df["cov_xx"] = major_return_df["xx"] - major_return_df["x"] * major_return_df["x"]
        major_return_df[factor_lbl] = major_return_df["cov_xy"] / major_return_df["cov_xx"]
        all_factor_data[instrument] = major_return_df[factor_lbl]

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