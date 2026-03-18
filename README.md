# bus-delay-inator
![GitHub last commit](https://img.shields.io/github/last-commit/kubakalisciak/bus-delays?color=%23f78166)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/kubakalisciak/bus-delays/fetch.yml?label=fetch&color=%23238636)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/kubakalisciak/bus-delays/merge.yml?label=merge&color=%233572a5)  
- ---
A quirky project gathering data on delays of buses in my hometown (Białystok) and working with this data. Also an exercise in matplotlib and Github Actions.

## Features

- Polling data
- Automatic polling every ~5 minutes via Github Actions
- Making graphs

## Usage
1. Clone the repo onto your device
```bash
git clone https://github.com/kubakalisciak/bus-delays.git
cd bus-delays
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

*or*
Get the latest data from the repo (new data is pushed to `main` every 3 days)

```bash
cd path-to-repo/bus-delays
git fetch
git pull
```

2. Generate graphs

   - Run `graphs.py` to generate graphs from the CSV. The images are saved in the `graphs` directory.

   - Choose the the graph type (the 1st flag):

|Flag|Graph Description|Filename|
|---|---|---|
|`--recompute`|Draw all the graphs|respective names of each graph|
|`--avg-delay-date`|Average delay over the dataset by date|`avg_delay__date.png`|
|`--avg-delay-time`|Average delay over the dataset by time of day|`avg_delay__time.png`|
|`--delays-line`|Average and median delay over the dataset by line (in table format)|`delays__line.png`|
|`--median-delay-date`|Median delay over the dataset by date|`median_delay__date.png`|
|`--median-delay-time`|Median delay over the dataset by time of day|`median_delay__time.png`|
|`--punctuality-percent`|Shows the percentage of rides that were on time, delayed, or early|`punctuality_percent.png`|
|`--punctuality`|Shows the punctuality status of the rides|`punctuality.png`|


- Pick the dataset (*monthly*) (the 2nd flag)

- Format: `--YYYY-MM`, where `YYYY` is the full year number and `MM` the zero-padded month number or `--all` to access all datasets

Examples:

```bash
python graphs.py --avg-delay-line --all

python graphs.py --avg-delay-day --2026-02
```

3. Access the graphs

     - The generated images are saved in `graphs`. Open them with your OS image viewer:

```bash
xdg-open graphs/avg_delay__line.png
```

## To-Do's

- [ ] Add a "Run Report" table

## License

This project is licensed under the [GPL v3.0 License](LICENSE)
