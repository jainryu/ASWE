'''
html visualizers for message counts
'''

import plotly.graph_objects as go

def single_plot(result, title, x_label, y_label):
    """
    plot counts per year or month for a single lead source
    """
    time = []
    counts = []
    for year, count in result.items():
        time.append(year)
        counts.append(count)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=counts, mode='lines', name='lines'))
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    return fig.to_html()

def both_plot(result, title, x_label, y_label):
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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=facebook,
                             line=dict(color='royalblue', width=4, dash='dot'),
                             name='facebook'))
    fig.add_trace(go.Scatter(x=x_values, y=thumbtack,
                             line = dict(color='firebrick', width=4, dash='dot'),
                             name='thumbtack'))
    fig.add_trace(go.Scatter(x=x_values, y=total, mode='lines', name='total'))

    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    return fig.to_html()
