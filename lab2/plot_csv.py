#!/usr/bin/env python3
"""Build plots from CSV export for the report. Requires matplotlib."""

import argparse
import csv
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Install matplotlib: pip install matplotlib")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", nargs="?", default="output.csv", help="CSV file path")
    parser.add_argument("-o", "--output", default="plot.png", help="Output plot path")
    args = parser.parse_args()

    xs, ys = [], []
    with open(args.csv_file, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # header
        for row in reader:
            try:
                x, y = float(row[0]), float(row[1])
                xs.append(x)
                ys.append(y)
            except (ValueError, IndexError):
                pass

    plt.figure(figsize=(10, 6))
    plt.plot(xs, ys, "b-", linewidth=1)
    plt.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
    plt.xlabel("X")
    plt.ylabel("Result")
    plt.title("System function: trig (x<=0) and log (x>0)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(args.output, dpi=150)
    print(f"Saved plot to {args.output}")


if __name__ == "__main__":
    main()
