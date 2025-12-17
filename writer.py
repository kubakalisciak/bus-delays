from api import fetch_data
import csv, datetime

def parse_data(data, line):
    segregated_data = []
    for row in data:
        if row['lineName'] is line:
            segregated_data.append(row)

    data_to_write = []
    for entry in segregated_data:
        if entry['online']:
            calculated_delay = round((entry['scheduledDeparture'] - entry['estimatedDeparture']) / 60000)
            entry_to_append = {'line': entry['lineName'],
                            'calculated_delay': calculated_delay,
                            'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                            'time': datetime.datetime.now().strftime("%H:%M"),
                            'vechicle_number': entry['vehicleNumber']}
            data_to_write.append(entry_to_append)

    return data_to_write
