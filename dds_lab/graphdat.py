from bokeh.plotting import show, figure
from bokeh.models import HoverTool, ColumnDataSource, Circle, Text
from collections import OrderedDict
import numpy as np


def find_height(node_key, adjencency_list):
    """
    Finds height of adjencency_list representation
    of tree. Uncertain about complexity... thinking O(nodes)
    atm. Not that it matters since there wont be massive
    trees.
    """
    if node_key not in adjencency_list:
        return 0
    else:
        # So much for avoiding nasty recursion
        return max([(find_height(x, adjencency_list) + 1)
                    for x in adjencency_list[node_key]])


def find_root(adjencency_list):
    """
    O(number_of_nodes * T_{find_height}(number_of_nodes))
    """
    nodes = []
    heights = []
    for node_key in adjencency_list:
        nodes.append(node_key)
        heights.append(find_height(node_key, adjencency_list))
    return nodes[np.argmax(heights)]


def level_dict(adj_list, curr_elems, order=0):
    """
    Turns an adjencency_list list for a binary tree
    and its given root in to a dict of levels
    """
    if not curr_elems:
        return {}
    d = OrderedDict()
    new_elems = []
    for elem, parent in curr_elems:
        d.setdefault(order, []).append((elem, parent))
        to_add = list(adj_list.get(elem, []))
        new_elems.extend(zip(to_add, [elem]*len(to_add)))

    d.update(level_dict(adj_list,
                        new_elems,
                        order=order + 1)
            )
    return d


def get_tree_plot(adjencency_list, names, info, title):
    """
    BFS-traversal (level order) and plot of tree.
    """
    if not adjencency_list:
        print("Please provide an adjencency_list along with data")
        fig_null = figure(title=title)
        # To suppress no glyph bug message:
        fig_null.line(x=[0,1],y=[0,1], line_color="white")

        # Keep the same format TODO: abstract
        fig_null.xgrid.grid_line_color = None
        fig_null.ygrid.grid_line_color = None
        fig_null.axis.major_label_text_font_size = "0pt"
        fig_null.axis.major_tick_line_color = None
        fig_null.axis[0].ticker.num_minor_ticks = 0
        fig_null.axis[1].ticker.num_minor_ticks = 0
        fig_null.outline_line_color = "white"
        fig_null.xaxis.axis_line_color = "white"
        fig_null.yaxis.axis_line_color = "white"
        return fig_null, adjencency_list
    x = []
    y = []

    root = find_root(adjencency_list)
    # print adjencency_list
    # This is level numebers counting from one
    # so not actually height
    height = find_height(root, adjencency_list) + 1
    o = level_dict(adjencency_list, [(root, None)])

    x = []
    y = []
    x.append(0)
    y.append(0)
    initial_x_manhatan = -(height - 1)
    const = initial_x_manhatan
    level_dist = initial_x_manhatan
    level = 0
    # Keeping track of parents
    dist_dict = {}
    linesx = []
    linesy = []

    fig = figure(
        title=title,
        tools="box_select,resize,reset"  # Note no hover
    )

    textsx = []
    textsy = []
    texts = []

    textsx.append(0 - 0.18)
    textsy.append(0-0.07)
    texts.append(root)
    for lev in o.keys():
        number_of_nodes = len(o[lev])
        left_right = [level_dist, -level_dist] * number_of_nodes
        side_index = 0
        for level_memeber, parent in o[lev]:
            if lev == 1:
                x.append(initial_x_manhatan)
                y.append(level)
                dist_dict[level_memeber] = float(initial_x_manhatan)
                textsx.append(dist_dict[level_memeber] - 0.18)
                textsy.append(level - 0.07)
                texts.append(level_memeber)
                fig.line([dist_dict[level_memeber], 0],
                         [level, level + 1])
                initial_x_manhatan += 2*abs(const) / (number_of_nodes - 1)
            elif lev !=0:
                side_factor = left_right[side_index]
                xdist = dist_dict[parent] + side_factor
                dist_dict[level_memeber] = float(xdist)
                x.append(xdist)
                y.append(level)
                textsx.append(dist_dict[level_memeber] - 0.18)
                textsy.append(level - 0.07)
                texts.append(level_memeber)
                fig.line([dist_dict[level_memeber], dist_dict[parent]],
                         [level, level + 1])
                side_index += 1
        level -= 1
        level_dist /= 1.5

    
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.axis.major_label_text_font_size = "0pt"
    fig.axis.major_tick_line_color = None
    fig.axis[0].ticker.num_minor_ticks = 0
    fig.axis[1].ticker.num_minor_ticks = 0
    fig.outline_line_color = "white"
    fig.xaxis.axis_line_color = "white"
    fig.yaxis.axis_line_color = "white"


    source = ColumnDataSource(
        data=dict(
            xname=x,
            yname=y,
            names=names,
            info=info
        )
    )
    circle = Circle(x="xname",
                    y="yname",
                    radius=0.3,
                    fill_color="#e9f1f8")
    circle_renderer = fig.add_glyph(source, circle)
    tooltips = OrderedDict([
        ("name", "@names"),
        ("info", "@info"),
    ])
    fig.add_tools(HoverTool(tooltips=tooltips, renderers=[circle_renderer]))
    fig.text(x=textsx,y=textsy,text=texts)

    return fig, adjencency_list


def adjecency_list_exercise():
    names = ["Sentence",
             "Noun phrase",
             "Verb phrase",
             "Verb",
             "Noun phrase",
             "Delimiter",
             "Noun"]
    info = ["John hit the ball",
            "John",
            "hit the ball",
            "hit",
            "the ball",
            "the",
            "ball"]
    # the adjecency list is more or less exactly the same as our table without the information collumn:
    adjecency_list = {"S": ["NP", "VP"],
                      "VP": ["V", "NP`"],
                      "NP`": ["D", "N"]}
    #Generate tree plot
    fig, ad_list = get_tree_plot(adjecency_list,
                                names=names,
                                info=info,
                                title="Parse Tree")
    return fig