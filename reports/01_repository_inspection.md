# Inspection record

## Repository and branch observed

- Repository URL: `https://github.com/evanh56/ProjectMayhem`
- Owner: `evanh56`
- Repository: `ProjectMayhem`
- Branch inspected: `main`
- Main head SHA returned by GitHub: `91860a951ea08e205ebbfd8389becce8647ebb7e`
- Main commit message: `Correct Login`
- Main branch protection: disabled

## Access check

### 1. Read `ProjectMayhem/main.py` on `main`

GitHub action used: `github_get_raw_repository_content`

Exact result: returned a text response with:

- `mimetype`: `text/plain`
- `name`: `main.py`
- A signed temporary download location

The action did not return the source text inline, but it confirmed that `ProjectMayhem/main.py` was readable.

### 2. Get branch `main`

GitHub action used: `github_get_a_branch`

Exact result: branch exists.

Returned head SHA:

```text
91860a951ea08e205ebbfd8389becce8647ebb7e
```

### 3. Get branch `fix/offline-testability-m15-append`

GitHub action used: `github_get_a_branch`

Exact result: branch exists.

Returned head SHA:

```text
91860a951ea08e205ebbfd8389becce8647ebb7e
```

It currently points to the same commit as `main`.

### 4. List workflow runs for `.github/workflows/offline-tests.yml` on `main`

GitHub action used: `github_list_workflow_runs_for_a_workflow`

Exact result: one workflow run was returned.

| Run ID | Status | Conclusion | Head SHA | Created |
|---:|---|---|---|---|
| `39128978458` | `completed` | `success` | `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8` | `2026-10-18T12:50:34Z` |

Additional returned facts:

- Workflow: `Project Mayhem Offline Tests`
- Event: `workflow_dispatch`
- Head branch: `main`
- Run number: `1`
- Run started: `2026-10-18T12:50:34Z`
- Updated: `2026-10-18T12:50:58Z`

This is real GitHub Actions evidence returned by the workflow-run API. It is separate from any owner-pasted log or documentation summary.

### Artifacts for the latest completed run

GitHub action used: `github_list_workflow_run_artifacts`

Exact result:

```json
{"artifacts":[],"total_count":0}
```

No artifacts were returned.

### Logs for the latest completed run

GitHub action used: `github_download_workflow_run_logs`

Exact result: a logs ZIP archive was returned:

- MIME type: `application/zip`
- Name: `evanh56_ProjectMayhem_run_39128978458_logs.zip`

Therefore, the run logs could be downloaded. The returned action did not expose the ZIP contents as readable text in this inspection.

## Tree and root folders

GitHub action used: `github_get_a_tree`, recursive tree on `main`.

Exact result: returned a non-truncated recursive tree for SHA:

```text
91860a951ea08e205ebbfd8389becce8647ebb7e
```

Observed root folders:

- `.github/`
- `ProjectMayhem/`
- `docs/`
- `reports/`
- `research/`
- `skills/`
- `tests/`

The tree also returned `requirements-ci.txt`.

The repository contains `ProjectMayhem/` directly at the root. No `src/` directory was returned.

## Workflow configuration

Path:

```text
.github/workflows/offline-tests.yml
```

GitHub action used: `github_get_repository_content`

Exact returned file content, decoded from the returned Base64:

```yaml
name: Project Mayhem Offline Tests

on:
  workflow_dispatch:

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
        uses: actions/checkout@v7
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
        uses: actions/upload-artifact@v7
        with:
          name: project-mayhem-offline-results-${{ github.run_id }}-${{ github.run_attempt }}
          path: reports/ci/
          retention-days: 1
          if-no-files-found: warn
```

Observed configuration:

- Trigger: manual `workflow_dispatch` only.
- Python version: `3.11`.
- Runner: `ubuntu-latest`.
- Timeout: 5 minutes.
- Inputs: no `workflow_dispatch` inputs are defined.
- Dependency installation: `requirements-ci.txt`.
- Test command: `python -m unittest discover -s tests -p 'test_offline.py' -v`.
- Artifacts: configured through `actions/upload-artifact@v7`.
- Upload condition: `always()`.
- Artifact retention: 1 day.
- The workflow has read-only repository contents permission.
- Checkout credentials persistence is disabled.

## `requirements-ci.txt`

Path:

```text
requirements-ci.txt
```

GitHub action used: `github_get_repository_content`

