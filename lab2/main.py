#!/usr/bin/env python3
"""CLI for system function: compute and export to CSV."""

import argparse
import sys
from pathlib import Path

# Add lab2 to path for imports
lab2_dir = Path(__file__).parent
sys.path.insert(0, str(lab2_dir))

from src.system.system_function import SystemFunction
from src.csv_export import export_to_csv


def main():
    parser = argparse.ArgumentParser(description="System function: compute and export to CSV")
    parser.add_argument("--x-start", type=float, default=-2.0, help="Start of x range")
    parser.add_argument("--x-end", type=float, default=2.0, help="End of x range")
    parser.add_argument("--step", type=float, default=0.1, help="Step for x")
    parser.add_argument("--output", "-o", type=str, default="output.csv", help="Output CSV path")
    parser.add_argument("--delimiter", type=str, default=",", help="CSV delimiter")
    parser.add_argument("--include-undefined", action="store_true", help="Include undefined points in CSV")
    args = parser.parse_args()

    system = SystemFunction()
    count = export_to_csv(
        system,
        x_start=args.x_start,
        x_end=args.x_end,
        step=args.step,
        path=args.output,
        delimiter=args.delimiter,
        skip_undefined=not args.include_undefined,
    )
    print(f"Exported {count} rows to {args.output}")


if __name__ == "__main__":
    main()
