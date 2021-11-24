#import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Response

def single_graph(result, title=None, x_label=None, y_label=None):
    x = []
    y = []
    for year, count in result.items():
        x.append(year)
        y.append(count)

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y, '-o')

    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')