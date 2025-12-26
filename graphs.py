import matplotlib.pyplot as plt
import os, csv

dir_name = 'output'

def read_data_from_file():
    filename = os.path.join(dir_name, 'output.csv')
    output = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            output.append(row)

    return output

def graph_average_delays_by_line():
    count, total_delay = {}, {}
    data = read_data_from_file()
    for row in data:
        line = row['line']
        try:
            count[line] += 1
            total_delay[line] += int(row['calculated_delay'])
        except KeyError:
            count[line] = 1
            total_delay[line] = int(row['calculated_delay'])

    # compute average delays
    avg_delays = {}
    for i in count.keys():
        avg_delays[i] = total_delay[i] / count[i]
    avg_delays = dict(sorted(avg_delays.items()))

    # plot the graph
    sorted_items = sorted(avg_delays.items(), key=lambda x: int(x[0]))
    labels = [str(k) for k, v in sorted_items]
    values = [v for k, v in sorted_items]

    fig = plt.figure()
    axis = fig.add_subplot(111)

    axis.bar(labels, values)
    axis.set_xlabel('Line')
    axis.set_ylabel('Average Delay')
    axis.set_title('Average Delay by Line')
    plt.xticks(rotation=90)
    plt.tight_layout()
    axis.grid(axis='x', linestyle='-', alpha=0.3)

    plt.savefig(os.path.join(dir_name, 'avg_delay__line.png'))
    plt.close()


def graph_average_delays_by_day():
    data = read_data_from_file()
    count, total_delay = {}, {}
    for row in data:
        date = row['date']
        try:
            count[date] += 1
            total_delay[date] += int(row['calculated_delay'])
        except KeyError:
            count[date] = 1
            total_delay[date] = int(row['calculated_delay'])

    # compute average delays
    avg_delays = {}
    for i in count.keys():
        avg_delays[i] = total_delay[i] / count[i]
    avg_delays = dict(sorted(avg_delays.items()))

    # plot the graph
    sorted_items = sorted(avg_delays.items())
    labels = [str(k) for k, v in sorted_items]
    values = [v for k, v in sorted_items]

    fig = plt.figure()
    axis = fig.add_subplot(111)

    axis.bar(labels, values)
    axis.set_xlabel('Line')
    axis.set_ylabel('Average Delay')
    axis.set_title('Average Delay by Day')
    plt.xticks(rotation=90)
    plt.tight_layout()
    axis.grid(axis='x', linestyle='-', alpha=0.3)

    plt.savefig(os.path.join(dir_name, 'avg_delay__day.png'))
    plt.close()



def main():
    graph_average_delays_by_day()


if __name__ == "__main__":
    main()