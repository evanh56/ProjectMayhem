# Inspection record

## Repository and branch

- **Repository URL:** `https://github.com/evanh56/ProjectMayhem`
- **Owner:** `evanh56`
- **Repository:** `ProjectMayhem`
- **Branch inspected:** `main`
- **Main branch head SHA returned by GitHub:** `8feb36db91d7144b4a190a302634ddd30c449c0b`
- **Repository access:** readable through GitHub read actions.
- **`main` branch protection:** returned as disabled/unprotected.

## Access check — exact GitHub action results

### 1. Read `ProjectMayhem/main.py` on `main`

**Action:** `github_get_repository_content`  
**Parameters:** owner `evanh56`, repository `ProjectMayhem`, ref `main`, path `ProjectMayhem/main.py`

**Result:** success. GitHub returned:

- path: `ProjectMayhem/main.py`
- blob SHA: `3f9cec66a27161dd329cf9f18e665182b60bd18e`
- size: `14684`
- encoding: `base64`
- readable file content
- raw URL: `https://raw.githubusercontent.com/evanh56/ProjectMayhem/main/ProjectMayhem/main.py`

The returned source contains MT5 login code, hard-coded account values, `symbol = 'GBPJPY'`, MT5 candle retrieval, CSV writers, scheduling, and entry-point calls.

### 2. Get branch `main`

**Action:** `github_get_a_branch`  
**Parameters:** owner `evanh56`, repository `ProjectMayhem`, branch `main`

**Result:** success.

- Branch: `main`
- Head commit SHA: `8feb36db91d7144b4a190a302634ddd30c449c0b`
- Commit message: `Merge pull request #2 from evanh56/improvement/offline-foundation-v1`
- Commit timestamp: `2026-10-21T23:38:31Z`

### 3. Get branch `fix/offline-testability-m15-append`

**Action:** `github_get_a_branch`  
**Parameters:** owner `evanh56`, repository `ProjectMayhem`, branch `fix/offline-testability-m15-append`

**Result:** success; branch exists.

- Branch: `fix/offline-testability-m15-append`
- Head commit SHA: `8c33a68fb5c46c510170050c5262c8ef74dfa020`
- Commit message: `Add Project Mayhem audit handoffs and consolidated report`
- Commit timestamp: `2026-10-21T00:00:00Z`

### 4. List workflow runs for `.github/workflows/offline-tests.yml` on `main`

**Action:** `github_list_workflow_runs_for_a_workflow`  
**Parameters:** owner `evanh56`, repository `ProjectMayhem`, workflow `.github/workflows/offline-tests.yml`, branch `main`, pull-request runs excluded

**Result:** success. GitHub returned one run.

Most recent run:

| Field | Returned value |
|---|---|
| Run ID | `39128978458` |
| Status | `completed` |
| Conclusion | `success` |
| Head SHA | `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8` |
| Created | `2026-10-18T12:50:34Z` |
| Started | `2026-10-18T12:50:34Z` |
| Updated | `2026-10-18T12:50:58Z` |
| Event | `workflow_dispatch` |
| Head branch | `main` |
| Workflow | `Project Mayhem Offline Tests` |
| Run number | `1` |

This is real GitHub Actions evidence and is separate from any owner-pasted log or document summary.

### Artifacts for run `39128978458`

**Action:** `github_list_workflow_run_artifacts`

**Result:** success.

```text
artifacts: []
total_count: 0
```

No artifacts were returned.

### Logs for run `39128978458`

**Action:** `github_download_workflow_run_logs`

**Result:** success. GitHub returned a downloadable ZIP archive descriptor:

- MIME type: `application/zip`
- archive name: `evanh56_ProjectMayhem_run_39128978458_logs.zip`
- a temporary download URL was returned

Therefore, the run logs could be downloaded. The log contents were not read in this inspection.

## Full repository tree

**Action:** `github_get_a_tree`  
**Parameters:** owner `evanh56`, repository `ProjectMayhem`, tree ref `main`, recursive `true`

**Result:** success. The tree was not truncated.

Root folders returned:

- `.github/`
- `ProjectMayhem/`
- `docs/`
- `reports/`
- `research/`
- `skills/`
- `tests/`

Root files returned:

- `requirements-ci.txt`

The tree also returned `ProjectMayhem/__pycache__/`, which was skipped as cache content.

Notable files returned include:

