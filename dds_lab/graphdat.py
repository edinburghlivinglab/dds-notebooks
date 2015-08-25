from bokeh.plotting import show, figure
from bokeh.models import HoverTool, ColumnDataSource, Circle
from collections import OrderedDict
import numpy as np
from queue import Queue


def test_binary_tree(adjencency_list):
    """
    Hardcoded bokeh 3 level completely balanced binary Tree
    Attempting to automate to n level trees in the function
    bellow. Hardcoded example need to automate.
    """
    fig = figure(
        title="DDS Help Tree",
        tools="box_zoom,box_select,resize,reset"  # Note no hover
    )
    names = ["Gavin Gray", "Ewan Klein",
             "Francisco Vargas", "S3", "S1", "S2", "S4"]
    info = ["TA", "Lectuer", "TA", "Student", "Student", "Student", "Student"]
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.axis.major_label_text_font_size = "0pt"
    fig.axis.major_tick_line_color = None
    fig.axis[0].ticker.num_minor_ticks = 0
    fig.axis[1].ticker.num_minor_ticks = 0
    fig.outline_line_color = "white"
    fig.xaxis.axis_line_color = "white"
    fig.yaxis.axis_line_color = "white"
    fig.line(x=[1, 3, 5], y=[1, 2, 1])
    fig.line(x=[0, 1, 2], y=[0, 1, 0])
    fig.line(x=[4, 5, 6], y=[0, 1, 0])

    source = ColumnDataSource(
        data=dict(
            xname=[1, 3, 5, 6, 0, 2, 4],
            yname=[1, 2, 1, 0, 0, 0, 0],
            name=names,
            info=info
        )
    )
    fig.annulus(x='xname', y='yname', inner_radius=0.29,
                outer_radius=0.295, source=source)

    circle = Circle(x="xname", y="yname", radius=0.29, fill_color="#e9f1f8")
    circle_renderer = fig.add_glyph(source, circle)

    x1, y1 = (-0.1, -0.04)
    fig.text(x=[-0.1, x1 + 2, x1 + 4, x1+6],
             y=[y1, y1, y1, y1], text=["S1", "S2", "S3", "S4"])
    fig.text(x=[x1 + 0.9, x1 + 5], y=[y1 + 1, y1 + 1], text=["GG", "FV"])
    fig.text(x=[x1 + 3], y=[y1 + 2], text=["EK"])

    tooltips = OrderedDict([
        ("name", "@name"),
        ("info", "@info"),
    ])
    fig.add_tools(HoverTool(tooltips=tooltips, renderers=[circle_renderer]))
    return fig, adjencency_list


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


def get_tree_plot(adjencency_list, names, info):
    """
    BFS-traversal (level order) and plot of tree.
    """
    x = []
    y = []

    q = Queue()
    root = find_root(adjencency_list)
    # This is level numebers counting from one
    # so not actually height
    height = find_height(root, adjencency_list) + 1
    q.put(root)
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
    fig = figure()
    for lev in o.keys():
        number_of_nodes = len(o[lev])
        left_right = [level_dist, -level_dist] * number_of_nodes
        side_index = 0
        for level_memeber, parent in o[lev]:
            if lev == 1:
                x.append(initial_x_manhatan)
                y.append(level)
                dist_dict[level_memeber] = float(initial_x_manhatan)
                fig.line([dist_dict[level_memeber], 0],
                         [level, level + 1])
                initial_x_manhatan += 2*abs(const) / (number_of_nodes - 1)
            elif lev !=0:
                side_factor = left_right[side_index]
                xdist = dist_dict[parent] + side_factor
                dist_dict[level_memeber] = float(xdist)
                x.append(xdist)
                y.append(level)
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
                    radius=0.25,
                    fill_color="#e9f1f8")
    circle_renderer = fig.add_glyph(source, circle)
    tooltips = OrderedDict([
        ("name", "@names"),
        ("info", "@info"),
    ])
    fig.add_tools(HoverTool(tooltips=tooltips, renderers=[circle_renderer]))

    return fig, adjencency_list
