"""
Test cases for PS 9 - Placement Data Analyzer (one.py)

Runs the four given test cases automatically and checks the program output.
Usage:  python test_cases.py -v
"""

import os
import io
import sys
import builtins
import tempfile
import unittest
import contextlib
import importlib.util

os.environ.setdefault("MPLBACKEND", "Agg")   # no chart windows during tests

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("one", os.path.join(HERE, "one.py"))
one = importlib.util.module_from_spec(spec)
spec.loader.exec_module(one)


def run_program(rows, answers):
    """Write placement.csv, feed menu answers, return the console output."""
    folder = tempfile.mkdtemp()
    path = os.path.join(folder, "placement.csv")
    with open(path, "w") as f:
        f.write("\n".join(rows) + "\n")

    answers = list(answers)
    buffer = io.StringIO()
    old_input, old_argv, old_show = builtins.input, sys.argv, one.plt.show
    builtins.input = lambda prompt="": answers.pop(0)
    sys.argv = ["one.py", path]
    one.plt.show = lambda: one.plt.close("all")
    try:
        with contextlib.redirect_stdout(buffer):
            one.main()
    finally:
        builtins.input, sys.argv, one.plt.show = old_input, old_argv, old_show
    return buffer.getvalue()


BASE_ROWS = ["Aman,CSE,TCS,6", "Riya,CSE,Infosys,8", "Karan,ECE,Wipro,4"]


class TestPlacementAnalyzer(unittest.TestCase):

    def test_1_normal_input(self):
        out = run_program(BASE_ROWS, ["1", "3"])
        self.assertIn("Total placed: 3 | Average package: 6.00 LPA", out)
        self.assertIn("Highest: 8.00 LPA (Riya, Infosys)", out)

    def test_2_boundary_minimum_input(self):
        out = run_program(["Neha,CSE,TCS,3.5"], ["1", "3"])
        self.assertIn("Total placed: 1 | Average package: 3.50 LPA", out)
        self.assertIn("Highest: 3.50 LPA (Neha, TCS)", out)

    def test_3_invalid_input(self):
        rows = ["Aman,CSE,TCS,abc", "Riya,CSE,Infosys,8", "Karan,ECE,Wipro,-4"]
        out = run_program(rows, ["1", "3"])
        self.assertIn("Row 1 skipped: invalid Package 'abc'.", out)
        self.assertIn("Row 3 skipped: Package must be positive.", out)
        self.assertIn("Valid records: 1", out)
        self.assertIn("Total placed: 1 | Average package: 8.00 LPA", out)

    def test_4_different_valid_scenario(self):
        rows = BASE_ROWS + ["Ravi,ECE,Accenture,12"]
        out = run_program(rows, ["2", "7", "3"])
        self.assertIn("Placements: CSE: 2 | ECE: 2", out)
        self.assertIn("Average package: CSE 7.00 | ECE 8.00", out)
        self.assertIn("Above 7 LPA: Riya (8.00) | Ravi (12.00)", out)
        self.assertIn("Pie chart 'Branch-wise Placements' displayed", out)


if __name__ == "__main__":
    unittest.main()
