"""Pytest configuration: add lab2 to path."""
import sys
from pathlib import Path

lab2 = Path(__file__).parent
if str(lab2) not in sys.path:
    sys.path.insert(0, str(lab2))
