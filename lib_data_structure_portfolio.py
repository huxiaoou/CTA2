from config_portfolio import available_factors_list, timing_factors_list, fast_n_slow_n_comb, allocation_options, synth_options
from config_portfolio import test_window_list
from lib_data_structure import database_structure, CLib1Tab1, CTable, ittl

# update @ 2022-11-16
pure_factors_list = ["pure_factors_VANILLA.{}.TW{:03d}".format(f, tw) for f, tw in ittl.product(available_factors_list, test_window_list)]
for z in pure_factors_list:
    database_structure.update({
        z: CLib1Tab1(
            t_lib_name=z + ".db",
            t_tab=CTable({
                "table_name": z.split(".")[0],
                "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
                "value_columns": {"value": "REAL"},
            })
        )
    })

pure_factors_list = ["pure_factors_MA.{}.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(f, tw, fn, sn)
                     for f, tw, (fn, sn) in ittl.product(available_factors_list, test_window_list, fast_n_slow_n_comb)]
for z in pure_factors_list:
    database_structure.update({
        z: CLib1Tab1(
            t_lib_name=z + ".db",
            t_tab=CTable({
                "table_name": z.split(".")[0],
                "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
                "value_columns": {"value": "REAL"},
            })
        )
    })

for z in allocation_options:
    database_structure.update({
        z: CLib1Tab1(
            t_lib_name=z + ".db",
            t_tab=CTable({
                "table_name": z.split(".")[0],
                "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
                "value_columns": {"value": "REAL"},
            })
        )
    })

for z in synth_options:
    database_structure.update({
        z: CLib1Tab1(
            t_lib_name=z + ".db",
            t_tab=CTable({
                "table_name": z.split(".")[0],
                "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
                "value_columns": {"value": "REAL"},
            })
        )
    })

# --- for optimization vanilla factor
for factor_lbl, mov_ave_len in ittl.product(available_factors_list, test_window_list):
    z = "{}VM{:03d}".format(factor_lbl, mov_ave_len)
    database_structure.update({
        z: CLib1Tab1(
            t_lib_name=z + ".db",
            t_tab=CTable({
                "table_name": z,
                "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
                "value_columns": {"value": "REAL"},
            })
        )
    })

# --- for optimization MA factor
for factor_lbl, mov_ave_len, (fn, sn) in ittl.product(timing_factors_list, test_window_list, fast_n_slow_n_comb):
    z = "{}F{:03d}S{:03d}M{:03d}".format(factor_lbl, fn, sn, mov_ave_len)
    database_structure.update({
        z: CLib1Tab1(
            t_lib_name=z + ".db",
            t_tab=CTable({
                "table_name": z,
                "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
                "value_columns": {"value": "REAL"},
            })
        )
    })

# --- for optimization allocation
for aid, mov_ave_len in ittl.product(list(synth_options) + list(allocation_options), test_window_list):
    z = "{}M{:03d}".format(aid, mov_ave_len)
    database_structure.update({
        z: CLib1Tab1(
            t_lib_name=z + ".db",
            t_tab=CTable({
                "table_name": z,
                "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
                "value_columns": {"value": "REAL"},
            })
        )
    })