- `.github/workflows/offline-tests.yml`
- `ProjectMayhem/main.py`
- `ProjectMayhem/Execution.py`
- `ProjectMayhem/FairValueGap.py`
- `ProjectMayhem/OrderBlockAnalysis.py`
- `ProjectMayhem/Liquidity.py`
- `ProjectMayhem/Strategy.py`
- seven CSV files under `ProjectMayhem/`
- `tests/test_offline.py`
- `docs/project_overview.md`
- `docs/Strategy.txt`
- `docs/data_dictionary.md`
- `docs/decision_log.md`
- `docs/experiment_log.md`
- `docs/risk_policy.md`
- `docs/strategy_specification.md`

The tree confirms that the application source is directly under `ProjectMayhem/`; no `src/` directory was returned.

## Workflow contents

**File:** `.github/workflows/offline-tests.yml`  
**GitHub result:** success; file exists and was readable.  
**Blob SHA:** `d6f84f1c1b389febcfee3700921a09317c74a6a6`

Decoded content:

```yaml
name: Project Mayhem Offline Tests

on:
  workflow_dispatch:
  push:
    branches:
      - improvement/offline-foundation-v1
    paths:
      - 'ProjectMayhem/**'
      - 'tests/**'
      - 'requirements-ci.txt'
      - '.github/workflows/offline-tests.yml'

permissions:
  contents: read

concurrency:
  group: project-mayhem-offline-tests
  cancel-in-progress: false

jobs:
  offline-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: Check out repository
        uses: actions/checkout@v6
        with:
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: '3.11'

      - name: Create report directory
        run: mkdir -p reports/ci

      - name: Record tested revision
        shell: bash
        run: |
          git rev-parse HEAD > reports/ci/commit.txt
          python --version > reports/ci/python-version.txt

      - name: Install test dependencies
        run: python -m pip install --disable-pip-version-check -r requirements-ci.txt

      - name: Record installed dependencies
        run: python -m pip freeze > reports/ci/dependencies.txt

      - name: Run offline tests
        shell: bash
        run: |
          set -o pipefail
          python -m unittest discover -s tests -p 'test_offline.py' -v 2>&1 | tee reports/ci/test-results.txt

      - name: Upload test evidence
        if: always()
        uses: actions/upload-artifact@v6
        with:
          name: project-mayhem-offline-results-${{ github.run_id }}-${{ github.run_attempt }}
          path: reports/ci/
          retention-days: 1
          if-no-files-found: warn
```

### Workflow observations

- Triggers:
  - manual `workflow_dispatch`
  - `push` only on branch `improvement/offline-foundation-v1`
  - path filters cover `ProjectMayhem/**`, `tests/**`, `requirements-ci.txt`, and the workflow itself
- Python version: `3.11`
- Runner: `ubuntu-latest`
- Timeout: five minutes
- Inputs: no `workflow_dispatch.inputs` block is present; the workflow accepts no declared inputs.
- Permissions: `contents: read`
- Dependencies are installed from `requirements-ci.txt`.
- Tests run with Python’s built-in `unittest` discovery.
- Test output is written to `reports/ci/test-results.txt`.
- Installed dependencies and revision information are written to `reports/ci/`.
- Artifacts are configured for upload with `if: always()`.
- The retrieved real run nevertheless returned zero artifacts.

## `requirements-ci.txt`

**File:** `requirements-ci.txt`  
**GitHub result:** success; file exists and was readable.  
**Blob SHA:** `a1e6c0bf859df58865e66aba1d07de3aa4de4f72`

Exact content:

```text
pandas==2.2.3
```

No other project-owned dependency manifest was observed in the returned tree.

## `tests/test_offline.py`

**File:** `tests/test_offline.py`  
**GitHub result:** success; file exists and was readable.  
**Blob SHA:** `6549f1e74e98ac4615b7a3ac347f79342c041382`

Imports returned:

```python
import ast
import csv
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
```

The test file does not import `ProjectMayhem.main`, `Execution`, `Strategy`, `Liquidity`, or `OrderBlockAnalysis`. It dynamically loads `ProjectMayhem/FairValueGap.py` with `importlib.util`.

### Test classes and tests

#### `SourceChecks`

##### `test_python_source_has_valid_syntax`

Evidence:

- Finds Python files below `ProjectMayhem/`.
- Excludes `.venv`, `venv`, `__pycache__`, `.git`, and `__MACOSX`.
- Asserts that at least one Python source file exists.
- Parses every discovered Python source file with `ast.parse`.
- This is a syntax test, not an execution or import test.

