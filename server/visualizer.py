#import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Response
import numpy as np

def single_plot(result, title=None, x_label=None, y_label=None):
    x = []
    y = []
    for year, count in result.items():
        x.append(year)
        y.append(count)

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y, '-o')

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
    x = []
    facebook = []
    thumbtack = []
    total = []
    for year, counts in result.items():
        x.append(year)
        facebook.append(counts["facebook"])
        thumbtack.append(counts["thumbtack"])
        total.append(counts["total"])

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, facebook, '-o')
    axis.plot(x, thumbtack, '-x')
    axis.plot(x, total, '-')

    if title:
        axis.title.set_text(title)
    if x_label:
        axis.set_xlabel(x_label)
    if y_label:
        axis.set_ylabel(y_label)
    axis.legend(['facebook','thumbtack', 'total'])
    axis.set_xticks(x[::int(len(x)/10) + 1])
    axis.tick_params(labelrotation=30)

    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')