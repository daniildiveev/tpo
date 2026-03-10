"""Integration tests: full path from x to result, CSV export."""

import csv
import tempfile
from pathlib import Path

import pytest

from src.system.system_function import SystemFunction
from src.csv_export import export_to_csv


class TestFullIntegration:
    def test_trig_branch_full_flow(self):
        sys_fn = SystemFunction()
        for x in [-0.5, -1.0, -2.0]:
            result = sys_fn.compute(x)
            assert isinstance(result, float)
            assert not (result != result)  # not NaN

    def test_log_branch_full_flow(self):
        sys_fn = SystemFunction()
        for x in [0.5, 2.0, 10.0]:
            result = sys_fn.compute(x)
            assert isinstance(result, float)
            assert not (result != result)

    def test_csv_export_creates_file(self):
        sys_fn = SystemFunction()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            path = f.name
        try:
            count = export_to_csv(sys_fn, x_start=-1.0, x_end=1.0, step=0.2, path=path)
            assert count > 0
            with open(path, newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)
            assert rows[0] == ["X", "Result"]
            assert len(rows) >= 2
        finally:
            Path(path).unlink(missing_ok=True)

    def test_csv_export_custom_delimiter(self):
        sys_fn = SystemFunction()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            path = f.name
        try:
            export_to_csv(
                sys_fn, x_start=2.0, x_end=3.0, step=0.5, path=path, delimiter=";"
            )
            with open(path, newline="") as f:
                content = f.read()
            assert ";" in content
        finally:
            Path(path).unlink(missing_ok=True)

    def test_csv_export_configurable_step(self):
        sys_fn = SystemFunction()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            path = f.name
        try:
            count_fine = export_to_csv(
                sys_fn, x_start=2.0, x_end=3.0, step=0.1, path=path
            )
            count_coarse = export_to_csv(
                sys_fn, x_start=2.0, x_end=3.0, step=0.5, path=path
            )
            assert count_fine > count_coarse
        finally:
            Path(path).unlink(missing_ok=True)
