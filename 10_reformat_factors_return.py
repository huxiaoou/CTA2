from setup_factor_and_portfolio import sys, os, pd
from setup_factor_and_portfolio import factors_return_dir, factors_return_reformat_dir
from config_factor import neutral_method
from config_portfolio import pid, available_factors_list
from config_portfolio import factors_return_lag
from struct_lib import database_structure
from skyrim.falkreath import CManagerLibReader

test_window = int(sys.argv[1])

print("... reformat factors return ", pid, neutral_method, "TW{:03d}".format(test_window), "T{}".format(factors_return_lag))

# --- load lib: factors_return/instruments_residual
factors_return_lib_id = "factors_return.{}.{}.TW{:03d}.T{}".format(pid, neutral_method, test_window, factors_return_lag)
factors_return_lib = CManagerLibReader(t_db_save_dir=factors_return_dir, t_db_name=database_structure[factors_return_lib_id].m_lib_name)
factors_return_lib.set_default(database_structure[factors_return_lib_id].m_tab.m_table_name)

# --- core loop
factors_return_df = factors_return_lib.read(t_value_columns=["trade_date", "factor", "value"])
factors_return_agg_df = pd.pivot_table(data=factors_return_df, index="trade_date", columns="factor", values="value", aggfunc=sum)
factors_return_agg_df = factors_return_agg_df.sort_index(ascending=True)
factors_return_agg_df = factors_return_agg_df[available_factors_list]
factors_return_agg_file = "{}.csv.gz".format(factors_return_lib_id)
factors_return_agg_path = os.path.join(factors_return_reformat_dir, factors_return_agg_file)
factors_return_agg_df.to_csv(factors_return_agg_path, index_label="trade_date", float_format="%.8f")

factors_return_lib.close()
