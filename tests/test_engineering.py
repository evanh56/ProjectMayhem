import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ProjectMayhem"


def load_main():
    spec = importlib.util.spec_from_file_location("pm_main", SOURCE / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EngineeringChecks(unittest.TestCase):
    def test_main_imports_without_mt5(self):
        sys.modules.pop("MetaTrader5", None)
        module = load_main()
        self.assertTrue(hasattr(module, "connect_broker"))

    def test_incremental_write_appends_one_row(self):
        module = load_main()
        frame = pd.DataFrame({"time": pd.to_datetime(["2025-01-01 00:00", "2025-01-01 00:15"]), "open": [1, 2], "high": [2, 3], "low": [0, 1], "close": [1.5, 2.5]})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            module.write_15m(frame, path, initial_run_complete=False)
            module.write_15m(frame, path, initial_run_complete=True)
            lines = path.read_text().splitlines()
            self.assertEqual(len(lines), 4)
            self.assertEqual(lines[0], "Date,Open,High,Low,Close")
            self.assertEqual(lines[-1].split(",")[0], "2025-01-01 00:15:00")

    def test_empty_incremental_input_writes_nothing(self):
        module = load_main()
        frame = pd.DataFrame(columns=["time", "open", "high", "low", "close"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            module.write_15m(frame, path, initial_run_complete=True)
            self.assertFalse(path.exists())

    def test_no_credential_literal_in_project_source(self):
        forbidden = ("5057709180", "Q-Fe7aBa", "MetaQuotes-Demo")
        for path in SOURCE.glob("*.py"):
            text = path.read_text()
            self.assertFalse(any(value in text for value in forbidden), path.name)


if __name__ == "__main__":
    unittest.main()
