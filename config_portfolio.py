from config_factor import test_windows
from config_factor import sectors, sector_classification
from config_factor import instruments_universe_options, universe_id
from config_factor import factors_pool_options, factors

hold_period_n_list = test_windows
factors_return_lag = 0  # the core difference between "Project_2022_11_Commodity_Factors_Return_Analysis_V4B"

# secondary parameters
cost_rate = 5e-4
cost_reservation = 0e-4
risk_free_rate = 0
top_n = 5
init_premium = 10000 * 1e4
minimum_abs_weight = 0.001

# Local
pid = "P3"
selected_sectors_list = [z for z in sectors if z in set(sector_classification[i] for i in instruments_universe_options[universe_id])]
selected_factors_list = factors_pool_options[pid]
available_factors_list = ["MARKET"] + selected_sectors_list + selected_factors_list
timing_factors_list = ["MARKET"] + selected_sectors_list

fast_n_slow_n_comb = (
    (5, 63),
    (5, 126),
    (21, 126),
    (21, 189),
)

FAR_END_DATE_IN_THE_FUTURE = "20330101"
allocation_options = {
    # Pure Factors: Long Term
    "A1": {
        FAR_END_DATE_IN_THE_FUTURE: {},
        "20230607": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(20),
            "BETA021": "pure_factors_VANILLA.BETA021.TW{:03d}".format(20),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(20),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(20),
        },
        "20221201": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(20),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(20),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(20),
            "RSW252HL063": "pure_factors_VANILLA.RSW252HL063.TW{:03d}".format(20),
        },
        "20170101": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(20),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(20),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(20),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(20),
            "RSW252HL063": "pure_factors_VANILLA.RSW252HL063.TW{:03d}".format(20),
        },
        "20120101": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(20),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(20),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(20),
        },
    },

    # Pure Factors: Short Term
    "A6": {
        FAR_END_DATE_IN_THE_FUTURE: {},
        "20230607": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(5),
            "BETA021": "pure_factors_VANILLA.BETA021.TW{:03d}".format(5),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(5),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(5),
        },
        "20221201": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(5),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(5),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(5),
            "RSW252HL063": "pure_factors_VANILLA.RSW252HL063.TW{:03d}".format(5),
        },
        "20170101": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(5),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(5),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(5),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(5),
            "RSW252HL063": "pure_factors_VANILLA.RSW252HL063.TW{:03d}".format(5),
        },
        "20120101": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(5),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(5),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(5),
        },
    },

    # Pure Factors: Long Term + SectorTiming
    "A3": {  # A3 = A1 + SectorTiming
        FAR_END_DATE_IN_THE_FUTURE: {},
        "20230607": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(20),
            "BETA021": "pure_factors_VANILLA.BETA021.TW{:03d}".format(20),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(20),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(20),

            "BLACK": "pure_factors_MA.BLACK.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 126),
            "CHEM": "pure_factors_MA.CHEM.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 189),
            "OIL": "pure_factors_MA.OIL.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 126),
            "MISC": "pure_factors_MA.MISC.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(10, 21, 126),
        },
        "20221201": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(20),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(20),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(20),
            "RSW252HL063": "pure_factors_VANILLA.RSW252HL063.TW{:03d}".format(20),

            "BLACK": "pure_factors_MA.BLACK.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 126),
            "CHEM": "pure_factors_MA.CHEM.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 189),
            "OIL": "pure_factors_MA.OIL.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 126),
            "MISC": "pure_factors_MA.MISC.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(10, 21, 126),
        },
        "20170101": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(20),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(20),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(20),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(20),
            "RSW252HL063": "pure_factors_VANILLA.RSW252HL063.TW{:03d}".format(20),

            "BLACK": "pure_factors_MA.BLACK.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 126),
            "CHEM": "pure_factors_MA.CHEM.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 189),
            "OIL": "pure_factors_MA.OIL.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 126),
            "MISC": "pure_factors_MA.MISC.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(10, 21, 126),
        },
        "20120101": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(20),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(20),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(20),

            "BLACK": "pure_factors_MA.BLACK.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 126),
            "CHEM": "pure_factors_MA.CHEM.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 189),
            "OIL": "pure_factors_MA.OIL.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(15, 21, 126),
            "MISC": "pure_factors_MA.MISC.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(10, 21, 126),
        },

    },

    # Pure Factors: Short Term + SectorTiming
    "A8": {  # A8 =  A6 + SectorTiming
        FAR_END_DATE_IN_THE_FUTURE: {},
        "20230607": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(5),
            "BETA021": "pure_factors_VANILLA.BETA021.TW{:03d}".format(5),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(5),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(5),

            "MARKET": "pure_factors_MA.MARKET.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
            "CHEM": "pure_factors_MA.CHEM.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
            "MISC": "pure_factors_MA.MISC.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
        },
        "20221201": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(5),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(5),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(5),
            "RSW252HL063": "pure_factors_VANILLA.RSW252HL063.TW{:03d}".format(5),

            "MARKET": "pure_factors_MA.MARKET.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
            "CHEM": "pure_factors_MA.CHEM.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
            "MISC": "pure_factors_MA.MISC.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
        },
        "20170101": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(5),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(5),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(5),
            "SKEW010": "pure_factors_VANILLA.SKEW010.TW{:03d}".format(5),
            "RSW252HL063": "pure_factors_VANILLA.RSW252HL063.TW{:03d}".format(5),

            "MARKET": "pure_factors_MA.MARKET.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
            "CHEM": "pure_factors_MA.CHEM.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
            "MISC": "pure_factors_MA.MISC.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
        },
        "20120101": {
            "BASIS147": "pure_factors_VANILLA.BASIS147.TW{:03d}".format(5),
            "CTP063": "pure_factors_VANILLA.CTP063.TW{:03d}".format(5),
            "CSP189": "pure_factors_VANILLA.CSP189.TW{:03d}".format(5),

            "MARKET": "pure_factors_MA.MARKET.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
            "CHEM": "pure_factors_MA.CHEM.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
            "MISC": "pure_factors_MA.MISC.TW{:03d}.FAST{:03d}.SLOW{:03d}".format(5, 5, 126),
        },
    },
}