Exact file content:

```text
pandas==2.2.3
```

## `tests/test_offline.py`

Path:

```text
tests/test_offline.py
```

GitHub action used: `github_get_repository_content`

The returned file imports:

```python
import ast
import csv
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
```

It dynamically loads:

```python
ProjectMayhem/FairValueGap.py
```

It does not import `main.py`, `Execution.py`, `OrderBlockAnalysis.py`, `Liquidity.py`, or `Strategy.py`.

### Tests returned

#### `SourceChecks.test_python_source_has_valid_syntax`

Assertions and behavior:

- Collects Python files under `ProjectMayhem/`, excluding:
  - `.venv`
  - `venv`
  - `__pycache__`
  - `.git`
  - `__MACOSX`
- Asserts that at least one Python source file exists.
- Parses every discovered Python file with `ast.parse`.
- Uses `subTest` with the relative filename.

#### `FairValueGapChecks.setUpClass`

Behavior:

- Finds exactly one `FairValueGap.py` under the source directory.
- Raises `RuntimeError` if the count is not exactly one.
- Loads that file dynamically as module `fvg_under_test`.

#### `FairValueGapChecks.setUp`

Behavior:

- Saves the original working directory.
- Creates a temporary directory.
- Changes into that temporary directory.

#### `FairValueGapChecks.tearDown`

Behavior:

- Restores the original working directory.
- Removes the temporary directory.

#### `FairValueGapChecks.detect`

Behavior:

- Writes a temporary `GBPUSD_15m_Data.csv`.
- Header:

```text
Date,Open,High,Low,Close
```

- Writes supplied candles with timestamps beginning at `2025-01-01 00:00:00`, incrementing by 15 minutes.
- Writes a temporary `FairValueGap_15m.csv`.
- Header:

```text
Date,Prev_candle,Next_candle,Position
```

- Calls:

```python
self.fvg.search_for_fvg()
```

- Reads and returns the generated CSV rows.

#### `FairValueGapChecks.bullish_candles`

Returns three candle rows:

```python
[
    [199.0, 199.2, 198.9, 199.1],
    [199.3, 199.9, 199.25, 199.8],
    [199.9, 200.0, 199.85, 199.95],
]
```

#### `FairValueGapChecks.test_detects_bullish_gap`

Assertions:

- Exactly one output row.
- `Position == "Bullish"`.
- `Prev_candle` approximately equals `199.2`.
- `Next_candle` approximately equals `199.85`.

#### `FairValueGapChecks.test_detects_bearish_gap`

Constructs a bearish candle sequence by transforming the bullish candles:

```python
[
    [400 - o, 400 - low, 400 - high, 400 - close]
    for o, high, low, close in self.bullish_candles()
]
```

Assertions:

- Exactly one output row.
- `Position == "Bearish"`.
- `Prev_candle` approximately equals `200.8`.
- `Next_candle` approximately equals `200.15`.

#### `FairValueGapChecks.test_rejects_overlapping_outer_candles`

Behavior:

- Changes the third candle’s low to `199.1`.
- Asserts the detector returns an empty list.

#### `FairValueGapChecks.test_removes_gap_after_later_boundary_breach`

Behavior:

- Appends:

```python
[199.9, 200.0, 199.1, 199.3]
```

- Asserts the detector returns an empty list.

The file ends with:

```python
if __name__ == "__main__":
    unittest.main()
```

## Files inspected

The following GitHub raw-content actions all returned signed text download responses:

- `ProjectMayhem/main.py`
- `ProjectMayhem/Execution.py`
- `ProjectMayhem/FairValueGap.py`
- `ProjectMayhem/OrderBlockAnalysis.py`
- `ProjectMayhem/Liquidity.py`
- `ProjectMayhem/Strategy.py`

The raw-content action returned metadata and signed download locations rather than inline source text in this session. Consequently, I cannot truthfully reproduce the source bodies or count source line numbers from those responses.

The tree confirms these source paths and sizes:

| Path | Size returned |
|---|---:|
| `ProjectMayhem/main.py` | 14,684 bytes |
| `ProjectMayhem/Execution.py` | 905 bytes |
| `ProjectMayhem/FairValueGap.py` | 2,551 bytes |
| `ProjectMayhem/OrderBlockAnalysis.py` | 7,206 bytes |
| `ProjectMayhem/Liquidity.py` | 3,223 bytes |
| `ProjectMayhem/Strategy.py` | 4,734 bytes |

