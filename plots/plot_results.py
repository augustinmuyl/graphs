"""Plot CSV results from experiments/run_single.py."""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


DEFAULT_X = "removed_fraction"
DEFAULT_Y = "gcc_fraction"


def _load_series(path, x_col, y_col):
    xs = []
    ys = []
    with Path(path).open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if x_col not in row or y_col not in row:
                raise ValueError(
                    f"Missing columns in {path}: required '{x_col}' and '{y_col}'."
                )
            xs.append(float(row[x_col]))
            ys.append(float(row[y_col]))

    if not xs:
        raise ValueError(f"No data rows found in {path}.")

    order = sorted(range(len(xs)), key=lambda i: xs[i])
    xs = [xs[i] for i in order]
    ys = [ys[i] for i in order]
    return xs, ys


def main():
    parser = argparse.ArgumentParser(description="Plot experiment CSV results.")
    parser.add_argument("--inputs", nargs="+", required=True, help="CSV files to plot")
    parser.add_argument("--labels", nargs="+", default=None, help="Optional labels")
    parser.add_argument("--x", dest="x_col", default=DEFAULT_X)
    parser.add_argument("--y", dest="y_col", default=DEFAULT_Y)
    parser.add_argument("--title", default=None)
    parser.add_argument("--out", default=None, help="Output image path (e.g., plot.png)")

    args = parser.parse_args()

    if args.labels is not None and len(args.labels) != len(args.inputs):
        raise ValueError("If provided, --labels must match number of --inputs.")

    for i, path in enumerate(args.inputs):
        xs, ys = _load_series(path, args.x_col, args.y_col)
        label = args.labels[i] if args.labels else Path(path).stem
        plt.plot(xs, ys, label=label)

    plt.xlabel(args.x_col)
    plt.ylabel(args.y_col)
    if args.title:
        plt.title(args.title)
    if len(args.inputs) > 1:
        plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path, dpi=200)
    else:
        plt.show()


if __name__ == "__main__":
    main()
