
# bus-delay-inator

A quirky project gathering data on delays of buss in my hometown (Białystok) and working with those data. Also a kind of exercies in matplotlib and Github Actions.


## Features

- Polling data
- Automatic polling every X minutes via Github Actions
- Making graphs
- And many more to come…


## Installation

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
Then, install the dependencies:
```bash
pip install matplotlib requests
```


## To-Do's

- [ ] Gather the artifacts from Github Actions
- [ ] Add more graphs
    - Average delays by tme of day
    - Most delayed lines/vehicles
    - Trends over days, weeks etc.
    - How much on time, delayed, early etc.
- [ ] Add some ML capabilities
## License

This project is licensed under the[GPL v3.0 License](LICENSE)