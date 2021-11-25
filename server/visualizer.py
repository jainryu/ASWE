'''
html visualizers for message counts
'''
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Response

def single_plot(result, title=None, x_label=None, y_label=None):
    """
    plot counts per year or month for a single lead source
    """
    time = []
    counts = []
    for year, count in result.items():
        time.append(year)
        counts.append(count)

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(time, counts, '-o')

    if title:
        axis.title.set_text(title)
    if x_label:
        axis.set_xlabel(x_label)
    if y_label:
        axis.set_ylabel(y_label)

    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def both_plot(result, title=None, x_label=None, y_label=None):
    """
    plot counts per year or month for a both lead sources
    """
    x_values = []
    facebook = []
    thumbtack = []
    total = []
    for times, counts in result.items():
        x_values.append(times)
        facebook.append(counts["facebook"])
        thumbtack.append(counts["thumbtack"])
        total.append(counts["total"])

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x_values, facebook, '-o')
    axis.plot(x_values, thumbtack, '-x')
    axis.plot(x_values, total, '-')

    if title:
        axis.title.set_text(title)
    if x_label:
        axis.set_xlabel(x_label)
    if y_label:
        axis.set_ylabel(y_label)
    axis.legend(['facebook','thumbtack', 'total'])
    axis.set_xticks(x_values[::int(len(x_values)/10) + 1])
    axis.tick_params(labelrotation=30)

    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
