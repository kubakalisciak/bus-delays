import matplotlib.pyplot as plt
import os, csv


def read_data_from_file():
    dir_name = 'output'
    filename = os.path.join(dir_name, 'output.csv')
    output = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            output.append(row)

    return output


def draw_graph(labels, values, xlabel, ylabel, title, filename):
    dir_name = 'output'
    os.makedirs(dir_name, exist_ok=True)

    fig, axis = plt.subplots()
        
    axis.bar(labels, values)
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)

    if min(values) > 0:
        axis.set_ylim(bottom=0)

    axis.set_title(title)
    axis.tick_params(axis='x', rotation=90)
    axis.grid(axis='x', linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(dir_name, filename))
    plt.close()



def sort_graph_items(data, value_as_num=False, key_as_num=False):
    if key_as_num:
        dict_keys = data.keys()
        int_keys_data = {}
        for key in dict_keys:
            int_keys_data[int(key)] = data[key]
        sorted_data = sorted(int_keys_data.items())
    else:
        sorted_data = sorted(data.items())
    labels = []
    values = []
    for row in sorted_data:
        labels.append(str(row[0]))
        values.append(str(row[1]))
    if value_as_num:
        values = list(map(float, values))

    return labels, values


def calculate_average_delays(count, summed_delays):
    avg_delays = {}
    for i in count.keys():
        avg_delays[i] = summed_delays[i] / count[i]

    return avg_delays


def graph_average_delays_by_line():
    count, summed_delays = {}, {}
    data = read_data_from_file()
    for row in data:
        line = row['line']
        try:
            count[line] += 1
            summed_delays[line] += int(row['calculated_delay'])
        except KeyError:
            count[line] = 1
            summed_delays[line] = int(row['calculated_delay'])

    avg_delays = calculate_average_delays(count, summed_delays)

    labels, values = sort_graph_items(avg_delays, value_as_num=True, key_as_num=True)

    draw_graph(labels, values, 'linia', 'średnie opóźnienie', 'wykres1', 'avg_delay__line.png')


def graph_average_delays_by_day():
    count, summed_delays = {}, {}
    data = read_data_from_file()
    for row in data:
        date = row['date']
        try:
            count[date] += 1
            summed_delays[date] += int(row['calculated_delay'])
        except KeyError:
            count[date] = 1
            summed_delays[date] = int(row['calculated_delay'])

    avg_delays = calculate_average_delays(count, summed_delays)

    labels, values = sort_graph_items(avg_delays, value_as_num=True)
    values = [round(x, 2) for x in values]

    draw_graph(labels, values, 'dzień', 'średnie opóźnienie', 'wykres2', 'avg_delay__day.png')


def main():
    graph_average_delays_by_day()


if __name__ == "__main__":
    main()