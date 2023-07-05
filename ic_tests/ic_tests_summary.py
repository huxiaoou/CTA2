import os
import pandas as pd


def ic_test_summary(factors_list, neutral_method: str, exception_list: list, test_ic_dir: str):
    pd.set_option("display.float_format", "{:.4f}".format)
    pd.set_option("display.width", 0)
    pd.set_option("display.max_rows", 1000)

    summary_dfs_list = []
    for factor_lbl in factors_list:
        if factor_lbl in exception_list:
            continue

        statistics_file = "statistics.{}.csv".format(factor_lbl)
        statistics_path = os.path.join(test_ic_dir, factor_lbl, statistics_file)
        statistics_df = pd.read_csv(statistics_path)
        statistics_df = statistics_df[["factor", "testWindow", "IC-Mean", "IC-Std", "ICIR"]]

        statistics_neutral_file = "statistics.{}.{}.csv".format(factor_lbl, neutral_method)
        statistics_neutral_path = os.path.join(test_ic_dir, factor_lbl, statistics_neutral_file)
        statistics_neutral_df = pd.read_csv(statistics_neutral_path)
        statistics_neutral_df = statistics_neutral_df[["factor", "testWindow", "IC-Mean", "IC-Std", "ICIR"]]

        summary_df = pd.merge(
            left=statistics_df, right=statistics_neutral_df,
            on=["factor", "testWindow"],
            how="outer", suffixes=("", "(SEC-NEU)")
        )

        summary_dfs_list.append(summary_df)

    tot_summary_df = pd.concat(summary_dfs_list, ignore_index=True, axis=0)
    print(tot_summary_df)

    for test_window, test_window_df in tot_summary_df.groupby(by="testWindow"):
        ic_order_df = test_window_df.sort_values(by="IC-Mean", ascending=False).head(12)
        ic_order_neutral_df = test_window_df.sort_values(by="IC-Mean(SEC-NEU)", ascending=False).head(12)
        print("=" * 120)
        print("test window = {}".format(test_window))
        print("-" * 120)
        print(ic_order_df)
        print("-" * 120)
        print(ic_order_neutral_df)

        ic_order_file = "ic_order.{}.TW{:03d}.csv".format(neutral_method, test_window)
        ic_order_path = os.path.join(test_ic_dir, ic_order_file)
        ic_order_df.to_csv(ic_order_path, index=False, float_format="%.3f")

        ic_order_neutral_file = "ic_order_neutral.{}.TW{:03d}.csv".format(neutral_method, test_window)
        ic_order_neutral_path = os.path.join(test_ic_dir, ic_order_neutral_file)
        ic_order_neutral_df.to_csv(ic_order_neutral_path, index=False, float_format="%.3f")
