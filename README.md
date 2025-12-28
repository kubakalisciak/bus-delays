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

## Usage

1. Obtain the latest CSV data (updated by GitHub Actions)

     - This repository includes a scheduled GitHub Action (see `.github/workflows/fetch.yml`) that runs every 10 minutes and can be run manually. The workflow runs `api.py`, appends/deduplicates `output/output.csv` and pushes the result to a branch named `data`.

     - To get the latest CSV locally you can merge the `data` branch into `main`:
         ```bash
         git fetch origin
         git checkout main
         git merge origin/data
         ```

     - If you don't want to merge the branch into `main`, fetch just the CSV file from the remote `data` branch:
         ```bash
         git fetch origin
         mkdir -p output
         git show origin/data:output/output.csv > output/output.csv
         ```

     - To force an immediate update, trigger the workflow manually from the repository's Actions tab (or use `workflow_dispatch`). After the job finishes, fetch the `data` branch as above.

     - Notes: the workflow commits and pushes to the `data` branch (it may force-push). Pulling the single CSV file is safer than merging the entire branch if you only want the artifact.

2. Generate graphs

   - Run graphs.py to generate graphs from the CSV. The images are saved in the graphs/ directory.

   - Choose the the graph type (the 1st flag):

|Flag|Graph Description|Filename|
|---|---|---|
|`--avg-delay-line`|Average delay over the dataset by line|`avg_delay__line.png`
`--avg-delay-day`|Average delay over the dataset by day|`avg_delay__day.png`

  - Pick the dataset (*monthly*) (the 2nd flag)
    - Format: `--YYYY-MM`, where `YYYY` is the full year number and `MM` the zero-padded month number

Examples:

```bash
python graphs.py --avg-delay-line --2025-12

python graphs.py --avg-delay-day --2026-02
```
3. Access the graphs

     - The generated images are saved in `graphs/`. List or open them with your OS image viewer:
         ```bash
         ls graphs/
         xdg-open graphs/avg_delay__line.png
         ```

## To-Do's
- [ ] Add more graphs
    - Average delays by tme of day
    - Most delayed lines/vehicles
    - Trends over days, weeks etc.
    - How much on time, delayed, early etc.
- [ ] Add some ML capabilities
- [ ] Add a flag to use all datasets
- [x] Add a 'Usage' section to the README
- [x] Refactor the graphing generator script to use *sys.argv*

## License
This project is licensed under the [GPL v3.0 License](LICENSE)