import ast
import csv
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ProjectMayhem"
EXCLUDED = {".venv", "venv", "__pycache__", ".git", "__MACOSX"}


def source_files():
    return sorted(p for p in SOURCE.rglob("*.py")
                  if not EXCLUDED.intersection(p.relative_to(SOURCE).parts))


class SourceChecks(unittest.TestCase):
    def test_python_source_has_valid_syntax(self):
        files = source_files()
        self.assertTrue(files, "No Python source found under ProjectMayhem/")
        for path in files:
            with self.subTest(file=str(path.relative_to(ROOT))):
                ast.parse(path.read_bytes(), filename=str(path.relative_to(ROOT)))


class FairValueGapChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        matches = [p for p in source_files() if p.name == "FairValueGap.py"]
        if len(matches) != 1:
            raise RuntimeError(f"Expected one FairValueGap.py; found {len(matches)}")
        spec = importlib.util.spec_from_file_location("fvg_under_test", matches[0])
        cls.fvg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.fvg)

    def setUp(self):
        self.previous_directory = Path.cwd()
        self.workspace = tempfile.TemporaryDirectory()
        os.chdir(self.workspace.name)

    def tearDown(self):
        os.chdir(self.previous_directory)
        self.workspace.cleanup()

    def detect(self, candles):
        with open("GBPUSD_15m_Data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Open", "High", "Low", "Close"])
            for index, prices in enumerate(candles):
                writer.writerow([f"2025-01-01 00:{index * 15:02d}:00", *prices])
        with open("FairValueGap_15m.csv", "w", newline="") as file:
            csv.writer(file).writerow(["Date", "Prev_candle", "Next_candle", "Position"])
        self.fvg.search_for_fvg()
        with open("FairValueGap_15m.csv", newline="") as file:
            return list(csv.DictReader(file))

    @staticmethod
    def bullish_candles():
        return [[199.0, 199.2, 198.9, 199.1],
                [199.3, 199.9, 199.25, 199.8],
                [199.9, 200.0, 199.85, 199.95]]

    def test_detects_bullish_gap(self):
        rows = self.detect(self.bullish_candles())
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Position"], "Bullish")
        self.assertAlmostEqual(float(rows[0]["Prev_candle"]), 199.2)
        self.assertAlmostEqual(float(rows[0]["Next_candle"]), 199.85)

    def test_detects_bearish_gap(self):
        candles = [[400-o, 400-low, 400-high, 400-close]
                   for o, high, low, close in self.bullish_candles()]
        rows = self.detect(candles)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Position"], "Bearish")
        self.assertAlmostEqual(float(rows[0]["Prev_candle"]), 200.8)
        self.assertAlmostEqual(float(rows[0]["Next_candle"]), 200.15)

    def test_rejects_overlapping_outer_candles(self):
        candles = self.bullish_candles()
        candles[2][2] = 199.1
        self.assertEqual(self.detect(candles), [])

    def test_removes_gap_after_later_boundary_breach(self):
        candles = self.bullish_candles()
        candles.append([199.9, 200.0, 199.1, 199.3])
        self.assertEqual(self.detect(candles), [])


if __name__ == "__main__":
    unittest.main()