The tree also returned compiled cache files under:

```text
ProjectMayhem/__pycache__/
```

These were skipped as requested.

## CSV files observed

The tree returned these CSV files under `ProjectMayhem/`:

```text
ProjectMayhem/Current_Candle_1m_Data.csv
ProjectMayhem/FairValueGap_15m.csv
ProjectMayhem/GBPUSD_15m_Data.csv
ProjectMayhem/GBPUSD_1hr_Data.csv
ProjectMayhem/Liquidity_15m.csv
ProjectMayhem/OrderBlock_15m.csv
ProjectMayhem/OrderBlock_1hr.csv
```

The filenames show the documented mismatch: the available market-data snapshots are named `GBPUSD`, while the supplied project documentation reports code selecting `GBPJPY`; no independently named `USDJPY` CSV was returned.

## Documentation evidence

Path:

```text
docs/project_overview.md
```

GitHub action used: `github_get_repository_content`

The returned document states, among other points:

- Updated 18 October 2026.
- Version `0.1`.
- The project targets GBPJPY and USDJPY.
- It uses hourly areas of interest and 15-minute confirmation.
- It is a Python/MT5 prototype, not a verified trading system.
- No broker session, live order, paper trade, or profitability test was performed while preparing the documents.
- Existing source code describes implemented behavior, not necessarily intended or correct behavior.
- The historical entry point is documented as `src/ProjectMayhem/main.py`, but the actual tree shows the source directly at `ProjectMayhem/main.py`.
- The document itself records that six Python modules and seven CSV snapshots were inspected.
- It records limitations involving hard-coded GBPJPY, GBPUSD filenames, incomplete strategy state handling, execution stubs, and commented-out scheduling.
- It identifies credential exposure in `main.py`.
- It states that `Execution.py::taketrade()` prints `"Work in progress"` and that `main()` returns without placing an order.
- It calls for an isolated offline harness, removal of broker side effects from imports in a reviewed change, and a dependency manifest before code execution.

The documentation’s `src/ProjectMayhem/` references are legacy documentation paths. The actual GitHub tree confirms `ProjectMayhem/` at the repository root.

## Credential locations

The documentation identifies credential-related code in:

```text
ProjectMayhem/main.py
```

Specifically, it describes module-level authentication assignments and an `mt.login` call.

Credential values were not reproduced.

Required remediation:

- Remove embedded credential values from source.
- Rotate any credentials that may have been committed.
- Use a secret-management mechanism for any future broker-connected environment.
- Keep offline tests secret-free.
- Avoid broker login as an import-time side effect.

## Workflow run evidence

The only run returned by the workflow-run listing was:

```text
Run ID: 39128978458
Status: completed
Conclusion: success
Head SHA: ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8
Created: 2026-10-18T12:50:34Z
Event: workflow_dispatch
Branch: main
```

Artifacts:

```text
No artifacts returned; total_count: 0
```

Logs:

```text
Download succeeded; ZIP archive returned:
evạnh56_ProjectMayhem_run_39128978458_logs.zip
```

This run evidence is not merged with the owner-provided documentation or any pasted log. The run head SHA differs from the current `main` head SHA observed above, which is expected because the current branch has since advanced.

## Execution and capability status

I did not execute repository code, install dependencies, authenticate with MT5, connect to a broker, retrieve market data, place orders, run local tests, or perform a backtest.

The workflow was not executed by me.

I have no action available to dispatch or re-run workflows. The workflow-run listing returned an existing manually dispatched run, but I did not dispatch or re-run it.

No repository writes were performed. I did not:

- create files
- update files
- delete files
- commit
- push
- open a pull request
- dispatch a workflow
- re-run a workflow

Unavailable or not verified in this inspection:

- Inline source text for the six raw-content responses was not returned by the tool.
- Source line numbers for those six modules are therefore not observable from the returned data.
- Workflow log contents were not exposed; only a downloadable ZIP was returned.
- No artifact contents were returned.
- No local execution capability was used or verified.
- No broker or MT5 session was available or used.
- No live, paper, or simulated trading result was produced.
- No performance baseline, P&L, win rate, drawdown, or profit factor was established.
- No workflow dispatch or re-run capability is available.
- No file-writing or repository-modification capability is available. ; reports/02_researcher_handoff.md = # Offline testing and numerical validation handoff

