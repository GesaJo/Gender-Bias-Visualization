"""creating plots (word-clouds) with bokeh"""
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LabelSet, ColumnDataSource


def bokeh_magic(x_values, y_values, labels, color):
    """create a word cloud"""

    source = ColumnDataSource(data=dict(x=x_values,
                                        y=y_values,
                                        labels=labels))
    cloud = figure(x_axis_label="x",
                   y_axis_label="y",
                   toolbar_location=None,
                   active_scroll="wheel_zoom")

    cloud.scatter(x_values, y_values, size=12, fill_color=color)
    labels = LabelSet(x="x", y="y", text='labels', level='glyph', x_offset=5,
                      y_offset=5, source=source, render_mode='canvas')
    cloud.add_layout(labels)
    cloud.grid.visible = False
    cloud.axis.visible = False
    cloud.outline_line_color = None
    script, divtag = components(cloud)
    return script, divtag
