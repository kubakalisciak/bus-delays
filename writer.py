import csv


def append_to_file(data):
    filename = 'output.csv'
    fieldnames = ['line', 'calculated_delay', 'date', 'time', 'vechicle_number']

    try:
        with open(filename, 'a', newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for row in data:
                writer.writerow(row)
    except FileNotFoundError:
        with open(filename, 'w', newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

        writer.writerows(data)