## Repository / revision observed

- **Repository:** `evanh56/ProjectMayhem`
- **Branch:** `main`
- **Observed commit:** `91860a951ea08e205ebbfd8389becce8647ebb7e` (`Correct Login`)
- **Actual source path:** `ProjectMayhem/`; documentation references to `src/ProjectMayhem/` are legacy paths.
- **Related branch:** `fix/offline-testability-m15-append` points to the same observed commit.
- **Existing CI evidence:** workflow run `39128978458` completed successfully, but it ran at head SHA `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`, not the current observed `main` commit. No artifacts were returned and log contents were not exposed.

---

## 1. Intended strategy versus implementation and offline test expectations

### Confirmed intended requirements

| Item | Requirement | Status / source |
|---|---|---|
| Instruments | GBPJPY and USDJPY | **Owner requirement**, `project_overview`, `decision_log` D001 |
| Higher-timeframe context | H1 areas of interest | **Owner requirement**, `project_overview`, D001 |
| Confirmation timeframe | M15 | **Owner requirement**, `project_overview`, D001 |
| Initial target | Exactly 2R | **Owner requirement**, `project_overview`, `risk_policy`, D002 |
| Intended maximum risk | 2% per trade | **Owner requirement**, `project_overview`, `risk_policy`, D002 |
| Trading objective | Short-duration trading | **Owner requirement**, `project_overview` |
| Frequency | 2–3 trades/day | **Owner requirement / intent**, `decision_log` D003; not a performance acceptance criterion |
| No forced trades | Do not trade without a valid setup | **Proposal**, D009 |
| Execution | No production order placement is currently available | **Observed fact**, `project_overview`; `Execution.py::taketrade()` is documented as printing `"Work in progress"` |

### Repository and test behavior actually evidenced

`tests/test_offline.py`:

1. Parses all Python files under `ProjectMayhem/`.
2. Dynamically loads only `ProjectMayhem/FairValueGap.py`.
3. Creates temporary files named:
   - `GBPUSD_15m_Data.csv`
   - `FairValueGap_15m.csv`
4. Supplies candles with timestamps beginning at `2025-01-01 00:00:00`, at 15-minute intervals.
5. Tests bullish and bearish FVG detection.
6. Tests rejection when the outer candles overlap.
7. Tests removal of a detected gap after a later boundary breach.

### Reconciliation

The offline tests are a **narrow detector contract**, not a complete implementation of the intended GBPJPY/USDJPY H1–M15 strategy.

Material mismatches:

- The test fixture uses **GBPUSD**, while the project requirement is **GBPJPY and USDJPY**. This is consistent with the documented filename/data mismatch but does not validate either required instrument.
- The test exercises only `FairValueGap.py`; it does not validate:
  - H1 area selection;
  - M15 confirmation;
  - direction alignment;
  - order blocks;
  - liquidity-based stops;
  - entry timing;
  - risk sizing;
  - 2R take-profit;
  - sessions;
  - holding period;
  - transaction costs;
  - portfolio exposure.
- A passing CI run therefore establishes, at most, syntax validity and the tested FVG fixture behavior. It does **not** establish runtime readiness or a trading edge. This follows `experiment_log`, EXP-000, and `risk_policy`.

**Assumption A1 — explicit:** The assertions in `tests/test_offline.py` are treated as current implementation/test expectations, not as owner-approved definitions of the trading strategy.

---

## 2. Approved calculations versus unresolved definitions

### Approved or sufficiently specified

| Calculation / rule | Current definition | Status |
|---|---|---|
| Initial risk fraction | `0.02 × current account equity` as the intended maximum risk budget | **Approved owner requirement**, `risk_policy` |
| Initial target | `TP distance = 2 × initial stop distance` for a 2R target | **Approved owner requirement**, D002 |
| Position sizing inputs | Equity, approved risk fraction, side, symbol, volume rules, entry assumptions, execution costs, price precision, margin and currency conversion | **Approved control requirements**, `risk_policy` |
| Volume rounding | Round volume down; reject if minimum volume exceeds the risk budget | **Approved owner requirement**, `risk_policy` |
| H1/M15 temporal join | Use only information available at the event time | **Approved owner requirement**, `data_dictionary` |
| FVG bullish test result | For the supplied test fixture, output one bullish row with bounds represented by `Prev_candle ≈ 199.2` and `Next_candle ≈ 199.85` | **Test expectation only**, `tests/test_offline.py` |
| FVG bearish test result | For the transformed fixture, output one bearish row with bounds represented by `Prev_candle ≈ 200.8` and `Next_candle ≈ 200.15` | **Test expectation only**, `tests/test_offline.py` |
| FVG invalidation test | A later candle boundary breach removes the earlier detected gap | **Test expectation only**, `tests/test_offline.py` |

