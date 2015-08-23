from bokeh.plotting import show, figure
from bokeh.models import HoverTool, ColumnDataSource, Circle
from collections import OrderedDict

def test_binary_tree(adjencency_list):
    """
    Hardcoded bokeh 3 level completely balanced binary Tree
    Attempting to automate to n level trees in the function
    bellow.
    """
    fig = figure(
    title='DDS Help Tree',
    tools= 'box_zoom,box_select,resize,reset' # Note no hover
    )
    names = ["Gavin Gray", "Ewan Klein", "Francisco Vargas", "S3", "S1", "S2", "S4"]
    info = ["TA", "Lectuer", "TA", "Student", "Student", "Student", "Student"]
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.axis.major_label_text_font_size = '0pt'  
    fig.axis.major_tick_line_color = None
    fig.axis[0].ticker.num_minor_ticks = 0
    fig.axis[1].ticker.num_minor_ticks = 0
    fig.outline_line_color = "white"
    fig.xaxis.axis_line_color = "white"
    fig.yaxis.axis_line_color = "white"
    fig.line(x=[1,3,5],y=[1,2,1])
    fig.line(x=[0,1,2],y=[0,1,0])
    fig.line(x=[4,5,6],y=[0,1,0])

    source = ColumnDataSource(
        data=dict(
            xname=[1, 3, 5,6,0,2,4],
            yname=[1, 2, 1,0,0,0,0],
            name = names,
            info = info
        )
    )
    fig.annulus(x='xname', y='yname', inner_radius=0.29, outer_radius=0.295,source=source)

    circle = Circle(x='xname', y='yname', radius=0.29, fill_color='#e9f1f8')
    circle_renderer = fig.add_glyph(source, circle)

    x1, y1 = (-0.1, -0.04)
    fig.text(x=[-0.1, x1 + 2, x1 + 4, x1+6] , y=[y1, y1, y1 , y1] , text=["S1", "S2", "S3", "S4"])
    fig.text(x=[x1 + 0.9, x1 + 5] , y=[y1 +1 , y1 +1] , text=["GG", "FV"])
    fig.text(x=[x1 + 3] , y=[y1 +2] , text=["EK"])

    tooltips = OrderedDict([
        ('name', '@name'),
        ('info', '@info'),
    ])
    fig.add_tools( HoverTool(tooltips=tooltips, renderers=[circle_renderer]))
    return fig, adjencency_list


def balanced_tree_by_height(height=0):
    """
    Complete binary tree function plotter. Created with
    the hope of automating with adjencency_list input
    based trees. Manhatan distances are used in placing the nodes
    in order to keep everything discrete. Trying to avoid recursion.
    TODO: Lines connecting nodes
    """
    # Base nodes (Circle):
    y = [0]
    x = [0]
    initial_x_manhatan = -(height -1)
    level_dist = initial_x_manhatan
    level = -1
    # BFS-traversal like plot by level
    for node_power in range(1, height):
        number_of_nodes = 2**(node_power)
        for node_x in range(0, number_of_nodes):
            x.append(initial_x_manhatan)
            y.append(level)
            initial_x_manhatan += 2*abs(level_dist) / (number_of_nodes -1)
        level -= 1
        initial_x_manhatan = -(height - level) + 2
        level_dist = initial_x_manhatan
    fig = figure()

    source = ColumnDataSource(
        data=dict(
            xname=x,
            yname=y
        )
    )
    circle = Circle(x="xname",
                    y="yname" ,
                    radius=0.29,
                    fill_color='#e9f1f8')
    circle_renderer = fig.add_glyph(source, circle)
    return fig
