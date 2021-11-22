from io import BytesIO
import base64
import matplotlib.pyplot as plt

def single_graph(result, title=None, x_label=None, y_label=None):
    tmpfile = BytesIO()
    x = []
    y = []
    for year, count in result.items():
        print("year: ", year)
        x.append(year)
        y.append(count)
    '''
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    '''
    plt.plot(x, y, '-o')
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    return html
