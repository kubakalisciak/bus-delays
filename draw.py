import matplotlib.pyplot as plt
import os


def draw_graph(
    labels,
    values,
    xlabel,
    ylabel,
    title,
    filename,
    color_mapping=None,
    rotation=True,
    style='bar'
):
    """
    Draws a graph with matplotlib.

    Parameters:
    labels (list): labels for the x-axis
    values (list): values to be plotted
    xlabel (str): label for the x-axis
    ylabel (str): label for the y-axis
    title (str): title of the graph
    filename (str): name of the file to be saved
    color_mapping (dict, optional): dictionary mapping labels to colors
    rotation (bool, optional): whether to rotate the x-axis labels by 90 degrees
    style (str, optional): style of the graph ('bar', 'line', 'scatter')

    Returns:
    None
    """
    graphs_dir = 'graphs'
    os.makedirs(graphs_dir, exist_ok=True)

    fig, ax = plt.subplots()

    match style:
        case 'bar':
            if color_mapping:
                colors = [color_mapping.get(label, 'gray') for label in labels]
                ax.bar(labels, values, color=colors)
            else:
                ax.bar(labels, values)
        case 'line':
            if color_mapping:
                colors = [color_mapping.get(label, 'gray') for label in labels]
                ax.plot(labels, values, color=colors)
            else:
                ax.plot(labels, values)
        case 'scatter':
            if color_mapping:
                colors = [color_mapping.get(label, 'gray') for label in labels]
                ax.scatter(labels, values, color=colors)
            else:
                ax.scatter(labels, values)
        case _:
            raise ValueError(f'Unknown style: {style}')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if min(map(float, values)) >= 0:
        ax.set_ylim(bottom=0)

    if rotation:
        ax.tick_params(axis='x', rotation=90)
    ax.grid(axis='x', linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, filename))
    plt.close()


import os
import matplotlib.pyplot as plt

def draw_table(data, row_labels, column_labels, title, filename):
    """
    Draws a table with matplotlib and places the title just above the table.

    Parameters:
    data (list of lists): 2D data to be displayed
    row_labels (list): labels for the rows
    column_labels (list): labels for the columns
    title (str): title of the table
    filename (str): name of the file to be saved
    """
    graphs_dir = 'graphs'
    os.makedirs(graphs_dir, exist_ok=True)

    fig, ax = plt.subplots()
    ax.axis('off')

    # Create the table
    table = ax.table(
        cellText=data,
        rowLabels=row_labels,
        colLabels=column_labels,
        loc='center'
    )
    table.scale(1, 1.5)

    # Draw canvas to compute table size
    fig.canvas.draw()
    bbox = table.get_window_extent(fig.canvas.get_renderer())
    # Convert bbox from pixels to axes coordinates
    inv = ax.transAxes.inverted()
    bbox_ax = inv.transform([[bbox.x0, bbox.y0], [bbox.x1, bbox.y1]])

    # Place title just above the table
    x_center = 0.5  # horizontal center
    y_top = bbox_ax[1, 1] + 0.02  # slightly above the table
    ax.text(
        x_center, y_top, title,
        ha='center', va='bottom',
        transform=ax.transAxes,
    )

    path = os.path.join(graphs_dir, filename)
    plt.savefig(path, bbox_inches='tight')
    plt.close()