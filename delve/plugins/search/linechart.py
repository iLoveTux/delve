from argparse import ArgumentParser
import logging

import pandas as pd
import streamlit as st
# import matplotlib.pyplot as plt
import altair as alt



parser = ArgumentParser()
parser.add_argument("-x", "--x-field")
parser.add_argument("-y", "--y-field")
parser.add_argument("-d", "--detail")
def linechart(argv: list[str], results: pd.DataFrame):
    log = logging.getLogger(__name__)
    args = parser.parse_args(argv)
    log.debug(f"Found args: {args}")

    chart = alt.Chart(results)
    if args.x_field:
        if args.y_field:
            if args.detail:
                chart = chart.mark_line().encode(
                    x=args.x_field,
                    y=args.y_field,
                    detail=args.detail,
                )
            else:
                chart = chart.mark_line().encode(
                    x=args.x_field,
                    y=args.y_field,
                )
        else:
            chart = chart.mark_line().encode(
                x=args.x_field,
            )
    else:
            chart = chart.mark_line().encode(
                x=args.x_field,
            )

    return chart
    # fig, ax = plt.subplots()
    # log.debug(f"Found fig: {fig}, ax: {ax}")
    # st.write(results)
    # ax.plot(results.loc[:,args.x_field].astype(str), results.loc[:,args.y_fields].astype(int))
    # log.debug(f"Found ax:  {ax}")
    # return fig
