# Test

- [x] Implement metrics/spectral.py (L, Lsym, Lrw + lambda2, lambda_n, lambda_n/lambda2, optional Kirchhoff).
- [ ] Implement metrics/robustness.py (GCC fraction, components count, avg shortest path in GCC).
- [ ] Implement attacks/node_attacks.py (random, degree, betweenness, Fiedler-magnitude).
- [ ] Build experiments/run_single.py to run one graph/attack and write CSV.
- [ ] Add experiments/sweep.py for batch runs.
- [ ] Plotting script.

```bash
python experiments/run_single.py --graph erdos_renyi --attack random --n 200 --p 0.03 --num-steps 25 --seed 42 --out results/er.csv
python experiments/run_single.py --graph small_world --attack degree --n 300 --k 6 --p 0.1 --num-steps 30 --out results/sw_degree.csv
python experiments/run_single.py --graph scale_free --attack fiedler --n 300 --m 3 --num-steps 30 --out results/sf_fiedler.csv
```

Notes

- For directed graphs, --kind controls component logic; defaults to weak.
- random attack uses --seed. Others are deterministic.
