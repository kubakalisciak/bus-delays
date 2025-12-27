# bus-delay-inator
A quirky project gathering data on delays of buss in my hometown (Białystok) and working with those data. Also a kind of exercise in matplotlib and Github Actions.

## Features
- Polling data
- Automatic polling every X minutes via Github Actions
- Making graphs
- And many more to come…

## Installation
Clone the repository and install dependencies (example uses pip and a virtualenv):
```bash
git clone https://github.com/kubakalisciak/bus-delays.git
cd bus-delays
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## To-Do's
- [ ] Gather the artifacts from Github Actions
- [ ] Add more graphs
    - Average delays by tme of day
    - Most delayed lines/vehicles
    - Trends over days, weeks etc.
    - How much on time, delayed, early etc.
- [ ] Add some ML capabilities
- [ ] Add a 'Usage' section to the README

## License
This project is licensed under the [GPL v3.0 License](LICENSE)