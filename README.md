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
