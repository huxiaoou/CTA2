import itertools as ittl
import multiprocessing as mp
from typing import List
from simulations.simulation import simulation_single_factor


def process_target_fun_for_simulation(t_group_id: int,
                                      t_gn: int, t_factors_list: list, t_test_window_list: list,
                                      calendar_path: str, instrument_info_path: str,
                                      md_by_instru_dir: str, major_minor_dir: str, available_universe_dir: str,
                                      sig_dir: str, dst_dir: str,
                                      database_structure: dict,
                                      test_universe: List[str], test_bgn_date: str, test_stp_date: str,
                                      cost_reservation: float, cost_rate: float, init_premium: float,
                                      skip_if_exist: bool = True
                                      ):
    for i, (factor, test_window) in enumerate(ittl.product(t_factors_list, t_test_window_list)):
        if i % t_gn == t_group_id:
            for start_delay in range(test_window):
                simulation_single_factor(
                    factor, test_window, start_delay,
                    calendar_path, instrument_info_path,
                    md_by_instru_dir, major_minor_dir, available_universe_dir,
                    sig_dir, dst_dir,
                    database_structure,
                    test_universe, test_bgn_date, test_stp_date,
                    cost_reservation, cost_rate, init_premium,
                    skip_if_exist
                )
    return 0


def fun_for_simulation_factors(t_gn: int, t_factors_list: list, t_test_window_list: list,
                               calendar_path: str, instrument_info_path: str,
                               md_by_instru_dir: str, major_minor_dir: str, available_universe_dir: str,
                               sig_dir: str, dst_dir: str,
                               database_structure: dict,
                               test_universe: List[str], test_bgn_date: str, test_stp_date: str,
                               cost_reservation: float, cost_rate: float, init_premium: float,
                               skip_if_exist: bool = True):
    to_join_list = []
    for group_id in range(t_gn):
        t = mp.Process(target=process_target_fun_for_simulation, args=(
            group_id,
            t_gn, t_factors_list, t_test_window_list,
            calendar_path, instrument_info_path,
            md_by_instru_dir, major_minor_dir, available_universe_dir,
            sig_dir, dst_dir,
            database_structure,
            test_universe, test_bgn_date, test_stp_date,
            cost_reservation, cost_rate, init_premium,
            skip_if_exist))
        t.start()
        to_join_list.append(t)
    for t in to_join_list:
        t.join()
    return 0
