from setup_factor_and_portfolio import sys
from config_factor import test_windows, factors_pool_options, factors_return_lags
from factors.XFuns import fun_for_normalize_delinear
from factors.XFuns import fun_for_factors_return
import subprocess as sp

trade_date, next_date = sys.argv[1], sys.argv[2]  # format = "YYYYMMDD"
sep = "-" * 120 + "\n"

sp.run(["python", "instrument_return.py"])
print(sep)

sp.run(["python", "available_universe.py", "--mode", "a", "--bgn", trade_date])
print(sep)

sp.run(["python", "market_return.py"])
print(sep)

sp.run(["python", "test_return.py", "--mode", "a", "--bgn", trade_date])
print(sep)

sp.run(["python", "test_return_neutral.py", "--mode", "a", "--bgn", trade_date])
print(sep)

sp.run(["python", "03_cal_factors.py", next_date])
print(sep)

sp.run(["python", "03_cal_factors_neutral.py", "--mode", "a", "--bgn", trade_date])
print(sep)

# The following parts may depend on IC-test results:
# From IC-tests, we may decide which factors are added
# to the pool, which are not.

fun_for_normalize_delinear(t_pid_list=list(factors_pool_options.keys()),
                           t_run_mode="a", t_bgn_date=trade_date, t_stp_date=next_date)
print(sep)

fun_for_factors_return(
    t_pid_list=list(factors_pool_options.keys()),
    t_test_window_list=test_windows,
    t_factors_return_lag_list=factors_return_lags,
    t_run_mode="a", t_bgn_date=trade_date, t_stp_date=next_date
)
print(sep)

# --- signals
for test_window in test_windows:
    sp.run(["python", "10_reformat_factors_return.py", str(test_window)])
print(sep)

for test_window in test_windows:
    sp.run(["python", "12_pure_factors_signals_VANILLA.py", "--testWin", str(test_window),
            "--mode", "a", "--bgn", trade_date, "--stp", next_date])
print(sep)

for test_window in test_windows:
    sp.run(["python", "12_pure_factors_signals_MA.py", "--testWin", str(test_window),
            "--mode", "a", "--bgn", trade_date, "--stp", next_date])
print(sep)

sp.run(["python", "15_A_raw_factors_simple_synth.py",
        "--mode", "a", "--bgn", trade_date, "--stp", next_date])
print(sep)

sp.run(["python", "15_B_allocation_pure_factors.py",
        "--mode", "a", "--bgn", trade_date, "--stp", next_date])
print(sep)

sp.run(["python", "16_signals_mov_ave_opt_VANILLA.py",
        "--mode", "a", "--bgn", trade_date, "--stp", next_date])
sp.run(["python", "16_signals_mov_ave_opt_MA.py",
        "--mode", "a", "--bgn", trade_date, "--stp", next_date])
sp.run(["python", "16_signals_mov_ave_opt.py",
        "--mode", "a", "--bgn", trade_date, "--stp", next_date])
print(sep)
