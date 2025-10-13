# Weighted PageRank for Player Analysis in the 2023 Women's World Cup

## Overview

This project introduces a novel approach to player performance analysis using a custom **Weighted PageRank (WPR)** algorithm. Traditional soccer metrics often fail to capture a player's influence within their team's passing network. This model moves beyond simple pass counts to evaluate players based on the quality and context of their passing contributions.

The core of this project is a custom PageRank algorithm applied to passing networks from the 2023 FIFA Women's World Cup. The weight of each pass (an edge in the network graph) is determined by a combination of:

1.  **Expected Threat (xT) Added:** The change in the probability of scoring resulting from the pass.
2.  **Pressure:** Bonuses are applied for making or receiving passes while under pressure from opponents.

The final WPR score for each player represents their overall influence and importance in creating threatening opportunities for their team.

## Key Features & Methodology

The analysis is conducted through a series of steps, detailed in the Jupyter Notebooks:

1.  **Data Preparation:** StatsBomb event data is converted into the SPADL (Soccer Player Action Description Language) format using the `socceraction` library.
2.  **Expected Threat (xT) Model:** A custom xT model is trained on the full tournament dataset to assign a threat value to every location on the pitch.
3.  **Weighted Passing Network Construction:** For each match, a directed graph is built where players are nodes and passes are edges. The edge weights are calculated based on the change in xT and pressure bonuses.
4.  **Weighted PageRank (WPR) Calculation:** A custom-built PageRank algorithm is run on the weighted adjacency matrix of the passing network to calculate each player's influence score for that match.
5.  **Cross-Match Normalization (Z-Scores):** To compare player performances across different matches and contexts, raw WPR scores are converted to Z-scores, which measure how many standard deviations a player's performance was from the match average.
6.  **Positional Analysis:** Player position data is integrated to analyze the results, identifying top performers in each role and highlighting versatile players.

## Results & Visualizations

The final output is a ranked list of all players in the tournament based on their average WPR Z-score. The analysis reveals key influencers who may not always top traditional stats leaderboards.

#### Top 10 Ranked Players (WWC 2023)

| Rank | Player | Team | Average Z-Score | Primary Position |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Khadija Monifa Shaw | Jamaica | 3.02 | Forward |
| 2 | Barbra Banda | Zambia | 2.79 | Forward |
| 3 | Thị Thảo Thái | Vietnam | 2.53 | Defensive Midfielder|
| 4 | K. Rivera Guillou | Philippines | 2.42 | Central Midfielder |
| 5 | Pernille Harder | Denmark | 2.37 | Attacking Midfielder|
| ... | ... | ... | ... | ... |

*(This table can be extended with your final results)*

---

## Repository Structure

```
.
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
│
├── data/
│   ├── .gitkeep
│   └── README.md  <-- Explains where to get data
│
├── notebooks/
│   ├── 01_socceraction_data_conversion.ipynb
│   ├── 02_xt_model_training.ipynb
│   ├── 03_wpr_core_processing.ipynb
│   └── 04_final_analysis.ipynb
│
└── src/
    ├── __init__.py
    ├── data_processing.py
    └── pagerank_calculator.py
```

---

## Setup and Usage

To run this project locally, please follow these steps.

### 1. Prerequisites
- Git
- Python 3.9+

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 3. Set Up the Data (Crucial)
This repository **does not** contain the raw StatsBomb data, as its redistribution is not permitted. You must download it yourself.

1.  Go to the [StatsBomb/open-data](https://github.com/statsbomb/open-data) repository.
2.  Download the data for the **2023 FIFA Women's World Cup**.
3.  Create a `data/` folder in the root of this project.
4.  Place the downloaded data into the `data/` folder, maintaining the following structure:
    ```
    data/
    └── wwc2023/
        ├── events/
        │   ├── 3893787.json
        │   └── ... (all other event files)
        └── lineups/
            ├── 3893787.json
            └── ... (all other lineup files)
    ```
5.  The derived xT grid and final CSVs are included in this repository for convenience.

### 4. Install Dependencies
It is recommended to use a virtual environment.
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the required libraries
pip install -r requirements.txt
```

### 5. Run the Notebooks
The analysis is split across several notebooks. Please run them in the following order:
1.  `notebooks/01_socceraction_data_conversion.ipynb` - To convert raw JSON data into the SPADL format.
2.  `notebooks/02_xt_model_training.ipynb` - To train the Expected Threat model.
3.  `notebooks/03_wpr_core_processing.ipynb` - To build the passing networks and run the WPR algorithm.
4.  `notebooks/04_final_analysis.ipynb` - To perform Z-score normalization and positional analysis.

---

## Acknowledgements & Data Source

*   This project uses open data provided by **StatsBomb**. All data is managed and accessed via the [StatsBomb/open-data](https://github.com/statsbomb/open-data) repository and is subject to their user agreement. A huge thank you to StatsBomb for making this data available to the public.
*   This project utilizes the [socceraction](https://github.com/ML-KULeuven/socceraction) library for handling event stream data. The library is licensed under the MIT License.

## License

The original code in this repository is licensed under the [MIT License](LICENSE).
