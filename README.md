# xT-Weighted PageRank on Passing Networks

A soccer-analytics project that ranks players by their **centrality in their team's passing
network** at the 2023 FIFA Women's World Cup, using a Weighted PageRank (WPR) algorithm on
StatsBomb event data.

## What this measures

For every match, each team's passing is modelled as a **directed weighted network** — players are
nodes, successful passes are edges. Each pass is weighted by two factors:

1. **Expected Threat added (ΔxT)** — the increase in the probability of scoring that the pass
   produces, using a **custom xT grid trained on this tournament's own event data**
   (`Evaluation/wwc2023_trained_xT_grid.csv`, 12×16 cells).
2. **Pressure** — a small bonus when the passer completes the pass under defensive pressure.

Weighted PageRank (damping factor 0.85) is then run on each team's network, giving every player a
WPR score per match. To compare players across matches, scores are **Z-score normalized per match**
and then averaged per player, producing the final `average_z_score`.

> **Important:** `average_z_score` measures how central a player is to their team's passing
> structure under this model. It is **not** a general measure of offensive contribution — it does
> not track goals, assists, or team results, and it is essentially uncorrelated with match ratings
> such as Sofascore. It is best used *alongside* outcome-based metrics to understand *role and
> system*, not to rank who scored or won.

## Pipeline

```
Download_Statsbomb.py        -> downloads StatsBomb open data into data/wwc2023/{events,lineups,...}
socceraction_load_and_convert_statsbomb_data.ipynb -> converts event data to SPADL (data/spadl-statsbomb.h5)
socceraction_xT.ipynb        -> trains the custom 12x16 xT grid -> Evaluation/wwc2023_trained_xT_grid.csv
WWC_PageRank_Core.ipynb      -> per-team weighted passing networks + Weighted PageRank
                               -> Results/all_matches_wpr_combined.csv
WWC_PageRank_Final_Processing.ipynb -> per-match Z-scores -> Results/player_rankings_z_score.csv
Add positions.ipynb          -> enriches with lineup positions -> Results/player_rankings_with_positions.csv
```

## Results — Top 10 players by average_z_score (WWC 2023)

| Rank | Player | Team | Avg Z-Score | Position |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Khadija Monifa Shaw | Jamaica | 2.97 | Center Forward |
| 2 | Barbra Banda | Zambia | 2.81 | Center Forward |
| 3 | Thị Thảo Thái | Vietnam | 2.60 | Defensive Midfielder |
| 4 | Katrina Rivera Guillou | Philippines | 2.51 | Central Midfielder |
| 5 | Marta Cox Villarreal | Panama | 2.23 | Center Forward |
| 6 | Pernille Harder | Denmark | 2.22 | Attacking Midfielder |
| 7 | Thị Thanh Nhã Nguyễn | Vietnam | 2.19 | Winger |
| 8 | Thembi Kgatlana | South Africa | 2.12 | Center Forward |
| 9 | Alex Morgan | United States | 1.96 | Center Forward |
| 10 | Nérilia Mondesir | Haiti | 1.95 | Winger |

Full rankings are in `Results/player_rankings_with_positions.csv`.

## Setup and Usage

### 1. Prerequisites
- Python 3.9+, Jupyter

### 2. Clone and install
```bash
git clone https://github.com/shawnhdx0710/xT-weighted-PageRank-on-passing-networks.git
cd xT-weighted-PageRank-on-passing-networks
pip install -r requirements.txt
```

### 3. Get the data
StatsBomb's open data is not redistributable, so the raw JSON is **not** in this repository
(it is git-ignored). Download it yourself:

```bash
python Download_Statsbomb.py
```
This downloads the 2023 FIFA Women's World Cup (and Euro 2022) event/lineup data into
`data/wwc2023/` and `data/euro2022/`. Alternatively, grab the files manually from
[StatsBomb/open-data](https://github.com/statsbomb/open-data) and place them in:

```
data/wwc2023/
├── events/<match_id>.json
├── lineups/<match_id>.json
└── three-sixty/<match_id>.json
```

### 4. Run
The trained xT grid (`Evaluation/`) and final results (`Results/`) are already included, so you can
run the main pipeline immediately. To reproduce the grid from scratch, run the two socceraction
notebooks in order first.

Run the notebooks in order:
1. `WWC_PageRank_Core.ipynb` — builds networks + computes WPR
2. `WWC_PageRank_Final_Processing.ipynb` — Z-scores and final ranking
3. `Add positions.ipynb` — position enrichment

*(Optional: rerun `socceraction_load_and_convert_statsbomb_data.ipynb` and `socceraction_xT.ipynb`
first to retrain the xT grid.)*

## Acknowledgements & Data Source
- Data: **StatsBomb** open data (see their [open-data](https://github.com/statsbomb/open-data)
  repository and user agreement).
- Libraries: [socceraction](https://github.com/ML-KULeuven/socceraction) (MIT), and the standard
  scientific Python stack.
- xT concept: [Karun Singh's Expected Threat](https://karun.in/blog/expected-threat.html).

## License
[MIT](LICENSE)
