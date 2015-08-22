from bokeh.plotting import show, figure
from bokeh.models import HoverTool, ColumnDataSource, Circle
from collections import OrderedDict

def test_binary_tree(adjencency_list):
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