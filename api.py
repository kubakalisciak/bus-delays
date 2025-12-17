import requests, json


def fetch_data(stop_id):
    endpoint = f"https://przystanki.bialystok.pl/csip/vm_channel/departures.json?symbol={stop_id}"
    response = requests.get(endpoint).json()['departures']
    return response


def main():
    print(json.dumps(fetch_data("303"), indent=2))
    

if __name__ == "__main__":
    main()