import os
import pandas as pd
from skyrim.riften import CNAV
from skyrim.winterhold import plot_lines
from skyrim.whiterun import df_to_md_files


def evaluation_single_factor_by_year(factor_lbl: str, hold_period_n: int,
                                     risk_free_rate: float,
                                     evaluations_allocation_dir: str, by_year_dir: str):
    pd.set_option("display.width", 0)
    comb_id = "{}.HPN{:03d}".format(factor_lbl, hold_period_n)

    # core settings
    index_cols = "年"
    latex_cols = ["天数", "持有期收益", "年化收益", "夏普比率", "最大回撤", "最大回撤时点", "最长回撤期", "最长恢复期", "卡玛比率"]
    md_cols = ["天数", "持有期收益", "年化收益", "夏普比率", "最大回撤", "最大回撤时点", "卡玛比率"]

    # load nav file
    nav_file = "nav.{}.csv.gz".format(comb_id)
    nav_path = os.path.join(evaluations_allocation_dir, "by_comb_id", nav_file)
    nav_df = pd.read_csv(nav_path, dtype={"trade_date": str}).set_index("trade_date")
    nav_df["trade_year"] = nav_df.index.map(lambda z: z[0:4])
    # print(nav_df.tail(20))

    # by year
    by_year_nav_summary_data = []
    for trade_year, trade_year_df in nav_df.groupby(by="trade_year"):
        # get nav summary
        p_nav = CNAV(t_raw_nav_srs=trade_year_df["AVER"], t_annual_rf_rate=risk_free_rate)
        p_nav.cal_all_indicators(t_method="compound")
        d = p_nav.to_dict(t_type="chs")
        d.update({
            "年": trade_year,
            "天数": len(trade_year_df),
        })
        by_year_nav_summary_data.append(d)

        plot_lines(
            t_plot_df=trade_year_df[["AVER"]] / trade_year_df["AVER"].iloc[0],
            t_vlines_index=None,
            t_fig_name="nav.{}.Y{}".format(comb_id, trade_year),
            t_save_dir=by_year_dir
        )

    aver_nav_summary_df = pd.DataFrame(by_year_nav_summary_data).sort_values(by=index_cols, ascending=True).set_index(index_cols)
    aver_nav_summary_file = "summary.{}.by_year.csv".format(comb_id)
    aver_nav_summary_path = os.path.join(by_year_dir, aver_nav_summary_file)
    aver_nav_summary_df.to_csv(aver_nav_summary_path, float_format="%.2f")
    aver_nav_summary_df[latex_cols].to_csv(aver_nav_summary_path.replace(".csv", ".latex.csv"), float_format="%.2f")
    df_to_md_files(aver_nav_summary_df[md_cols].reset_index(), aver_nav_summary_path.replace(".csv", ".md"))
    print("=" * 120)
    print("AVER NAV SUMMARY BY YEAR", factor_lbl, hold_period_n)
    print("-" * 120)
    print(aver_nav_summary_df)
    print("-" * 120 + "\n")
    return 0