#### `FairValueGapChecks`

`setUpClass`:

- Locates exactly one `FairValueGap.py`.
- Loads it dynamically.
- Executes the module loader.

`setUp`:

- Creates a temporary directory.
- Changes the current working directory to that directory.

`tearDown`:

- Restores the prior working directory.
- Removes the temporary directory.

##### `test_detects_bullish_gap`

Creates three candles:

```text
[199.0, 199.2, 198.9, 199.1]
[199.3, 199.9, 199.25, 199.8]
[199.9, 200.0, 199.85, 199.95]
```

Calls the module’s `search_for_fvg()` through the test harness.

Asserts:

- exactly one output row
- output position is `"Bullish"`
- `Prev_candle` is approximately `199.2`
- `Next_candle` is approximately `199.85`

##### `test_detects_bearish_gap`

Builds bearish-oriented candles from the bullish fixture and calls the same detector.

Asserts:

- exactly one output row
- output position is `"Bearish"`
- `Prev_candle` is approximately `200.8`
- `Next_candle` is approximately `200.15`

##### `test_rejects_overlapping_outer_candles`

Modifies the third candle so its low overlaps the relevant gap.

Asserts:

```python
self.assertEqual(self.detect(candles), [])
```

##### `test_removes_gap_after_later_boundary_breach`

Appends a later candle that breaches the gap boundary.

Asserts:

```python
self.assertEqual(self.detect(candles), [])
```

### Functions used from `ProjectMayhem/`

The test directly exercises the `search_for_fvg()` function in:

```text
ProjectMayhem/FairValueGap.py
```

It does not directly call the other application modules.

## Documentation access

### `docs/project_overview.md`

**GitHub result:** success; file exists and was readable.  
**Blob SHA:** `aae09ba3282f59682b310f96123ad7b3206efbfe`

The document states, among other points:

- updated 18 October 2026
- version `0.1`
- the project targets GBPJPY and USDJPY
- intended sequence is hourly context with 15-minute confirmation
- planned initial target is 2R
- intended maximum risk is 2% per trade
- the project is a Python/MT5 prototype, not a verified trading system
- no broker session, live order, paper trade, or profitability test was performed during document preparation
- existing source reflects implemented behavior, not necessarily intended or correct behavior
- source is directly under `ProjectMayhem/` in the actual tree, despite legacy `src/ProjectMayhem/` references in the document
- an isolated offline harness and dependency manifest are required before application execution
- the document records findings F01–F10, including credential exposure, symbol/file mismatch, append concerns, possible `NameError`, confirmation indexing, scheduling, look-ahead effects, and missing execution/testing evidence

## Source files inspected

All requested source files were readable through GitHub actions.

### `ProjectMayhem/main.py`

Observed imports:

```python
import csv
import MetaTrader5 as mt
from datetime import datetime, timezone
import pandas as pd
import pytz
import time
import tzlocal
import threading

import Execution as ex
import FairValueGap as fvg
import OrderBlockAnalysis as ob
import Liquidity as lqt
import Strategy as s
```

Observed module-level broker credentials and connection:

- module-level `login`
- module-level `password`
- module-level `server`
- module-level call to `mt.login(login, password, server)`

Credential values are not reproduced here. Their location is:

```text
ProjectMayhem/main.py
```

Observed instrument:

```python
symbol = 'GBPJPY'
```

Observed MT5 timeframes and candle counts:

- M1: one candle
- M15: 192 candles
- H1: 120 candles

Observed MT5 calls include:

- `mt.initialize()`
- `mt.account_info()`
- `mt.copy_rates_from_pos(...)`
- `mt.symbol_select(...)`
- `mt.symbol_info_tick(...)`
- `mt.shutdown()`
- `mt.login(...)`

Observed candle handling:

- MT5 timestamps are converted with `pd.to_datetime(..., unit='s', utc=True)`.
- They are converted to `Europe/London` with `pytz`.
- Timezone information is then stripped with `.dt.tz_localize(None)`.
- Retrieval starts at position `0`, so the current/latest candle may be included.
- No explicit completed-candle filtering was observed.

Observed entry points/functions:

