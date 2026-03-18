import csv
from pathlib import Path
from typing import Union

from .system.system_function import SystemFunction, DomainError


def export_to_csv(
    system_func: SystemFunction,
    x_start: float,
    x_end: float,
    step: float,
    path: Union[str, Path],
    delimiter: str = ",",
    skip_undefined: bool = True,
) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(["X", "Result"])

        x = x_start
        while (step > 0 and x <= x_end) or (step < 0 and x >= x_end):
            try:
                result = system_func.compute(x)
                writer.writerow([x, result])
                count += 1
            except DomainError:
                if not skip_undefined:
                    writer.writerow([x, "undefined"])
                    count += 1
            x += step

    return count
