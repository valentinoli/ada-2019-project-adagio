# -*- coding: utf-8 -*-
"""Plotting functions"""

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, Legend
from bokeh.plotting import figure
from bokeh.transform import dodge

HTML_DIR = "../docs/_includes/"

def plot_consumption_per_type(data):
    source = ColumnDataSource(data=data)
    # output_file(HTML_DIR + "consumption_per_type.html")

    title = "Swiss Domestic vs. Imported Consumption"
    p = figure(x_range=data.index.tolist(), y_range=(0, 100), plot_height=250, plot_width=700,
               title=title, toolbar_location=None, y_axis_label="ratio (%)")

    r1 = p.vbar(x=dodge("type", -0.125, range=p.x_range), top="domestic_consumption", 
                width=0.2, source=source, color="#b7eebc")

    r2 = p.vbar(x=dodge("type",  0.125, range=p.x_range), top="imported_consumption",
                width=0.2, source=source, color="#ca041e")

    legend_items = [
        ("domestic consumption", [r1]),
        ("imported consumption", [r2]),
    ]

    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None

    legend = Legend(items=legend_items, location=(5, 0))
    legend.click_policy="mute"
    p.add_layout(legend, 'right')

    show(p)