- `MT5_account()`
- `check_system_timezone()`
- `get_candle_1m(...)`
- `get_candles_15m(...)`
- `get_candles_1hr(...)`
- `data_1m()`
- `write_1m(...)`
- `data_15m()`
- `write_15m(...)`
- `FairValueGap()`
- `OrderBlock_15m()`
- `Liquidity()`
- `data_1Hr()`
- `write_1hr(...)`
- `OrderBlock_1hr()`
- `initialise(...)`
- `check_1m()`
- `check_15m()`
- `check_1hr()`
- `should_run_now(...)`
- `run_scheduler()`
- `main()`

The `main()` function:

- calls `MT5_account()`
- runs initial M1, M15, and H1 checks
- starts the scheduler
- eventually calls `mt.shutdown()`
- calls `check_1m()` and `s.main()` after the scheduler block

The file ends with:

```python
if __name__ == '__main__':
    main()
```

The module-level `mt.login(...)` occurs before that guard, so importing the module has broker-side effects.

### `ProjectMayhem/FairValueGap.py`

Functions:

- `add_fvg(FairValueGap)`
- `check_fvg(FairValueGap, pos, loc)`
- `search_for_fvg()`
- `main()`

Observed detection formulas:

Bullish candidate:

```python
current['Open'] - current['Close'] < 0
prev['High'] < current['Close']
next['Low'] > current['Open']
next['High'] - prev['Low'] > 0.00005
```

The output stores:

- `Date`: current candle date
- `Prev_candle`: previous candle high
- `Next_candle`: next candle low
- `Position`: `"Bullish"`

Bearish candidate:

```python
current['Open'] - current['Close'] > 0
prev['Low'] > current['Close']
next['High'] < current['Open']
prev['Low'] - next['High'] > 0.00005
```

The output stores:

- `Date`: current candle date
- `Prev_candle`: previous candle low
- `Next_candle`: next candle high
- `Position`: `"Bearish"`

The later invalidation scan checks later rows and rejects a candidate if:

- bullish: later `Close < Next_candle` or later `Low < Next_candle`
- bearish: later `Close > Next_candle` or later `High > Next_candle`

It reads:

```text
GBPUSD_15m_Data.csv
```

and writes:

```text
FairValueGap_15m.csv
```

### `ProjectMayhem/OrderBlockAnalysis.py`

Functions:

- `countRows(counter, data_file)`
- `AddOb(ob_dict, val)`
- `check_prev(prev_row, loc)`
- `Next_candle(next1, next2, loc)`
- `OB_check(OrderBlock, counter, pos, loc, data_file)`
- `Analyse_Data(data_file, val)`
- `main(data_file, val)`

Observed order-block direction formula:

```python
Open - Close > 0
```

is treated as bearish; otherwise bullish.

Observed containment bounds:

```python
ob_open = float(OrderBlock['Open'])
ob_close = float(OrderBlock['Close'])
lo_body = min(ob_open, ob_close)
hi_body = max(ob_open, ob_close)
end_contain = min(pos + 6, counter - 1, len_df - 1)
```

The code scans subsequent candles for containment inside the order-block body.

Observed activation/invalidation:

- Bearish OB:
  - activation when a later high or open exceeds the OB open
  - invalidation when a later low, open, or close falls below the OB open
- Bullish OB:
  - activation when a later low, open, or close falls below the OB open
  - invalidation when a later high, open, or close rises above the OB open

The module writes:

- `OrderBlock_15m.csv` when `val == 0`
- `OrderBlock_1hr.csv` otherwise

It uses later candles and a global counter. The documentation identifies possible look-ahead and indexing concerns.

### `ProjectMayhem/Liquidity.py`

Functions:

- `Add_liq(Liquidity)`
- `check_liq(Liquidity, pos, loc, HrL)`
- `find_liq()`
- `main()`

Observed liquidity candidate thresholds:

For bearish candles:

```python
current['Close'] - current['Low'] > 0.06
```

with liquidity level based on `current['Low']`.

For bullish candles:

```python
current['High'] - current['Close'] > 0.06
```

with liquidity level based on `current['High']`.

A second set of smaller thresholds appears for bullish/bearish candle wick logic:

```python
current['High'] - current['Close'] > 0.00018
current['Close'] - current['Low'] > 0.00018
```

The code uses `HrL` values `"High"` and `"Low"` and checks later candles against the stored liquidity level.

It reads:

```text
GBPUSD_15m_Data.csv
```

and writes:

```text
Liquidity_15m.csv
```

