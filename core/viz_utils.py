from math import pi

import pandas as pd

from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
import streamlit as st


def draw_pie(male_count, female_count):
    x = {"Male": male_count, "Female": female_count}

    data = pd.Series(x).reset_index(name="value").rename(columns={"index": "gender"})
    data["angle"] = data["value"] / data["value"].sum() * 2 * pi

    data["color"] = ["#3182bd", "#6baed6"]

    p = figure(
        height=350,
        title="Get count addressbook by gender",
        toolbar_location=None,
        tools="hover",
        tooltips="@gender: @value",
        x_range=(-0.5, 1.0),
    )

    p.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field="gender",
        source=data,
    )

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    st.bokeh_chart(p)


if __name__ == "__main__":

    male_count, female_count = 30, 60
    draw_pie(male_count, female_count)
