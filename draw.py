import matplotlib.pyplot as plt
import os


def draw_graph(labels, values,
               xlabel,
               ylabel,
               title,
               filename,
               color_mapping=None,
               rotation=True,
               style='bar'):

    """
    Draw a graph with given labels and values.

    Parameters
    ----------
    labels : List[str]
        List of labels for each data point.
    values : List[float]
        List of values for each data point.
    xlabel : str
        Label for the x-axis.
    ylabel : str
        Label for the y-axis.
    title : str
        Title of the graph.
    filename : str
        Name of the file to save the graph as.
    color_mapping : Dict[str, str], optional
        Mapping of labels to colors. If not provided, all data points will be gray.
    rotation : bool, optional
        Whether to rotate the x-axis labels. Defaults to True.
    style : str, optional
        Style of the graph. Can be 'bar', 'line', or 'scatter'. Defaults to 'bar'.

    Raises
    ------
    ValueError
        If an unknown style is provided.

    Returns
    -------
    None
    """
    dir_name = 'graphs'
    os.makedirs(dir_name, exist_ok=True)

    fig, axis = plt.subplots()


    match style:
        case 'bar':
            if color_mapping:
                colors = [color_mapping.get(label, 'gray') for label in labels]
                axis.bar(labels, values, color=colors)
            else:
                axis.bar(labels, values)
        case 'line':
            if color_mapping:
                colors = [color_mapping.get(label, 'gray') for label in labels]
                axis.plot(labels, values, color=colors)
            else:
                axis.plot(labels, values)
        case 'scatter':
            if color_mapping:
                colors = [color_mapping.get(label, 'gray') for label in labels]
                axis.scatter(labels, values, color=colors)
            else:
                axis.scatter(labels, values)
        case _:
            raise ValueError(f'Unknown style: {style}')

    axis.set_title(title)
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)

    if min(map(int, values)) > 0:
        axis.set_ylim(bottom=0)

    if rotation:
        axis.tick_params(axis='x', rotation=90)
    axis.grid(axis='x', linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(dir_name, filename))
    plt.close()