### `ProjectMayhem/Strategy.py`

Functions:

- `check_trading_time(start_time_str, end_time_str)`
- `check_if_in_ob_hr(minute_candle, val)`
- `correct_dir()`
- `check_if_in_fvg()`
- `run_strategy_check()`
- `main()`

Observed session check:

```python
check_trading_time('07:00', '02:00')
```

The function handles a time window crossing midnight by accepting times after the start or before the end.

Observed order-block file choice:

```python
'OrderBlock_1hr.csv' if val == 1 else 'OrderBlock_15m.csv'
```

Observed order-block zone bounds:

- bullish:
  - top = `Close`
  - bottom = `Open`
- bearish:
  - top = `Open`
  - bottom = `Close`

Observed overlap check:

```python
body_fully_inside = (body_bottom >= ob_zone_bottom) and (body_top <= ob_zone_top)
body_overlaps_zone = not (body_top < ob_zone_bottom or body_bottom > ob_zone_top)
```

Observed direction confirmation:

- bullish OB requires a later close below the OB open
- bearish OB requires a later close above the OB open

Observed FVG confirmation:

- bullish position checks current close and low against `Next_candle`
- bearish position checks current open and high against `Next_candle`

The module uses global state:

- `hourly_ob`
- `ob_15m`
- `pos`
- `ob_15`

The documentation identifies incomplete state handling and possible indexing problems.

### `ProjectMayhem/Execution.py`

Functions:

- `price_to_pip(symbol, live_price)`
- `taketrade()`
- `main(candle_of_joy)`

Observed experimental position-sizing formula for JPY and GBPUSD symbols:

```python
acc_bal = mt.account_info().balance
pip_val = acc_bal / 100
pips = 7
pip_unit = pip_val / live_price
lot_size = round(pip_unit * pips, 2)
```

A module-level ticker is set to:

```python
ticker = 'GBPJPY'
```

Observed stop-loss variable:

```python
Sl = 350
```

Observed execution behavior:

```python
def taketrade():
    print("Work in progress")
    return
```

No MT5 order-placement call was returned in this file. No `order_send` call was observed. `main(candle_of_joy)` returns immediately.

Therefore:

- position sizing is experimental and not compliant with the documented 2%-risk policy
- stop/take-profit behavior is not implemented
- order placement is not implemented
- broker execution remains a stub

## Instrument selection and CSV files

The tree returned these CSV files:

```text
ProjectMayhem/Current_Candle_1m_Data.csv
ProjectMayhem/GBPUSD_15m_Data.csv
ProjectMayhem/GBPUSD_1hr_Data.csv
ProjectMayhem/FairValueGap_15m.csv
ProjectMayhem/OrderBlock_15m.csv
ProjectMayhem/OrderBlock_1hr.csv
ProjectMayhem/Liquidity_15m.csv
```

Observed mismatch:

- `main.py` selects `GBPJPY`
- data files are named `GBPUSD_15m_Data.csv` and `GBPUSD_1hr_Data.csv`
- no independent USDJPY stream was returned
- CSV files do not contain a symbol column according to the inspected documentation and source behavior

## MT5 and broker calls

Observed in `ProjectMayhem/main.py`:

- `mt.login(...)`
- `mt.initialize()`
- `mt.account_info()`
- `mt.copy_rates_from_pos(...)`
- `mt.symbol_select(...)`
- `mt.symbol_info_tick(...)`
- `mt.shutdown()`

Observed in `ProjectMayhem/Execution.py`:

- `mt.account_info()`

No returned source contained a working MT5 order-placement call.

## Timestamp and candle handling

Observed:

- MT5 epoch timestamps are parsed as UTC.
- Times are converted to `Europe/London`.
- Timezone metadata is removed before CSV output.
- Current-position retrieval starts at position zero.
- The code does not establish that the latest candle is closed before writing or analysis.
- Stored CSV timestamps therefore lack offset/completion metadata.
- The documented risk/data requirements call for preserving legacy timestamps until provenance is reconciled and for event-time-safe H1/M15 joins.

## Dependency and package observations

Observed project-owned manifest:

```text
requirements-ci.txt
```

Exact content:

```text
pandas==2.2.3
```

Direct runtime imports in the source include:

- `MetaTrader5`
- `pandas`
- `pytz`
- `tzlocal`

Only `pandas` is listed in the CI manifest. The workflow does not install the runtime MT5 dependency.