### Unresolved strategy definitions

The following are not numerically defined by the supplied digest or inspection record:

| Q reference | Unresolved item | Required decision |
|---|---|---|
| Q01–Q04 | Zone definitions, direction labels, confirmation timing | Define exact H1 area, OB/FVG boundaries, bullish/bearish labels, and when an M15 confirmation becomes actionable |
| Q05 | Entry rule | Market, limit, or stop entry; exact trigger candle; entry price basis; whether entry occurs intrabar or only after M15 close |
| Q06 | Liquidity stop | Define the liquidity event, stop anchor, buffer, spread treatment, and whether the stop is beyond a wick, swing, or zone |
| Q07 | Sessions | Select LDN, NY, Asia, or a precise timezone/session window |
| Q08 | Maximum holding period | Set a numeric limit; “not multiple hours” is not executable |
| Q09 | Portfolio limits | Aggregate open risk, concurrent positions, directional JPY exposure, daily loss and drawdown limits |
| Q10 | Frequency semantics | Define whether 2–3 trades/day is a target, cap, per-symbol limit, or portfolio limit; define cooldown and duplicate-signal behavior |
| Q11 | Evaluation evidence and promotion | Define minimum sample size, chronological development/validation/holdout windows, cost assumptions, and promotion criteria |

Additional unresolved calculations:

- News and external-factor treatment: `Strategy.txt`, pending decisions.
- Spread, slippage, commission and data-freshness limits: `risk_policy`, `data_dictionary`.
- Order-block direction and boundary semantics.
- Liquidity output interpretation, because the digest states that some side/context information is lost.
- Timezone and candle-completion semantics, because CSV timestamps have no offset or completion metadata.

**Assumption A2 — explicit:** Undefined controls must be treated as missing configuration and cause a fail-closed result, not as zero, unlimited, or an implicit default. Source: `decision_log`, `risk_policy`.

---

## 3. Review of FVG boundaries, order-block direction, liquidity levels and timestamps

### Fair-value-gap boundaries

The tested bullish fixture is:

| Candle | Open | High | Low | Close |
|---|---:|---:|---:|---:|
| 1 | 199.0 | 199.2 | 198.9 | 199.1 |
| 2 | 199.3 | 199.9 | 199.25 | 199.8 |
| 3 | 199.9 | 200.0 | 199.85 | 199.95 |

The test expects:

- `Position = "Bullish"`
- `Prev_candle ≈ 199.2`
- `Next_candle ≈ 199.85`

This is consistent with an inferred bullish outer-candle gap:

\[
\text{bullish gap bounds} = [\text{candle 1 high},\ \text{candle 3 low}]
= [199.20,\ 199.85]
\]

For the transformed bearish fixture, the expected values are:

\[
[200.15,\ 200.80]
\]

However:

- The field names `Prev_candle` and `Next_candle` do not clearly state lower and upper bounds.
- The digest proposes normalising FVG display bounds using `min/max` while retaining original fields.
- The implementation’s output is a regenerated snapshot with later-row invalidation scans, not an immutable event history.

**Conclusion:** The numeric test behavior is reproducible from the test file, but the approved strategy meaning of the boundaries remains unresolved under **Q01–Q04**.

### FVG invalidation

`test_removes_gap_after_later_boundary_breach` appends:

```text
Open 199.9, High 200.0, Low 199.1, Close 199.3
```

and expects no retained FVG.

This establishes a test expectation that a later candle breaching the gap boundary invalidates the output. It does not establish:

- whether any wick breach or only a close invalidates;
- whether invalidation occurs at candle close or intrabar;
- whether a retest consumes the zone;
- whether an invalidated event should remain in an immutable history.

These are part of **Q01–Q04** and the data-model concerns in `data_dictionary`.

### Order-block direction

The supplied material does not provide a sufficiently precise formula for:

- selecting the order-block candle;
- defining bullish versus bearish order blocks;
- using candle body, wick, or full range;
- determining whether the block is H1-only or can be M15;
- invalidating the block;
- resolving conflicts between an OB and an FVG.

