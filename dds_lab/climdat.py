import numpy as np
import scipy as s
from bokeh.browserlib import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Circle, Text
from bokeh.models import (
    BasicTicker, ColumnDataSource, Grid, GridPlot, LinearAxis,
    DataRange1d, PanTool, Plot, WheelZoomTool, HoverTool, Line
)
from bokeh.charts import TimeSeries, HeatMap
from bokeh.palettes import YlOrRd9 as palette
from bokeh.plotting_helpers import _update_legend
from bokeh.resources import INLINE
from bokeh.sampledata.iris import flowers
from bokeh.plotting import *
from bokeh.io import gridplot, output_file, show, vplot
import re
from os import listdir
from os.path import isfile, join
from itertools import product
from collections import OrderedDict
from scipy.ndimage.filters import convolve1d
from dds_lab.datasets import climate
import pandas as pd


def read_tags(path):
    """
    This function takes in a unix path of type String and
    returns a list of html tags each of type String
    """
    txts = [f for f in listdir(path) if(isfile(join(path, f)) and 'txt' in f)]
    html_tags = {}
    for x in txts:
        html_tags[x] = list(set(open(path + x, 'r').read().split(">,<")))
        # ^ tags contain duplicates due to the process
        # they were retrieved in thus we use set to remove them
    return html_tags


# Regex for values + filtering over the data set
# Year, value parsing functions to parse an individual tag
# i.e.:
# <span style="max-width: 962px; max-height: 992px;">Year: 1961<br>Value: 1011.88<br>Series: City of Edinburgh<br></span>
year = lambda x: (int(re.search(r'(?<=Year:\s)(\d+)', x).group(0))
                  if re.search(r'(?<=Year:\s)(\d+)', x) else None)

val = lambda x: (float(re.search(r'(?<=Value:\s)\d+\.?\d*', x).group(0))
                 if re.search(r'(?<=Value:\s)\d+\.?\d*', x) else None)

# Function that combines the previous two and applys them to a list in order to yield (year, value)
# pairs.
extract = lambda y: dict(zip(filter(lambda x: x is not None,
                                    map(year, y)),
                             (filter(lambda x: x is not None,
                                     map(val, y)))))


def parse_time_series(html_tags_files, txt):
    """
    This function parses individual timeseries data in to
    a dictionary which contains the year as keys
    """
    prod_dict = {}
    t_dict = OrderedDict()
    for p in txt:
        prod_dict[str(p)] = extract(html_tags_files[str(p)])
    return prod_dict


def pair_data(html_tags1, html_tags2, order, split_by=2010):

    # obtain years and values for every tag in both data sets and place them in
    # dictionary data structure since this is probably one ofthe most efficient
    # ways to pair them on later on
    first_pair = extract(html_tags1)
    second_pair = extract(html_tags2)

    first_y = []
    second_y = []

    order = list(order)
    # Determine which pair is larger and pair up relative to
    # that pair in order to not miss tags
    if(len(second_pair) < len(first_pair)):
        tmp = dict(second_pair)
        tmp_name = order[0]
        second_pair = dict(first_pair)
        first_pair = dict(tmp)
        order[0] = order[1]
        order[1] = tmp_name
        del tmp

    # Pairing up process taking advantage of the dictionary data structure
    for k, v in second_pair.items():
        if k in first_pair:
            first_y.append((k, first_pair[k]))
            second_y.append((k, v))

    # Make sure to sort by one axis
    final = list(zip(first_y, second_y))
    final.sort(key=lambda x: x[0][1])

    # Split set by  3 year ranges (interesting thought)
    if split_by:
        first_third = []
        second_third = []
        third_third = []
        for x in final:
            # Playing with splits
            if(x[0][0] >= split_by):
                first_third.append(x)
            # TODO: Make it a param and not a hardcoded val.
            elif(x[0][0] >= 1980):
                second_third.append(x)
            else:
                third_third.append(x)

        # Maybe change return to dict format to increase readability.
        return (np.array(first_third)[:, 0],
                np.array(first_third)[:, 1],
                np.array(second_third)[:, 0],
                np.array(second_third)[:, 1],
                np.array(third_third)[:, 0],
                np.array(third_third)[:, 1],
                first_pair,
                second_pair,
                order)

    # Raw return (no ranges)
    return (np.array(final)[:, 0],
            np.array(final)[:, 1],
            first_pair,
            second_pair,
            order)