The repository documentation explicitly states that the bundled virtual environment should not be blindly copied or treated as a reproducible dependency manifest.

## Credential locations

Credential material was returned in:

```text
ProjectMayhem/main.py
```

The file contains module-level login, password, and server assignments and calls `mt.login(...)`.

Credential values are intentionally not reproduced.

Required remediation:

- revoke/rotate any exposed broker credentials
- remove credential literals from source history and working tree
- use environment variables or a secret manager
- prevent broker authentication during imports
- ensure offline tests cannot access broker credentials or MT5

The historical `docs/Strategy.txt` also contains authentication examples/placeholders. No values are reproduced.

## Real workflow evidence versus supplied documentation

### Real GitHub Actions evidence

Retrieved directly from GitHub:

- Run ID: `39128978458`
- Branch: `main`
- Head SHA: `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`
- Status: `completed`
- Conclusion: `success`
- Created: `2026-10-18T12:50:34Z`
- Artifacts: none returned
- Logs: downloadable ZIP returned

### Not merged with that evidence

The supplied document digest says that an offline baseline inspection was completed and describes static findings. That owner-provided/documentary material is not treated as the workflow log and was not merged with the real run evidence above.

The retrieved workflow run is not proof that the current `main` commit was tested: its head SHA differs from the current `main` head SHA.

## Findings

1. **Broker side effect on import**  
   `ProjectMayhem/main.py` performs `mt.login(...)` at module scope.

2. **Credential exposure**  
   Broker credential assignments are present in `ProjectMayhem/main.py`. Values are withheld here. Rotate and remove them.

3. **Instrument/file mismatch**  
   Runtime symbol is `GBPJPY`, while data filenames are `GBPUSD_*`.

4. **No independent USDJPY stream**  
   No USDJPY CSV or symbol-specific stream was returned.

5. **Incomplete dependency declaration**  
   `requirements-ci.txt` contains only `pandas==2.2.3`; runtime source imports additional external packages.

6. **Execution is not implemented**  
   `Execution.py::taketrade()` only prints `"Work in progress"` and returns.

7. **No order-placement evidence**  
   No working MT5 `order_send` path was observed.

8. **Position sizing is not the documented policy**  
   `price_to_pip()` uses balance-derived experimental arithmetic and does not implement current-equity, stop-loss-loss, contract, currency, cost, and broker-constraint checks.

9. **Stop/take-profit behavior is absent**  
   No complete stop-loss/take-profit order construction was returned.

10. **Potential forming-candle use**  
    MT5 retrieval begins at position zero and no closed-candle exclusion was observed.

11. **Timezone provenance loss**  
    Source converts timestamps to London time and strips timezone information before CSV output.

12. **FVG detector uses fixed thresholds**  
    FVG detection uses `0.00005` thresholds and later-row invalidation scans.

13. **Liquidity detector uses fixed thresholds**  
    Liquidity logic uses `0.06` and `0.00018` thresholds.

14. **Order-block logic is stateful and look-ahead-sensitive**  
    It scans later candles for activation/invalidation and writes derived snapshots.

15. **Strategy state is incomplete**  
    `Strategy.py` relies on global state and does not implement a complete order lifecycle.

16. **Offline tests are narrow**  
    Tests cover syntax and FVG behavior only. They do not test MT5 isolation, order placement, sizing, Strategy, Liquidity, or OrderBlockAnalysis.

17. **Current run evidence is historical relative to `main`**  
    The only retrieved run passed at head SHA `ad1e0ee0...`; current `main` is `8feb36db...`.

18. **No artifacts were returned for the successful run**  
    Although artifact upload is configured, GitHub returned `total_count: 0`.

## Capabilities unavailable or not performed

- No workflow dispatch action is available in the supplied tools.
- No workflow re-run action is available.
- No commit, update, delete, push, pull request, or file-writing action was used or is available for this inspection.
- No local code execution action is available.
- No test execution was performed by this inspection.
- No broker connection was made.
- No MT5 initialization or authentication was performed.
- No live, demo, or paper order was submitted.
- No backtest or profitability evaluation was performed.
- No artifact contents were available because the run returned no artifacts.
- Workflow logs were downloadable, but their contents were not read.
- Binary research files such as Pages documents, images, and PDFs were not interpreted in this inspection.
- No claim is made that the current `main` branch ran or passed the workflow.
- No credential values are reproduced.