The digest specifically records OB bounds and labels as requiring reconciliation. This remains unresolved under **Q01–Q04**.

**Assumption A3 — explicit:** No order-block formula should be inferred from filenames, labels, or historical trading terminology.

### Liquidity levels and stops

The supplied material does not define:

- equal-high/equal-low tolerance;
- swing lookback;
- buy-side versus sell-side liquidity;
- whether a liquidity sweep requires a wick and close back inside;
- which liquidity level anchors the stop;
- stop buffer size;
- treatment of spread and slippage.

The digest states that liquidity output loses some side/context information. Therefore the existing CSV cannot, by itself, be assumed to contain enough information for a directionally correct stop.

This remains unresolved under **Q05–Q06**, with cost and exposure controls additionally covered by `risk_policy`.

### Confirmation timestamps

The test creates 15-minute timestamps, but makes no timestamp assertions. The supplied CSV metadata lacks:

- timezone offset;
- broker/server timezone;
- candle-completion flag;
- extraction timestamp;
- symbol and broker identity;
- spread and price basis.

The intended join must therefore be:

1. Identify the completed H1 candle and H1 zone using data available at that time.
2. Process only completed M15 candles after the zone is known.
3. Timestamp the confirmation at the M15 candle close unless the owner approves an intrabar rule.
4. Permit entry only using a quote available after that confirmation timestamp.

This is a **proposed interpretation**, not an approved entry rule, and is unresolved under **Q04–Q05**.

**Assumption A4 — explicit:** No current-bar high, low, close, zone invalidation, or confirmation result may be used before that candle is complete.

---

## 4. Proposed worked acceptance examples

These examples are proposed acceptance tests, not evidence of strategy approval or profitability.

### Example 1 — bullish FVG detector

**Inputs**

- Instrument label: `GBPUSD` fixture only; this does not validate GBPJPY.
- Timeframe: M15.
- Three sequential candles, prices in quote-price units:

```text
C1: O=199.0, H=199.2,  L=198.9,  C=199.1
C2: O=199.3, H=199.9,  L=199.25, C=199.8
C3: O=199.9, H=200.0,  L=199.85, C=199.95
```

**Expected output**

```text
row_count = 1
Position = "Bullish"
lower_bound = 199.20
upper_bound = 199.85
```

The test file expresses these bounds as:

```text
Prev_candle ≈ 199.2
Next_candle ≈ 199.85
```

**Acceptance tolerance:** the existing test uses approximate numeric comparison; the exact tolerance should be retained or explicitly specified in the future test contract.

**Status:** Existing test expectation. Proposed canonical representation is `[min(Prev_candle, Next_candle), max(...)]`, subject to owner approval. Source: `tests/test_offline.py`; proposal in `data_dictionary`.

---

### Example 2 — overlapping outer candles reject the FVG

**Inputs**

Use Example 1 but change candle 3 low:

```text
C3 low = 199.1
```

Now candle 3 overlaps the earlier outer-candle range.

**Expected output**

```text
row_count = 0
```

**Status:** Existing test expectation. It does not define whether overlap is evaluated using wick ranges, bodies, or closes in the general strategy.

---

### Example 3 — later boundary breach invalidates the FVG

**Initial FVG**

```text
Bullish lower boundary = 199.20
Bullish upper boundary = 199.85
```

**Later M15 candle**

```text
O=199.9, H=200.0, L=199.1, C=199.3
```

**Expected output under the current test contract**

```text
FVG retained = False
```

**Proposed explicit interpretation**

- Any completed-candle low below `199.20` invalidates the bullish zone.
- Invalidation timestamp is the later candle’s close time.
- The zone remains in immutable event history with `invalidated_at`, rather than being deleted.

The last two points are proposals only.

---

### Example 4 — proposed H1/M15 timestamp gate

**Inputs**

- H1 candle closes at `10:00 UTC`.
- Its zone is first knowable at `10:00 UTC`.
- M15 candles close at `10:15`, `10:30`, `10:45`, and `11:00 UTC`.
- A confirmation condition is observed on the `10:30` M15 candle.

**Expected proposed behavior**

```text
H1 zone available: 10:00 UTC
M15 confirmation available: 10:30 UTC
Earliest permissible entry decision: after 10:30 UTC
M15 data from 10:30 onward may not be used to claim an earlier entry
```

