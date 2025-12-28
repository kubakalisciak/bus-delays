from draw import draw_graph
import os, csv, sys, statistics


def read_dataset(set_name):
    dir_name = 'output'
<<<<<<< HEAD
    filepath = os.path.join(dir_name, filename[2:])
=======
    filepath = os.path.join(dir_name, f"{set_name}.csv")
>>>>>>> 595f4d7e39499297340870a7aa44ce7ae45ba537
    output = []
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                output.append(row)
    except FileNotFoundError:
        print("This dataset does not exist.")
    return output


<<<<<<< HEAD
def draw_graph(labels, values, xlabel, ylabel, title, filename):
    dir_name = 'graphs'
    os.makedirs(dir_name, exist_ok=True)

    fig, axis = plt.subplots()
        
    axis.bar(labels, values)
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)

    if min(values, default=0) > 0:
        axis.set_ylim(bottom=0)

    axis.set_title(title)
    axis.tick_params(axis='x', rotation=90)
    axis.grid(axis='x', linestyle='-', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(dir_name, filename))
    plt.close()


def prepare_graph_items(data, value_as_num=False, key_as_num=False):
=======
def sort_by_labels(data, value_as_num=False, key_as_num=False):
>>>>>>> 595f4d7e39499297340870a7aa44ce7ae45ba537
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


def calculate_punctuality_status(dataset):
    collected_data = {'too_early': 0,
                        'early': 0,
                        'on_time': 0,
                        'late': 0,
                        'too_late': 0}
    data = read_dataset(dataset)
    for row in data:
        if int(row['calculated_delay']) <= -3:
            collected_data['too_early'] += 1
        elif int(row['calculated_delay']) < 0:
            collected_data['early'] += 1
        elif int(row['calculated_delay']) == 0:
            collected_data['on_time'] += 1
        elif int(row['calculated_delay']) < 3:
            collected_data['late'] += 1
        else:
            collected_data['too_late'] += 1

    return collected_data


# ================================


def graph_average_delays_by_line(dataset):
    count, summed_delays = {}, {}
    data = read_dataset(dataset)
    for row in data:
        line = row['line']
        try:
            count[line] += 1
            summed_delays[line] += int(row['calculated_delay'])
        except KeyError:
            count[line] = 1
            summed_delays[line] = int(row['calculated_delay'])

    avg_delays = calculate_average_delays(count, summed_delays)

    labels, values = sort_by_labels(avg_delays, value_as_num=True, key_as_num=True)

    draw_graph(labels, values,
               'line',
               'average delay',
               'Average delay by line',
               'avg_delay__line.png')


def graph_average_delays_by_day(dataset):
    count, summed_delays = {}, {}
    data = read_dataset(dataset)
    for row in data:
        date = row['date']
        try:
            count[date] += 1
            summed_delays[date] += int(row['calculated_delay'])
        except KeyError:
            count[date] = 1
            summed_delays[date] = int(row['calculated_delay'])

    avg_delays = calculate_average_delays(count, summed_delays)

    labels, values = sort_by_labels(avg_delays, value_as_num=True)
    values = [round(x, 2) for x in values]

    draw_graph(labels, values,
               'date',
               'average delay',
               'Average delay by date',
               'avg_delay__date.png',
               style='line')
    

def graph_punctuality(dataset):
    collected_data = calculate_punctuality_status(dataset)

    labels = [x.replace('_', ' ') for x in collected_data.keys()]
    values = collected_data.values()

    mapping = {
        'too early': 'red',
        'early': 'orange',
        'on time': 'blue',
        'late': 'orange',
        'too late': 'red'
    }

    draw_graph(labels, values,
               '',
               'no. of rides',
               'Amount of punctual rides',
               'punctuality.png',
               color_mapping=mapping,
               rotation=False)


def graph_punctuality_percentage(dataset):
    collected_data = calculate_punctuality_status(dataset)

    labels = [x.replace('_', ' ') for x in collected_data.keys()]
    values = list(collected_data.values())
    
    amount_of_rides = sum(values)

    for i in range(len(values)):
        values[i] = (values[i] / amount_of_rides) * 100

    mapping = {
        'too early': 'red',
        'early': 'orange',
        'on time': 'blue',
        'late': 'orange',
        'too late': 'red'
    }
    
    draw_graph(labels, values, 
               '', 
               '% of rides', 
               '% of punctual rides', 
               'punctuality_percent.png', 
               color_mapping=mapping, 
               rotation=False)
    

def graph_median_delay_by_line(dataset):
    data = read_dataset(dataset)
    organized_data = {}
    for row in data:
        line = row['line']
        try:
            organized_data[line].append(int(row['calculated_delay']))
        except KeyError:
            organized_data[line] = [int(row['calculated_delay'])]

    for key in organized_data.keys():
        organized_data[key] = int(statistics.median(organized_data[key]))

    labels, values = sort_by_labels(organized_data, value_as_num=True, key_as_num=True)

    draw_graph(labels, values,
               'line',
               'median delay',
               'Median delay by line',
               'median_delay__line.png',
               style='scatter')


def graph_median_delay_by_date(dataset):
    data = read_dataset(dataset)
    organized_data = {}
    for row in data:
        date = row['date']
        try:
            organized_data[date].append(int(row['calculated_delay']))
        except KeyError:
            organized_data[date] = [int(row['calculated_delay'])]

    for key in organized_data.keys():
        organized_data[key] = int(statistics.median(organized_data[key]))

    labels, values = sort_by_labels(organized_data, value_as_num=True, key_as_num=False)

    draw_graph(labels, values,
               'date',
               'median delay',
               'Median delay by date',
               'median_delay__date.png',
               style='line')


def main():
    match sys.argv[1]:
        case '--avg-delay-line':
            graph_average_delays_by_line(sys.argv[2][2:])
        case '--avg-delay-date':
            graph_average_delays_by_day(sys.argv[2][2:])
        case '--punctuality':  
            graph_punctuality(sys.argv[2][2:])
        case '--punctuality-percent':
            graph_punctuality_percentage(sys.argv[2][2:])
        case '--median-delay-line':
            graph_median_delay_by_line(sys.argv[2][2:])
        case '--median-delay-date': 
            graph_median_delay_by_date(sys.argv[2][2:])
        case _:
            print("Invalid command. Try again.")
            print("Refer to README.md for possible options.")


if __name__ == "__main__":
    main()
