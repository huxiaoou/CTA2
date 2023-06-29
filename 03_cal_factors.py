from setup_factor_and_portfolio import sys
from setup_factor_and_portfolio import factors_exposure_dir
from setup_factor_and_portfolio import instruments_return_dir, major_minor_dir, major_return_dir, fundamental_by_instru_dir, md_by_instru_dir
from factors.factors_algorithm_BASIS import factors_algorithm_BASIS
from factors.factors_algorithm_BETA import factors_algorithm_BETA
from factors.factors_algorithm_CSP import factors_algorithm_CSP
from factors.factors_algorithm_CSR import factors_algorithm_CSR
from factors.factors_algorithm_CTP import factors_algorithm_CTP
from factors.factors_algorithm_CTR import factors_algorithm_CTR
from factors.factors_algorithm_CV import factors_algorithm_CV
from factors.factors_algorithm_CVP import factors_algorithm_CVP
from factors.factors_algorithm_CVR import factors_algorithm_CVR
from factors.factors_algorithm_HP import factors_algorithm_HP
from factors.factors_algorithm_MTM import factors_algorithm_MTM
from factors.factors_algorithm_RSW import factors_algorithm_RSW
from factors.factors_algorithm_SGM import factors_algorithm_SGM
from factors.factors_algorithm_SIZE import factors_algorithm_SIZE
from factors.factors_algorithm_SKEW import factors_algorithm_SKEW
from factors.factors_algorithm_TO import factors_algorithm_TO
from factors.factors_algorithm_TS import factors_algorithm_TS
from factors.factors_algorithm_VOL import factors_algorithm_VOL
from config_factor import concerned_instruments_universe, md_bgn_date
from config_factor import factors_args
from struct_lib import database_structure

md_stp_date = sys.argv[1]  # format = "YYYYMMDD"

switch = {
    "BASIS": True,
    "BETA": True,
    "CSP": True,
    "CSR": False,
    "CTP": True,
    "CTR": False,
    "CV": False,
    "CVP": True,
    "CVR": False,
    "HP": False,
    "MTM": True,
    "RSW": True,
    "SGM": False,
    "SIZE": True,
    "SKEW": True,
    "TO": True,
    "TS": True,
    "VOL": False,
}

if switch["BASIS"]:
    for basis_window in factors_args["BASIS"]:
        factors_algorithm_BASIS(
            basis_window=basis_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            bgn_date=md_bgn_date,
            stp_date=md_stp_date,
            fundamental_dir=fundamental_by_instru_dir,
            major_minor_dir=major_minor_dir
        )

if switch["BETA"]:
    for beta_window in factors_args["BETA"]:
        factors_algorithm_BETA(
            beta_window=beta_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            instruments_return_dir=instruments_return_dir,
            major_return_dir=major_return_dir,
        )

if switch["CSP"]:
    for csp_window in factors_args["CSP"]:
        factors_algorithm_CSP(
            csp_window=csp_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir
        )

if switch["CSR"]:
    for csr_window in factors_args["CSR"]:
        factors_algorithm_CSR(
            csr_window=csr_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir
        )

if switch["CTP"]:
    for ctp_window in factors_args["CTP"]:
        factors_algorithm_CTP(
            ctp_window=ctp_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir
        )

if switch["CTR"]:
    for ctr_window in factors_args["CTR"]:
        factors_algorithm_CTR(
            ctr_window=ctr_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir
        )

if switch["CV"]:
    for cv_window in factors_args["CV"]:
        factors_algorithm_CV(
            cv_window=cv_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir
        )

if switch["CVP"]:
    for cvp_window in factors_args["CVP"]:
        factors_algorithm_CVP(
            cvp_window=cvp_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir,
        )

if switch["CVR"]:
    for cvr_window in factors_args["CVR"]:
        factors_algorithm_CVR(
            cvr_window=cvr_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir,
        )

if switch["HP"]:
    for hp_window in factors_args["HP"]:
        factors_algorithm_HP(
            hp_window=hp_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir
        )

if switch["MTM"]:
    for mtm_window in factors_args["MTM"]:
        factors_algorithm_MTM(
            mtm_window=mtm_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir,
        )

if switch["RSW"]:
    for half_life in factors_args["RSW252HL"]:
        factors_algorithm_RSW(
            rs_window=252, half_life=half_life,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            fundamental_dir=fundamental_by_instru_dir,
            major_minor_dir=major_minor_dir,
        )

if switch["SGM"]:
    for sgm_window in factors_args["SGM"]:
        factors_algorithm_SGM(
            sgm_window=sgm_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir,
        )

if switch["SIZE"]:
    for size_window in factors_args["SIZE"]:
        factors_algorithm_SIZE(
            size_window=size_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir,
        )

if switch["SKEW"]:
    for skew_window in factors_args["SKEW"]:
        factors_algorithm_SKEW(
            skew_window=skew_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir,
        )

if switch["TO"]:
    for to_window in factors_args["TO"]:
        factors_algorithm_TO(
            to_window=to_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir,
        )

if switch["TS"]:
    for ts_window in factors_args["TS"]:
        factors_algorithm_TS(
            ts_window=ts_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_minor_dir=major_minor_dir,
            md_dir=md_by_instru_dir,
        )

if switch["VOL"]:
    for vol_window in factors_args["VOL"]:
        factors_algorithm_VOL(
            vol_window=vol_window,
            concerned_instruments_universe=concerned_instruments_universe,
            database_structure=database_structure,
            factors_exposure_dir=factors_exposure_dir,
            md_bgn_date=md_bgn_date,
            md_stp_date=md_stp_date,
            major_return_dir=major_return_dir,
        )