synth_options = {
    "R1": {
        "RSW252HL063": {"weight": 1 / 6, "SHP": 0.3},
        "BASIS147": {"weight": 1 / 6, "SHP": 0.3},
        "CTP063": {"weight": 1 / 6, "SHP": 0.3},
        "CVP063": {"weight": 1 / 6, "SHP": 0.3},
        "TS126": {"weight": 1 / 6, "SHP": 0.3},
        "MTM231": {"weight": 1 / 6, "SHP": 0.3},
    },

    "R4": {
        "RSW252HL063": {"weight": 1 / 8, "SHP": 0.3},
        "BASIS147": {"weight": 1 / 8, "SHP": 0.3},
        "CTP063": {"weight": 1 / 8, "SHP": 0.3},
        "CVP063": {"weight": 1 / 8, "SHP": 0.3},
        "TS126": {"weight": 1 / 8, "SHP": 0.3},
        "MTM231": {"weight": 1 / 8, "SHP": 0.3},
        "SKEW010": {"weight": 1 / 8, "SHP": 0.3},
        "BETA021": {"weight": 1 / 8, "SHP": 0.3},
    },
}

if __name__ == "__main__":
    import pandas as pd

    print("Total number of factors = {}".format(len(factors)))  # 103
    print("\n".join(factors))
    print(selected_sectors_list)
    print(selected_factors_list)
    print(available_factors_list)
    print("Sectors N:{:>2d}".format(len(selected_sectors_list)))
    print("Factors N:{:>2d}".format(len(selected_factors_list)))
    print("ALL     N:{:>2d}".format(len(available_factors_list)))

    comp_struct = {}
    for k, v in allocation_options.items():
        comp_struct[k] = {z: 1 for z in v}
    comp_df = pd.DataFrame(comp_struct)
    print(comp_df)
