from draw import draw_graph, draw_table
import os, csv, sys, statistics, datetime


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
        return False
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


def create_log(success, graph_name, dataset_name, dataset_size, start_time, filename='_report.txt', dir='graphs'):
    with open(os.path.join(dir, filename), 'w') as file:
        now = datetime.datetime.now()
        file.write(f"current time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"success: {success}\n")
        if graph_name == '--avg-line-delay-hour' or graph_name == '--avg-line-delay-day':
            file.write(f"flag name: {graph_name}")
            if success:
                file.write(f" (line: {sys.argv[3][2:]})\n")
            else:
                file.write("\n")
        else:
            file.write(f"flag name: {graph_name}\n")
        file.write(f"dataset name: {dataset_name}\n")
        if success:
            file.write(f"dataset size: {dataset_size} entries\n")
            file.write(f"time: {(now - start_time).total_seconds():.3f}s\n")


def compute_all_graphs(data):
    table_delays_by_line(data)
    graph_average_delays_by_day(data)
    graph_punctuality(data)
    graph_punctuality_percentage(data)
    graph_average_delay_by_hour(data)

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

    draw_table(values, keys, ['Average delay', 'Median delay'], "Delays by line", 'delays__line.png')


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
    

def graph_average_delay_by_hour(data):
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
               'avg_delay__hour.png',
               style='line')


def graph_average_line_delay_by_hour(data, line):
    count, summed_delays = {}, {}
    for row in data:
        if row['line'] == line:
            hour = row['time'].split(':')[0]
            try:
                count[hour] += 1
                summed_delays[hour] += int(row['calculated_delay'])
            except KeyError:
                count[hour] = 1
                summed_delays[hour] = int(row['calculated_delay'])
    
    avg_delays = {hour: value / count[hour] for hour, value in summed_delays.items()}
    labels, values = sort_by_labels(avg_delays, value_as_num=True, key_as_num=True)

    draw_graph(labels, values,
               'hour of day',
               'average delay',
               f'Average delay by hour of day on line {line}',
               f'avg_delay__hour_{line}.png',
               style='line')
    

def graph_average_line_delay_by_day(data, line):
    count, summed_delays = {}, {}
    for row in data:
        if row['line'] == line:
            date = row['date']
            try:
                count[date] += 1
                summed_delays[date] += int(row['calculated_delay'])
            except KeyError:
                count[date] = 1
                summed_delays[date] = int(row['calculated_delay'])
    
    avg_delays = {date: value / count[date] for date, value in summed_delays.items()}
    labels, values = sort_by_labels(avg_delays, value_as_num=True, key_as_num=False)

    try:
        draw_graph(labels, values,
               'date',
               'average delay',
               f'Average delay by date on line {line}',
               f'avg_delay__hour_{line}.png',
               style='line')
    except ValueError:
        return False
    
    return True


def main():
    success = False
    start_time = datetime.datetime.now()
    graph_name = sys.argv[1]
    dataset_name = sys.argv[2][2:]
    if dataset_name == 'all':
        data = read_all_datasets()
    else:
        data = read_dataset(dataset_name)

    dataset_size = len(data) if data else 0

    graph_functions = {
        '--delays-line': table_delays_by_line,
        '--avg-delay-date': graph_average_delays_by_day,
        '--punctuality': graph_punctuality,
        '--punctuality-percent': graph_punctuality_percentage,
        '--avg-delay-hour': graph_average_delay_by_hour,
        '--avg-line-delay-hour': graph_average_line_delay_by_hour,
        '--avg-line-delay-day': graph_average_line_delay_by_day,
        '--recompute': compute_all_graphs
    }

    if graph_name in graph_functions:
        if graph_name == '--avg-line-delay-hour' or graph_name == '--avg-line-delay-day':
            success = graph_functions[graph_name](data, sys.argv[3][2:])
        else:
            graph_functions[graph_name](data)
            success = True
    else:
        print(f"Invalid command: {graph_name}. Try again.")
        print("Refer to README.md for possible options.")

    create_log(success, graph_name, dataset_name, dataset_size, start_time)


if __name__ == "__main__":
    main()
