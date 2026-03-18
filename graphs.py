from draw import draw_graph, draw_table
import os, csv, sys, statistics


def read_dataset(set_name):
    dir_name = 'output'
    filepath = os.path.join(dir_name, f"{set_name}.csv")
    output = []
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                output.append(row)
    except FileNotFoundError:
        print("This dataset does not exist.")
    return output


def sort_by_labels(data, value_as_num=False, key_as_num=False):
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


def calculate_punctuality_status(data):
    collected_data = {'too_early': 0,
                        'early': 0,
                        'on_time': 0,
                        'late': 0,
                        'too_late': 0}
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


def read_all_datasets():
    dir_name = 'output'
    files = os.listdir(dir_name)
    data = []
    for file in files:
        filepath = os.path.join(dir_name, file)
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

    return data


def compute_all_graphs(data):
    table_delays_by_line(data)
    graph_average_delays_by_day(data)
    graph_median_delay_by_date(data)
    graph_punctuality(data)
    graph_punctuality_percentage(data)
    graph_average_delay_by_time_of_day(data)
    graph_median_delay_by_time_of_day(data)


# ================================


def table_delays_by_line(data):
    collected_data = {}
    for row in data:
        line = row['line']
        try:
            collected_data[line].append(int(row['calculated_delay']))
        except KeyError:
            collected_data[line] = [int(row['calculated_delay'])]

    lines = sorted(collected_data.keys(), key=int)

    processed_data = {}

    for line in lines:
        delays = collected_data[line]

        average = round(statistics.mean(delays), 2)
        median = int(statistics.median(delays))

        processed_data[line] = [average, median]

    keys = list(processed_data.keys())
    values = list(processed_data.values())

    draw_table(values, keys, ['avg', 'median'], "Delays by line", 'delays__line.png')


def graph_average_delays_by_day(data):
    count, summed_delays = {}, {}
    for row in data:
        date = row['date']
        try:
            count[date] += 1
            summed_delays[date] += int(row['calculated_delay'])
        except KeyError:
            count[date] = 1
            summed_delays[date] = int(row['calculated_delay'])

    avg_delays = {date: value / count[date] for date, value in summed_delays.items()}
    
    labels, values = sort_by_labels(avg_delays, value_as_num=True, key_as_num=False)

    draw_graph(labels, values,
               'date',
               'average delay',
               'Average delay by date',
               'avg_delay__date.png',
               style='line')


def graph_median_delay_by_date(data):
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
    

def graph_punctuality(data):
    collected_data = calculate_punctuality_status(data)

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


def graph_punctuality_percentage(data):
    collected_data = calculate_punctuality_status(data)

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
    

def graph_average_delay_by_time_of_day(data):
    organized_data = {}
    if not data:
        return

    for row in data:
        hour = row['time']
        if hour:
            hour = int(hour.split(':')[0])
            try:
                organized_data[str(hour)].append(int(row['calculated_delay']))
            except KeyError:
                organized_data[str(hour)] = [int(row['calculated_delay'])]

    for row in organized_data:
        organized_data[row] = float(statistics.mean(organized_data[row]))

    labels, values = sort_by_labels(organized_data, value_as_num=True, key_as_num=True)

    draw_graph(labels, values,
               'hour of day',
               'average delay',
               'Average delay by hour of day',
               'avg_delay__time.png',
               style='line')


def graph_median_delay_by_time_of_day(data):
    organized_data = {}
    for row in data:
        hour = row['time']
        if hour:
                hour = int(hour.split(':')[0])
                try:
                    organized_data[str(hour)].append(int(row['calculated_delay']))
                except KeyError:
                    organized_data[str(hour)] = [int(row['calculated_delay'])]

    for row in organized_data:
        organized_data[row] = float(statistics.median(organized_data[row]))

    labels, values = sort_by_labels(organized_data, value_as_num=True, key_as_num=True)

    draw_graph(labels, values,
               'hour of day',
               'median delay',
               'Median delay by hour of day',
               'median_delay__time.png',
               style='line')


def main():
    graph_name = sys.argv[1]
    dataset_name = sys.argv[2][2:]
    if dataset_name == 'all':
        data = read_all_datasets()
    else:
        data = read_dataset(dataset_name)

    graph_functions = {
        '--delays-line': table_delays_by_line,
        '--avg-delay-date': graph_average_delays_by_day,
        '--median-delay-date': graph_median_delay_by_date,
        '--punctuality': graph_punctuality,
        '--punctuality-percent': graph_punctuality_percentage,
        '--avg-delay-time': graph_average_delay_by_time_of_day,
        '--median-delay-time': graph_median_delay_by_time_of_day,
        '--recompute': compute_all_graphs
    }

    if graph_name in graph_functions:
        graph_functions[graph_name](data)
    else:
        print(f"Invalid command: {graph_name}. Try again.")
        print("Refer to README.md for possible options.")



if __name__ == "__main__":
    main()
