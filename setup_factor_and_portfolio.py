"""
Created by huxo
Initialized @ 10:53, 2023/3/27
=========================================
This project is mainly about:
0.  calculate factors of futures
"""

import os
import sys
import json
import platform
import numpy as np
import pandas as pd
import datetime as dt
import itertools as ittl

# platform confirmation
this_platform = platform.system().upper()
if this_platform == "WINDOWS":
    with open("/Deploy/config.json", "r") as j:
        global_config = json.load(j)
elif this_platform == "LINUX":
    with open("/home/huxo/Deploy/config.json", "r") as j:
        global_config = json.load(j)
else:
    print("... this platform is {}.".format(this_platform))
    print("... it is not a recognized platform, please check again.")
    sys.exit()

deploy_dir = global_config["deploy_dir"][this_platform]
project_data_root_dir = os.path.join(deploy_dir, "Data")

# --- calendar
calendar_dir = os.path.join(project_data_root_dir, global_config["calendar"]["calendar_save_dir"])
calendar_path = os.path.join(calendar_dir, global_config["calendar"]["calendar_save_file"])

# --- futures data
futures_dir = os.path.join(project_data_root_dir, global_config["futures"]["futures_save_dir"])
futures_shared_info_path = os.path.join(futures_dir, global_config["futures"]["futures_shared_info_file"])
instrument_info_path = os.path.join(futures_dir, global_config["futures"]["futures_instrument_info_file"])

futures_md_dir = os.path.join(futures_dir, global_config["futures"]["md_dir"])
futures_md_structure_path = os.path.join(futures_md_dir, global_config["futures"]["md_structure_file"])
futures_md_db_name = global_config["futures"]["md_db_name"]

futures_fundamental_dir = os.path.join(futures_dir, global_config["futures"]["fundamental_dir"])
futures_fundamental_structure_path = os.path.join(futures_fundamental_dir, global_config["futures"]["fundamental_structure_file"])
futures_fundamental_db_name = global_config["futures"]["fundamental_db_name"]

futures_by_instrument_dir = os.path.join(futures_dir, global_config["futures"]["by_instrument_dir"])
major_minor_dir = os.path.join(futures_by_instrument_dir, global_config["futures"]["major_minor_dir"])
major_return_dir = os.path.join(futures_by_instrument_dir, global_config["futures"]["major_return_dir"])
instru_idx_dir = os.path.join(futures_by_instrument_dir, global_config["futures"]["instru_idx_dir"])
md_by_instru_dir = os.path.join(futures_by_instrument_dir, global_config["futures"]["md_by_instru_dir"])
fundamental_by_instru_dir = os.path.join(futures_by_instrument_dir, global_config["futures"]["fundamental_by_instru_dir"])

factors_library_dir = os.path.join(futures_dir, global_config["futures"]["signals_dir"])
instruments_return_dir = os.path.join(factors_library_dir, "instruments_return")
instruments_corr_dir = os.path.join(factors_library_dir, "instruments_corr")
available_universe_dir = os.path.join(factors_library_dir, "available_universe")
test_return_dir = os.path.join(factors_library_dir, "test_return")
test_return_neutral_dir = os.path.join(factors_library_dir, "test_return_neutral")
factors_exposure_dir = os.path.join(factors_library_dir, "factors_exposure")
factors_exposure_neutral_dir = os.path.join(factors_library_dir, "factors_exposure_neutral")
factors_exposure_corr_dir = os.path.join(factors_library_dir, "factors_exposure_corr")
test_ic_dir = os.path.join(factors_library_dir, "test_ic")
factors_exposure_norm_dir = os.path.join(factors_library_dir, "factors_exposure_norm")
factors_exposure_delinear_dir = os.path.join(factors_library_dir, "factors_exposure_delinear")
factors_portfolio_dir = os.path.join(factors_library_dir, "factors_portfolio")
factors_return_dir = os.path.join(factors_library_dir, "factors_return")
factors_return_agg_dir = os.path.join(factors_library_dir, "factors_return_agg")
instruments_residual_dir = os.path.join(factors_library_dir, "instruments_residual")
instruments_residual_agg_dir = os.path.join(factors_library_dir, "instruments_residual_agg")
factors_delinear_test_ic_dir = os.path.join(factors_library_dir, "factors_delinear_test_ic")

# portfolio
portfolio_dir = os.path.join(futures_dir, global_config["futures"]["signals_dir"])
factors_return_reformat_dir = os.path.join(portfolio_dir, "factors_return_reformat")
signals_dir = os.path.join(portfolio_dir, "signals")
signals_allocation_dir = os.path.join(portfolio_dir, "signals_allocation")
by_year_dir = os.path.join(portfolio_dir, "by_year_allocation")
misc_dir = os.path.join(portfolio_dir, "misc")
signals_opt_dir = os.path.join(portfolio_dir, "signals_opt")
simulations_opt_dir = os.path.join(portfolio_dir, "simulations_opt")
evaluations_opt_dir = os.path.join(portfolio_dir, "evaluations_opt")

# --- projects
projects_dir = os.path.join(deploy_dir, global_config["projects"]["projects_save_dir"])

if __name__ == "__main__":
    from skyrim.winterhold import check_and_mkdir

    check_and_mkdir(factors_library_dir)
    check_and_mkdir(instruments_return_dir)
    check_and_mkdir(instruments_corr_dir)
    check_and_mkdir(available_universe_dir)
    check_and_mkdir(test_return_dir)
    check_and_mkdir(test_return_neutral_dir)
    check_and_mkdir(factors_exposure_dir)
    check_and_mkdir(factors_exposure_neutral_dir)
    check_and_mkdir(factors_exposure_corr_dir)
    check_and_mkdir(test_ic_dir)
    check_and_mkdir(factors_exposure_norm_dir)
    check_and_mkdir(factors_exposure_delinear_dir)
    check_and_mkdir(factors_portfolio_dir)
    check_and_mkdir(factors_return_dir)
    check_and_mkdir(factors_return_agg_dir)
    check_and_mkdir(instruments_residual_dir)
    check_and_mkdir(instruments_residual_agg_dir)
    check_and_mkdir(factors_delinear_test_ic_dir)

    check_and_mkdir(portfolio_dir)
    check_and_mkdir(factors_return_reformat_dir)
    check_and_mkdir(signals_dir)
    check_and_mkdir(signals_allocation_dir)
    check_and_mkdir(signals_opt_dir)
    check_and_mkdir(simulations_opt_dir)
    check_and_mkdir(evaluations_opt_dir)
    check_and_mkdir(os.path.join(evaluations_opt_dir, "by_comb_id"))
    check_and_mkdir(by_year_dir)
    check_and_mkdir(misc_dir)

    print("... directory system for this project has been established.")