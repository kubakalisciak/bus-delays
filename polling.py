import requests, csv, time


def fetch_data(stop_id):
    endpoint = f"https://przystanki.bialystok.pl/csip/vm_channel/departures.json?symbol={stop_id}"
    response = requests.get(endpoint).json()['departures']
    return response


def parse_data(data, line):
    segregated_data = []
    for row in data:
        if row['lineName'] == line:
            segregated_data.append(row)

    data_to_write = []
    for entry in segregated_data:
        if entry['online']:
            calculated_delay = round((entry['estimatedDeparture'] - entry['scheduledDeparture']) / 60000)
            entry_to_append = {'line': entry['lineName'],
                            'calculated_delay': calculated_delay,
                            'date': time.strftime("%Y-%m-%d", time.localtime()),
                            'time': time.strftime("%H:%M", time.localtime()),
                            'vechicle_number': entry['vehicleNumber']}
            data_to_write.append(entry_to_append)

    return data_to_write


def write_to_file(data):
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


def main():
    final_stops_1 = {'1': '799',
                     '2': '635',
                     '3': '261',
                     '4': '274',
                     '5': '533',
                     '6': '097',
                     '7': '368',
                     '8': '840',
                     '9': '351',
                     '10': '153',
                     '11': '652',
                     '12': '106',
                     '13': '916',
                     '14': '121',
                     '15': '688',
                     '16': '126',
                     '17': '312',
                     '18': '844',
                     '19': '126',
                     '20': '016',
                     '21': '513',
                     '22': '923',
                     '23': '582',
                     '24': '283',
                     '25': '214',
                     '26': '1260',
                     '27': '558',
                     '28': '099',
                     '29': '679',
                     '30': '635',
                     '100': '777',
                     '101': '623',
                     '102': '726',
                     '103': '936',
                     '104': '825',
                     '105': '1417',
                     '107': '232',
                     '108': '1507',
                     '109': '1894',
                     '111': '940',
                     '112': '969',
                     '113': '1121',
                     '122': '1514',
                     '123': '1139',
                     '126': '1665',
                     '132': '733',
                     '142': '1514',
                     '200': '1210',
                     '201': '1949',
                     '202': '1209',
                     'N1': '308',
                     'N2': '308',
                     'N3': '416',
                     'N4': '990',
                     'N5': '990',
                     'N6': '990'
                     }
    final_stops_2 = {'1': '551',
                     '2': '296',
                     '3': '741',
                     '4': '560',
                     '5': '043',
                     '6': '277',
                     '7': '270',
                     '8': '490',
                     '9': '575',
                     '10': '595',
                     '11': '649',
                     '12': '052',
                     '13': '078',
                     '14': '274',
                     '15': '473',
                     '16': '296',
                     '17': '337',
                     '18': '338',
                     '19': '156',
                     '20': '473',
                     '21': '582',
                     '22': '058',
                     '23': '101',
                     '24': '337',
                     '25': '185',
                     '26': '997',
                     '27': '609',
                     '28': '426',
                     '29': '126',
                     '30': '416',
                     '100': '058',
                     '101': '304',
                     '102': '303',
                     '103': '062',
                     '104': '303',
                     '105': '304',
                     '107': '058',
                     '108': '303',
                     '109': '416',
                     '111': '303',
                     '112': '304',
                     '113': '602',
                     '122': '303',
                     '123': '346',
                     '126': '365',
                     '132': '303',
                     '142': '058',
                     '200': '830',
                     '201': '1979',
                     '202': '1839',
                     'N1': '337',
                     'N2': '052',
                     'N3': '296',
                     'N4': '703',
                     'N5': '400',
                     'N6': '578'
                     }
    keys = list(final_stops_1.keys())
    for i in keys:
        print(f"fetching line {i}...")
        out_1 = parse_data(fetch_data(final_stops_1[i]), i)
        print(out_1)
        out_2 = parse_data(fetch_data(final_stops_2[i]), i)
        print(out_2)
        print(f"fetched line {i}")
        write_to_file(out_1+out_2)

    print("complete!")


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"{round(end - start, 3)}s")