**Status:** Proposed temporal rule based on the owner requirement to use information available at event time. Exact entry price and intrabar timing remain unresolved under **Q04–Q05**.

---

### Example 5 — proposed 2R calculation

**Inputs**

- Proposed long entry: `200.00`
- Proposed stop: `199.80`
- Price distance: `0.20` quote-price units
- Approved target multiple: `2R`

**Expected target**

\[
R = 200.00 - 199.80 = 0.20
\]

\[
TP = 200.00 + 2(0.20) = 200.40
\]

```text
Initial risk distance = 0.20
Target distance = 0.40
Take-profit = 200.40
```

**Status:** The 2R requirement is approved. The stop location and entry price are not approved, so this is only a calculation acceptance example.

---

### Example 6 — proposed fail-closed sizing example

**Inputs**

- Equity: `10,000` account-currency units
- Approved risk fraction: `2%`
- Risk budget: `200` account-currency units
- Entry, stop, symbol tick value, conversion rate, spread, slippage and volume constraints: required

**Expected behavior**

- If any required value is missing or stale: **reject order and report missing configuration**.
- If calculated volume is valid: round volume down to broker step.
- If rounded volume is below broker minimum: reject.

No pip value, contract size, or GBPJPY/USDJPY conversion value is supplied, so a numerical lot-size result must not be invented.

**Status:** Control behavior is owner-required; the numerical sizing implementation remains unvalidated.

---

## 5. Material inspected, blockers and next action

### Material inspected or evidenced

- `docs/project_overview.md`
- `ProjectMayhem/main.py`
- `ProjectMayhem/Execution.py`
- `ProjectMayhem/FairValueGap.py`
- `ProjectMayhem/OrderBlockAnalysis.py`
- `ProjectMayhem/Liquidity.py`
- `ProjectMayhem/Strategy.py`
- Seven CSV snapshots under `ProjectMayhem/`
- `tests/test_offline.py`
- `requirements-ci.txt`
- `.github/workflows/offline-tests.yml`
- Repository tree and branch/workflow metadata

The source-content inspection record confirms signed raw-content responses for the six modules, but did not expose their bodies inline or provide source line numbers. Conclusions about formulas are therefore limited to the supplied digest, file names, and test expectations.

### Not inspected / not claimed

No screenshots, Pages documents, or full PDF contents were provided. They were not reviewed and are not treated as requirements. No profitability, P&L, win rate, drawdown, profit factor, or live/paper result was derived.

### Material blockers

1. No independently identified GBPJPY or USDJPY market-data series.
2. CSVs lack symbol, broker, timezone, candle-completion, spread, price-basis and provenance fields.
3. FVG field names and invalidation semantics are not strategy-approved.
4. Order-block direction and boundaries are unresolved.
5. Liquidity levels and stop placement are unresolved.
6. M15 confirmation and entry timing are unresolved.
7. Session and maximum holding-period rules are unresolved.
8. Portfolio exposure, daily loss and concurrency limits are unresolved.
9. No realistic cost model or transaction-level trade data exists.
10. Current CI evidence is for an earlier commit and has no retained artifacts.
11. No project-owned dependency manifest beyond `requirements-ci.txt` was evidenced.
12. Credential exposure and import-time broker side effects remain documented risks; credential values are intentionally not reproduced.

### Recommended next action

The product owner should resolve **Q01–Q11** in order:

1. Approve canonical FVG and order-block definitions and boundary conventions.
2. Define liquidity detection and stop-buffer rules.
3. Define completed-candle confirmation and executable entry timing.
4. Select sessions and numeric holding-period limits.
5. Set aggregate exposure, concurrency, daily-loss and frequency controls.
6. Approve a symbol-identified, timezone-aware GBPJPY/USDJPY historical dataset.
7. Establish spread, commission, slippage and stale-data assumptions.
8. Add deterministic unit tests for H1/M15 joins, zone lifecycle, stops, 2R targets and sizing.
9. Re-run the isolated offline suite at the current commit and retain artifacts.
10. Only then design a chronological development/validation/untouched-holdout simulation.

**Final status:** Offline testing evidence supports only the narrow FVG fixture behavior and syntax-oriented CI checks. The intended GBPJPY/USDJPY strategy is not yet sufficiently specified for numerical backtesting, and no profitability conclusion is justified.