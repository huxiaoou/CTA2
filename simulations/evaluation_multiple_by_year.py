import os
import pandas as pd
from skyrim.winterhold import plot_lines


def evaluation_multiple_by_year_plot_nav(output_id: str, alloc_id_hpn_options: list, evaluations_allocation_dir: str, by_year_dir: str):
    pd.set_option("display.width", 0)

    multiple_nav_data = {}
    for allocation_id, hold_period_n in alloc_id_hpn_options:
        comb_id = "{}.HPN{:03d}".format(allocation_id, hold_period_n)
        nav_file = "nav.{}.csv.gz".format(comb_id)
        nav_path = os.path.join(evaluations_allocation_dir, "by_comb_id", nav_file)
        nav_df = pd.read_csv(nav_path, dtype={"trade_date": str}).set_index("trade_date")
        multiple_nav_data[comb_id] = nav_df["AVER"]

    multiple_nav_df = pd.DataFrame(multiple_nav_data)
    norm_plot_df = multiple_nav_df / multiple_nav_df.iloc[0]
    plot_lines(
        t_plot_df=norm_plot_df,
        t_fig_name="nav.{}".format(output_id),
        t_colormap="jet",
        t_save_dir=by_year_dir
    )

    multiple_nav_df["trade_year"] = multiple_nav_df.index.map(lambda z: z[0:4])

    for trade_year, trade_year_df in multiple_nav_df.groupby(by="trade_year"):
        plot_df = trade_year_df.drop(labels="trade_year", axis=1)
        norm_plot_df = plot_df / plot_df.iloc[0]
        plot_lines(
            t_plot_df=norm_plot_df,
            # t_vlines_index=["20221014"] if trade_year == "2022" else None,
            t_fig_name="nav.{}.Y{}".format(output_id, trade_year),
            t_colormap="jet",
            t_save_dir=by_year_dir
        )
        print("... multiple nav of {:>24s} of year {} plot".format(output_id, trade_year))
