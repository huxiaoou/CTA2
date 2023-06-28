from setup_factor_and_portfolio import ittl
from skyrim.falkreath import CLib1Tab1, CTable, Dict
from config_factor import factors_pool_options, instruments_universe_options, universe_id, sector_classification
from config_factor import test_window_list, factors_return_lag_list, factors_list, sectors_list

# --- DATABASE STRUCTURE
# available universe structure
database_structure: Dict[str, CLib1Tab1] = {
    "available_universe": CLib1Tab1(
        t_lib_name="available_universe.db",
        t_tab=CTable({
            "table_name": "available_universe",
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {
                **{"return": "REAL", "amount": "REAL"},
                **{"WGT{:02d}".format(z): "REAL" for z in test_window_list}
            }
        })
    )}

# test return structure
test_return_lbl_list = ["test_return_{:03d}".format(w) for w in test_window_list]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z,
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {"value": "REAL"},
        })
    ) for z in test_return_lbl_list})

# test return neutral structure
test_return_neutral_lbl_list = ["test_return_{:03d}.WS".format(w) for w in test_window_list]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z.split(".")[0],
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {"value": "REAL"},
        })
    ) for z in test_return_neutral_lbl_list})

# factor structure
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z,
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {"value": "REAL"},
        })
    ) for z in factors_list})

# factors neutral structure
factors_neutral_list = ["{}.WS".format(f) for f in factors_list]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z.split(".")[0],
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {"value": "REAL"},
        })
    ) for z in factors_neutral_list})

# norm factors pool
norm_factors_pool_list = ["{}.WS.NORM".format(p) for p in factors_pool_options]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z.split(".")[0],
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {f: "REAL" for f in factors_pool_options[z.split(".")[0]]},
        })
    ) for z in norm_factors_pool_list})

# delinear factors pool
delinear_factors_pool_list = ["{}.WS.DELINEAR".format(p) for p in factors_pool_options]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z.split(".")[0],
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {f: "REAL" for f in factors_pool_options[z.split(".")[0]]},
        })
    ) for z in delinear_factors_pool_list})

# factors return lib
factors_return_list = ["factors_return.{}.WS.TW{:03d}.T{}".format(p, tw, l)
                       for p, tw, l in ittl.product(factors_pool_options.keys(), test_window_list, factors_return_lag_list)]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z.split(".")[0],
            "primary_keys": {"trade_date": "TEXT", "factor": "TEXT"},
            "value_columns": {"value": "REAL"},
        })
    ) for z in factors_return_list})

# factors delinear test ic lib
factors_delinear_test_ic_list = ["factors_delinear_test_ic.{}.WS.TW{:03d}.T{}".format(p, tw, l)
                                 for p, tw, l in ittl.product(factors_pool_options.keys(), test_window_list, factors_return_lag_list)]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z.split(".")[0],
            "primary_keys": {"trade_date": "TEXT", "factor": "TEXT"},
            "value_columns": {"value": "REAL"},
        })
    ) for z in factors_delinear_test_ic_list})

# instrument residual lib
instrument_residual_list = ["instruments_residual.{}.WS.TW{:03d}.T{}".format(p, tw, l)
                            for p, tw, l in ittl.product(factors_pool_options.keys(), test_window_list, factors_return_lag_list)]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z.split(".")[0],
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {"value": "REAL"},
        })
    ) for z in instrument_residual_list})

# factors portfolio lib
factors_portfolio_list = ["factors_portfolio.{}.WS.TW{:03d}.T{}".format(p, tw, l)
                          for p, tw, l in ittl.product(factors_pool_options.keys(), test_window_list, factors_return_lag_list)]
for z in factors_portfolio_list:
    # selected sectors list
    mother_universe = instruments_universe_options[universe_id]
    sector_set = {sector_classification[u] for u in mother_universe}  # this set may be a subset of sectors_list and in random order
    selected_sectors_list = [z for z in sectors_list if z in sector_set]  # sort sector set by sectors list order

    # selected factors pool
    selected_factors_pool = factors_pool_options[z.split(".")[1]]

    database_structure.update({
        z: CLib1Tab1(
            t_lib_name=z + ".db",
            t_tab=CTable({
                "table_name": z.split(".")[0],
                "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
                "value_columns": {f: "REAL" for f in ["MARKET"] + selected_sectors_list + selected_factors_pool}
            })
        )})

# IV lib
iv_list = ["IV{}WSTW{:03d}T{}".format(p, tw, l)
           for p, tw, l in ittl.product(factors_pool_options.keys(), test_window_list, factors_return_lag_list)]
database_structure.update({
    z: CLib1Tab1(
        t_lib_name=z + ".db",
        t_tab=CTable({
            "table_name": z,
            "primary_keys": {"trade_date": "TEXT", "instrument": "TEXT"},
            "value_columns": {"value": "REAL"},
        })
    ) for z in iv_list})

if __name__ == "__main__":
    print(norm_factors_pool_list)
    print(database_structure["P3.WS.NORM"].m_tab.m_value_columns)