class ClimPlots:

    """
    Container class for the SEPA climate variable data set
    and the 
    """

    def __init__(self, txt, path=climate):
        self.txt = txt
        self.path = path
        self.prod_dict = OrderedDict()
        self.html_tags = read_tags(self.path)
        self.uniform_mask = np.ones(6) / 6.0
        self.radius = len(self.uniform_mask)

    @staticmethod
    def make_pairs(html_tags):
        """
        This helper method pairs up the different climate
        variables so that they can be passed to the scatter plot matrix
        """
        for p in product(self.txts, repeat=2):
            self.prod_dict[str(p)] = pair_data(html_tags[p[0]],
                                               html_tags[p[1]],
                                               p,
                                               1995)

    def causal_avg_filter(self, data):
        """
        Causal moving average filter. Causes a low pass filter
        on the underlying frequency
        """
        # Non causal moving average.
        non_causal = convolve1d(data,
                                self.uniform_mask)
        # shift impulse response for causality
        causal = (non_causal[int(self.radius/2):len(non_causal) - int(self.radius/2.0) - 1]
                  if self.radius % 2 == 1
                  else non_causal[(self.radius/2):len(non_causal) - (self.radius/2.0)])
        return causal

    def plot_pairs(self):
        """
        Creates a scatter plot matrix for the specified data
        """

        html_tags = self.html_tags
        prod_dict = OrderedDict()

        txts = self.txt

        for p in product(txts, repeat=2):
            prod_dict[str(p)] = pair_data(html_tags[p[0]],
                                          html_tags[p[1]],
                                          p,
                                          1995)

        n = len(prod_dict)
        k2 = len(txts)

        fig_dict = OrderedDict()
        cds_dict = OrderedDict()

        for k, v in prod_dict.items():

            v[-1][0] = v[-1][0].replace(".txt", "").replace("_", " ")
            v[-1][1] = v[-1][1].replace(".txt", "").replace("_", " ")
            fig_dict[k] = figure(width=260, plot_height=260, title=str(v[-1][0]) + " vs "+str(v[-1][1]),
                                 title_text_font_size='8pt',
                                 tools="reset,hover",
                                 x_axis_label=v[-1][0],
                                 y_axis_label=v[-1][1])

            fig_dict[k].xaxis.axis_label_text_font_size = '8pt'
            fig_dict[k].yaxis.axis_label_text_font_size = '8pt'

            # Data sources are required for all 3 colors
            # in order to display labels and dynamically
            # update with notebook widgets
            cds_dict[k+'1'] = ColumnDataSource(
                data=dict(
                    x=np.array(v[0])[:, 1],
                    y=np.array(v[1])[:, 1],
                    desc=np.array(v[1])[:, 0]
                )
            )
            cds_dict[k+'2'] = ColumnDataSource(
                data=dict(
                    x=np.array(v[2])[:, 1],
                    y=np.array(v[3])[:, 1],
                    desc2=np.array(v[3])[:, 0]
                )
            )
            cds_dict[k+'3'] = ColumnDataSource(
                data=dict(
                    x=np.array(v[4])[:, 1],
                    y=np.array(v[5])[:, 1],
                    desc=np.array(v[5])[:, 0]
                )
            )

            # All 3 plots
            hover = HoverTool()
            s1 = fig_dict[k].scatter(np.array(v[0])[:, 1], np.array(v[1])[:, 1],
                                     fill_color='red', size=13, source=cds_dict[k + '1'])
            s1.select(dict(type=HoverTool)).tooltips = {
                "x": "$x", "y": "$y", "year": "@desc"}
            s2 = fig_dict[k].scatter(np.array(v[2])[:, 1], np.array(v[3])[:, 1],
                                     fill_color='green', size=10, source=cds_dict[k + '2'])
            s2.select(dict(type=HoverTool)).tooltips = {
                "x": "$x", "y": "$y", "year": "@desc"}
            s3 = fig_dict[k].scatter(np.array(v[4])[:, 1], np.array(v[5])[:, 1],
                                     fill_color='blue', size=7, source=cds_dict[k+'3'])
            s1.select(dict(type=HoverTool)).tooltips = {
                "x": "$x", "y": "$y", "year": "@desc"}

        # List of figures
        f_vals = list(fig_dict.values())

        # Creates gird for k2 x k2 grid plot by default k2 should be 3
        g = gridplot([([None]*(k2 - 1 - round((i + 1) / k2)) + f_vals[i: i + 1
                                                                      + round((i + 1) / k2)][::-1])
                      for i in range(0, n, k2)][::-1])
        return g

    def plot_time_series(self, moving_avg=False):
        """
        Plots time series and moving average filter
        when moving_avg set to true
        """
        t_fig_dict = dict()

        # Parse individual time series
        n_dict = parse_time_series(self.html_tags, self.txt)

        series = list()

        cds_dict = dict()

        for k in list(sorted(n_dict.keys())):
            v = n_dict[k]
            # Creating fig inst in dict for plot k
            t_fig_dict[k] = figure(title=k.split(",")[-1][0:-1],    
                                   height=315)

            # Sort by x-axis(dates) in order to ensure a
            # sound plot
            tmp = list(v.items())
            tmp.sort()

            np.array(tmp)

            date = np.array(tmp)[:, 0]
            vals = np.array(tmp)[:, 1]

            tooltips = OrderedDict([
                ("time", "@x"),
                ("value", "@y"),
            ])
            cds_dict[k+'1'] = ColumnDataSource(
                data=dict(
                    x=date,
                    y=vals,
                )
            )
            if moving_avg:
                # Moving averaged filter data
                vals_a = self.causal_avg_filter(vals)
                date_a = date[self.radius:]

                cds_dict[k+'2'] = ColumnDataSource(
                    data=dict(
                        x=date_a,
                        y=vals_a,
                    )
                )
                # Plot moving averaged filtered data
                # k + " avg data"
                line_a = Line(x="x", y="y",
                              line_color='blue', line_width=6)
                circle_renderer = t_fig_dict[k].add_glyph(cds_dict[k+'2'], line_a)
                _update_legend(plot=t_fig_dict[k], legend_name=k + " avg data", glyph_renderer=circle_renderer)
                t_fig_dict[k].add_tools(HoverTool(tooltips=tooltips, renderers=[circle_renderer]))
            # Plot raw data
            line_r = Line(x="x", y="y",
                          line_color='red')
            circle_renderer2 = t_fig_dict[k].add_glyph(cds_dict[k+'1'], line_r)
            _update_legend(plot=t_fig_dict[k], legend_name=k + " raw data", glyph_renderer=circle_renderer2)
            t_fig_dict[k].add_tools(HoverTool(tooltips=tooltips, renderers=[circle_renderer2]))

        # Unpack the fig instances in dict plot as a vertical stack of
        # horizontal plots
        v = vplot(*list(t_fig_dict.values()))

        return v

    def plot_time_series_heatMap(self, moving_avg=False):
        """
        Plots time series Heat map or moving average filter
        when moving_avg set to true
        """

        # Parse individual time series
        n_dict = parse_time_series(self.html_tags, self.txt)

        k = list(n_dict.keys())[0]
        v = n_dict[k]

        # Sort by x-axis(dates) in order to ensure a
        # sound plot
        tmp = list(v.items())
        tmp.sort()

        np.array(tmp)

        date = np.array(tmp)[:, 0]
        vals = np.array(tmp)[:, 1]

        tooltips = OrderedDict([
            ("time", "@x"),
            ("value", "@y"),
        ])

        if moving_avg:
            # Moving averaged filter data
            vals_a = self.causal_avg_filter(vals)
            date_a =list(map(str,date[self.radius:]))
            # Plot moving averaged filtered data
            # k + " avg data"
            df = pd.DataFrame(
                    dict(
                        zip(date_a, vals_a)

                    ),
                    index=[k]
            )

            p = HeatMap(df, title='avg timeseries heat map',
                        width=900, height=315, palette=palette)
            return p 
        # Plot raw data
        date = list(map(str, date))
        df = pd.DataFrame(
                    dict(
                        zip(date, vals)

                    ),
                    index=[k]
        )

        p = HeatMap(df, title='raw timeseries heat map',
                    width=900, height=315, palette=palette)
        return p 


