# Applications of the Laplacian Matrix of Graphs

Goal: Investigate how the spectrum of a graph Laplacian relates to network robustness under
random failures and targeted attacks.

## Run a single experiment

`experiments/run_single.py` runs one graph generator + one attack strategy and writes a CSV
with robustness and spectral metrics.

Example: Erdos-Renyi graph under random failures (defaults shown):
```bash
python experiments/run_single.py \
  --graph erdos_renyi \
  --attack random \
  --n 100 \
  --p 0.05 \
  --out results/er_random.csv
```

Example: Small-world graph under degree attack with coarser checkpoints:
```bash
python experiments/run_single.py \
  --graph small_world \
  --attack degree \
  --n 200 \
  --k 6 \
  --p 0.1 \
  --num-steps 25 \
  --out results/sw_degree.csv
```

Key options:
- `--graph`: `complete`, `erdos_renyi`, `small_world`, `scale_free`
- `--attack`: `random`, `degree`, `betweenness`, `fiedler`
- `--n`, `--p`, `--k`, `--m`: graph parameters (vary by generator)
- `--num-steps`: number of removal checkpoints (default: all nodes)
- `--kind`: component definition for directed graphs (`weak`, `strong`, `undirected`)
- `--out`: output CSV path

## Plot results

`plots/plot_results.py` plots one or more CSVs (produced by `run_single.py`).

Example: Plot giant component size vs removed fraction:
```bash
python plots/plot_results.py \
  --inputs results/er_random.csv \
  --x removed_fraction \
  --y gcc_fraction \
  --title "ER Random Attack" \
  --out results/er_random.png
```

Example: Compare multiple attacks:
```bash
python plots/plot_results.py \
  --inputs results/er_random.csv results/er_degree.csv \
  --labels random degree \
  --x removed_fraction \
  --y gcc_fraction \
  --title "ER Attacks" \
  --out results/er_attacks.png
```

Notes:
- If `--out` is omitted, the plot opens in a window.
- Default columns are `removed_fraction` (x) and `gcc_fraction` (y).

## Experiment One: Erdos-Renyi Graphs and Random Failures/Attacks
This report summarizes the ER experiment results in `results/data/er.csv` and the plots in `results/plots`. The dataset contains 201 removal checkpoints for a single Erdos-Renyi graph with inferred size `n=200` (from `removed_nodes + gcc_size`). Spectral metrics are computed on the GCC and are missing for 9 checkpoints where the GCC becomes too small.

**Experiment Setup (from `results/data/er.csv`)**
- Graph family: Erdos-Renyi (single instance, `n=200`, parameters not recorded in the CSV).
- Failure/attack model: node removals in increasing fractions `removed_fraction` from 0.0 to 1.0 (201 checkpoints).
- Robustness metrics: `gcc_fraction`, `gcc_size`, `num_components`, `avg_shortest_path_gcc`.
- Spectral metrics on GCC: `algebraic_connectivity_gcc`, `spectral_gap_ratio_gcc`, `kirchhoff_index_gcc`.

**Core Robustness Outcomes**
- The GCC shrinks steadily as removal fraction increases and collapses near full removal. This is shown in `results/plots/er_gcc_fraction.png`.
- Fragmentation (number of components) increases with removal fraction, as shown in `results/plots/er_num_components.png`.
- The average shortest path within the GCC grows as removals increase, indicating that the remaining giant component becomes less efficient, shown in `results/plots/er_avg_shortest_path_gcc.png`.

**Spectral Behavior Across Removals**
- Algebraic connectivity of the GCC drops as removals progress (`results/plots/er_algebraic_connectivity_gcc.png`), reflecting weaker internal connectivity within the GCC.
- Kirchhoff index evolves strongly with GCC size and fragmentation (`results/plots/er_kirchhoff_index_gcc.png` and `results/plots/er_compare_gcc_fraction_vs_kirchhoff.png`).

**Correlation Analysis (Pearson r, n=192 paired points)**
These correlations quantify how well each spectral indicator tracks robustness outcomes in this ER dataset.

| Spectral Metric | Robustness Metric | Pearson r |
| --- | --- | --- |
| kirchhoff_index_gcc | gcc_fraction | 0.981 |
| kirchhoff_index_gcc | gcc_size | 0.981 |
| kirchhoff_index_gcc | num_components | -0.964 |
| spectral_gap_ratio_gcc | avg_shortest_path_gcc | 0.770 |
| algebraic_connectivity_gcc | avg_shortest_path_gcc | -0.712 |
| kirchhoff_index_gcc | avg_shortest_path_gcc | 0.429 |
| spectral_gap_ratio_gcc | gcc_fraction | -0.220 |
| spectral_gap_ratio_gcc | gcc_size | -0.220 |
| algebraic_connectivity_gcc | num_components | -0.191 |
| algebraic_connectivity_gcc | gcc_fraction | 0.164 |
| algebraic_connectivity_gcc | gcc_size | 0.164 |
| spectral_gap_ratio_gcc | num_components | 0.096 |

**Key Conclusions Supported by the Data**
- The Kirchhoff index is the strongest spectral proxy for GCC size and fragmentation in this experiment (very strong correlations with `gcc_fraction`, `gcc_size`, and `num_components`). This supports using Kirchhoff index as a stability indicator for ER robustness under random removals.
- Algebraic connectivity (λ2) is a strong indicator of path efficiency inside the GCC rather than GCC size. It correlates strongly with `avg_shortest_path_gcc` but only weakly with `gcc_fraction`/`gcc_size`.
- Spectral gap ratio is also strongly tied to path efficiency but is a weak predictor of GCC size/fragmentation in this dataset.
- In this ER run, “robustness” splits into two different behaviors:
  - **Connectivity of the GCC** (captured by λ2 and spectral gap ratio).
  - **Existence/size of the GCC** (captured best by Kirchhoff index).

**Plots Included**
GCC robustness over removals:
- `results/plots/er_gcc_fraction.png`
- `results/plots/er_num_components.png`
- `results/plots/er_avg_shortest_path_gcc.png`

Spectral metrics over removals:
- `results/plots/er_algebraic_connectivity_gcc.png`
- `results/plots/er_kirchhoff_index_gcc.png`
- `results/plots/er.png`

Spectral-vs-robustness relationships (new):
- `results/plots/er_scatter_kirchhoff_vs_gcc_fraction.png`
- `results/plots/er_scatter_algebraic_connectivity_vs_avg_shortest_path.png`
- `results/plots/er_scatter_spectral_gap_ratio_vs_avg_shortest_path.png`

**Figure Gallery**
![](results/plots/er_gcc_fraction.png)
![](results/plots/er_num_components.png)
![](results/plots/er_avg_shortest_path_gcc.png)
![](results/plots/er_algebraic_connectivity_gcc.png)
![](results/plots/er_kirchhoff_index_gcc.png)
![](results/plots/er.png)
![](results/plots/er_compare_gcc_fraction_vs_kirchhoff.png)
![](results/plots/er_scatter_kirchhoff_vs_gcc_fraction.png)
![](results/plots/er_scatter_algebraic_connectivity_vs_avg_shortest_path.png)
![](results/plots/er_scatter_spectral_gap_ratio_vs_avg_shortest_path.png)
