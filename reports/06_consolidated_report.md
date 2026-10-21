# Consolidated Project Mayhem Offline Testing and Numerical Validation Report

**Report date:** 2026-10-21  
**Repository:** `https://github.com/evanh56/ProjectMayhem`  
**Owner:** `evanh56`  
**Reviewed branch:** `main`  
**Reviewed commit:** `91860a951ea08e205ebbfd8389becce8647ebb7e` (`Correct Login`)  
**Source path observed:** `ProjectMayhem/`  
**Related branch:** `fix/offline-testability-m15-append`, observed at the same commit  
**Repository modifications:** None

## 1. Workflow run evidence

The supplied workflow-run log source returned nothing. Consequently, the requested run-log-only details are not available:

- Run ID: not shown in the supplied run log.
- Test count: not shown in the supplied run log.
- Individual test names and results: not shown.
- Overall `OK` or failed status: not shown.
- Python version: not shown.
- Artifact name: not shown.
- Artifact ID: not shown.
- Artifact size: not shown.
- Artifact SHA256: not shown.
- Tested commit from `git rev-parse`, `git log`, or a fetched ref: not shown.

No run was dispatched or retrieved by this reporting process. The missing capability is workflow-dispatch/retrieval access and readable workflow-log contents.

The repository inspection separately reports an existing GitHub Actions run, but that API metadata is not treated as supplied run-log evidence for the requested run-result fields. It reports run `39128978458` as completed successfully at an earlier SHA, with no artifacts returned and a downloadable ZIP whose contents were not exposed. Individual test output therefore remains unavailable.

Because the supplied run log does not list test names, no test names or individual results are claimed here.

Passing starter tests, even if a successful run is independently recorded, do not establish:

- strategy correctness;
- absence of look-ahead bias;
- valid position sizing;
- valid execution controls;
- realistic transaction-cost handling;
- profitability;
- acceptable drawdown or risk;
- paper-trading or live-trading readiness.

## 2. Reviewed revision and tested revision comparison

The reviewed revision is:

```text
91860a951ea08e205ebbfd8389becce8647ebb7e
```

The supplied workflow run log does not show a tested commit. Therefore, comparison between the tested commit and the reviewed commit is unavailable.

The repository inspection separately records an existing run at:

```text
ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8
```

That is repository inspection metadata, not a tested commit shown in the supplied run log. It is therefore not used as the run-log tested revision for this report.

## 3. Calculation and numerical-validation table

| Calculation | Inputs and units | Formula | Result | Evidence source | Label |
|---|---|---|---|---|---|
| Initial risk budget | Equity \(E\), account-currency units; risk fraction \(r\), dimensionless | \(B=E\\times r\) | Must use current equity and an approved fraction no greater than 0.02 | `risk_policy`, D002 | Proposed/required calculation; not executed |
| Worked risk budget | \(E=10{,}000\) account-currency units; \(r=0.02\) | \(10{,}000\\times0.02\) | \(200\) account-currency units | Supplied engineer handoff | Independently derived arithmetic; not tool-executed |
| Risk distance | Entry \(P_e\), stop \(P_s\), quote-price units | \(d=|P_e-P_s|\) | Positive distance required | Supplied handoffs | Approved calculation rule; not executed |
| Long 2R target | Entry and stop in quote-price units | \(TP=P_e+2d\) | Determined only after a valid long entry and stop exist | D002 and supplied handoffs | Approved calculation rule; not executed |
| Short 2R target | Entry and stop in quote-price units | \(TP=P_e-2d\) | Determined only after a valid short entry and stop exist | D002 and supplied handoffs | Approved calculation rule; not executed |
| Long worked 2R example | Entry `200.00`; stop `199.80`; quote-price units | \(d=200.00-199.80=0.20\); \(TP=200.00+2(0.20)\) | Distance `0.20`; target `200.40` | Supplied engineer handoff | Independently derived arithmetic; not tool-executed |
| Short worked 2R example | Entry `200.00`; stop `200.20`; quote-price units | \(d=200.20-200.00=0.20\); \(TP=200.00-2(0.20)\) | Distance `0.20`; target `199.60` | Supplied risk handoff | Independently derived arithmetic; not tool-executed |
| Invalid target inputs | Zero/non-positive stop distance or invalid side | Reject if \(d\\leq0\) or side is invalid | No target | Supplied engineer handoff | Proposed expected result |
| Gross stop loss per volume | Distance in price units; tick size in price units; tick value in account currency per tick per volume; volume \(v\) | \(v\\times(d/\text{tick size})\\times\text{tick value}\) | Cannot be calculated from supplied data | `risk_policy` | Required formula; not numerically executed |
| Cost-adjusted intended risk | Gross loss plus spread, commission, slippage and other costs | \(\text{total risk}=\text{gross loss}+\text{costs}\) | Must not exceed the risk budget | `risk_policy`, `data_dictionary` | Required control; inputs missing |
| Maximum unrounded volume | Risk budget \(B\); loss per volume \(L_v\) | \(v_{\max}=B/L_v\) | Cannot calculate without verified broker specifications | `risk_policy` | Required formula; no volume result |
| Rounded volume | Maximum volume and broker step \(s\) | \(\lfloor v_{\max}/s\rfloor s\) | Round down only | `risk_policy` | Proposed expected result |
| Minimum-volume control | Rounded volume and broker minimum | Reject when rounded volume is below minimum | No order | `risk_policy` | Proposed expected result |
| Bullish FVG fixture | Candle 1 high `199.2`; candle 3 low `199.85`; price units | Outer-candle gap bounds | Expected lower/upper values `199.2` and `199.85` | `tests/test_offline.py` | Test expectation, not executed in this report |
| Bearish FVG fixture | Transformed fixture; price units | Inverted outer-candle relationship | Expected values approximately `200.8` and `200.15` in the test fields | `tests/test_offline.py` | Test expectation, not executed in this report |

No lot size, pip value, contract size, conversion rate, P&L, drawdown, win rate, profit factor, or profitability result is reported.

## 4. Implementation defects and unresolved requirements

### Implementation and repository findings

The supplied inspection and handoffs identify or document the following implementation concerns:

- The documented historical source path `src/ProjectMayhem/` does not match the observed tree, which contains `ProjectMayhem/` directly at repository root.
- The test fixture uses `GBPUSD`, while the stated strategy scope is GBPJPY and USDJPY.
- No separately named USDJPY CSV was observed.
- The repository contains broker-related authentication assignments and an `mt.login` call in `ProjectMayhem/main.py`.
- Broker-related import-time side effects are documented.
- `Execution.taketrade()` is documented as printing `"Work in Progress"` and not placing orders.
- `Execution.main()` is documented as returning without placing an order.
- `Execution.price_to_pip()` is not verified as a risk-policy-compliant sizing implementation.
- Existing tests dynamically load only `FairValueGap.py`.
- Existing tests do not cover H1 context, M15 confirmation, order blocks, liquidity, stops, sizing, 2R targets, costs, sessions, holding time, exposure, or broker reconciliation.
- Potential append failure, possible `NameError`, incomplete strategy state handling, scheduling limitations, look-ahead risk, and execution stubs remain previously documented findings. They were not independently re-verified from inline source bodies in this session.
- The raw source responses did not expose complete source bodies or line numbers, so exact source-line claims are unavailable.
- Credential values are intentionally not reproduced.

### Unresolved requirements

The following remain unspecified or insufficiently defined:

1. Canonical H1 zone, order-block and FVG definitions.
2. Bullish and bearish direction semantics.
3. M15 confirmation timing.
4. Market, limit or stop entry behavior.
5. Exact entry-price basis and intrabar rules.
6. Liquidity-event definition and stop anchor.
7. Stop buffer and spread treatment.
8. Trading sessions and timezone.
9. Maximum holding period.
10. Aggregate open-risk and concurrent-position limits.
11. Combined JPY exposure limits for GBPJPY and USDJPY.
12. Daily loss and drawdown controls.
13. Frequency, cooldown and duplicate-signal semantics.
14. News and external-factor treatment.
15. Spread, commission, slippage and stale-data thresholds.
16. Chronological development, validation and holdout windows.
17. Minimum sample size and promotion criteria.
18. Symbol identity, broker identity, timezone and candle-completion metadata.
19. Account currency, contract specifications, tick value, volume constraints and conversion rates.

Undefined controls must be treated as missing configuration and fail closed. They must not be silently interpreted as zero, unlimited or default values.

## 5. Missing data and execution capabilities

The following data or capabilities were not available or not verified:

- Readable contents of the supplied workflow-log ZIP.
- Workflow-run log test names and individual results.
- Workflow artifact contents; the inspected API result returned no artifacts.
- Current-revision workflow execution.
- Local Python execution.
- Dependency installation and local test execution.
- Complete inline source bodies for six raw-content responses.
- Source line numbers for implementation findings.
- Identified GBPJPY and USDJPY historical series.
- Symbol and broker metadata.
- Account currency and current equity.
- Tick size, tick value, contract size and volume constraints.
- Spread, commission and slippage data.
- Timezone and candle-completion metadata.
- Execution, fill, cost, outcome and equity-curve data.
- Broker or MT5 access.
- Paper trading or live trading results.
- Backtest results.
- P&L, win rate, drawdown or profit factor.
- Workflow dispatch or rerun capability.
- Repository writing, commit or push capability.

No broker session was opened, no credentials were used, no orders were placed, no dependencies were installed, and no repository code was executed by this reporting process.

## 6. One prioritised implementation task

### Priority task

**Assigned agent:** Engineering agent, with product-owner approval and QA review.

**Task:** Establish a reviewed, broker-independent offline validation layer for the approved GBPJPY/USDJPY strategy.

**Dependencies:**

- Product owner resolves Q01–Q11.
- Canonical FVG, order-block, liquidity-stop, entry and timestamp rules are approved.
- Identified GBPJPY and USDJPY fixtures are supplied with timezone and candle-completion metadata.
- Broker symbol specifications and account-currency conversion rules are supplied.
- Credential exposure and import-time broker side effects are removed from offline-test paths.
- Risk, exposure, cost and fail-closed policies are approved.

**Acceptance criteria:**

1. Pure functions exist for approved FVG detection, order-block detection, 2R target geometry and position sizing.
2. Offline imports do not authenticate with MT5 or contact a broker.
3. Tests cover completed-candle H1/M15 temporal joins without look-ahead.
4. Tests cover FVG lifecycle, invalidation and canonical boundaries.
5. Tests cover approved order-block and liquidity semantics.
6. Tests reject invalid stops, missing data, stale data and missing symbol/account metadata.
7. Position sizing includes approved risk, costs, rounding and minimum-volume controls.
8. The test suite uses identified symbols and timezone-aware fixtures.
9. The workflow runs at the current reviewed commit and produces readable retained evidence.
10. No claim of profitability or strategy correctness is made solely from these tests.

No implementation was started, repaired or applied.

## 7. Usage and cost

Observable usage and cost were not supplied or verified.

No billable tool usage, runner duration, token usage, cloud cost, broker cost, market-data cost, or execution cost can be reported. No profitability or financial return was established.

---

# Appendix A — Repository Inspection Returned Here

The repository inspection returned the following information.

## Repository and branch observed

- Repository URL: `https://github.com/evanh56/ProjectMayhem`
- Owner: `evanh56`
- Repository: `ProjectMayhem`
- Branch inspected: `main`
- Main head SHA returned by GitHub: `91860a951ea08e205ebbfd8389becce8647ebb7e`
- Main commit message: `Correct Login`
- Main branch protection: disabled

## Access check

`ProjectMayhem/main.py` was readable through `github_get_raw_repository_content`. The action returned a text response with MIME type `text/plain`, the file name, and a signed temporary download location, but did not expose source text inline.

The `main` branch exists at:

```text
91860a951ea08e205ebbfd8389becce8647ebb7e
```

The `fix/offline-testability-m15-append` branch exists and currently points to the same SHA.

## Workflow inspection

The workflow path is:

```text
.github/workflows/offline-tests.yml
```

The observed configuration is:

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

The workflow is manually triggered only, uses Python 3.11 on `ubuntu-latest`, has a five-minute timeout, installs `requirements-ci.txt`, runs the offline unittest discovery command, and uploads `reports/ci/` for one day. It has no workflow inputs, uses read-only contents permission, and disables checkout credential persistence.

The API inspection reported one existing run:

- Run ID: `39128978458`
- Status: `completed`
- Conclusion: `success`
- Head SHA: `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`
- Created: `2026-10-18T12:50:34Z`
- Event: `workflow_dispatch`
- Branch: `main`
- Run number: `1`
- Updated: `2026-10-18T12:50:58Z`

No artifacts were returned:

```json
{"artifacts":[],"total_count":0}
```

A logs ZIP was returned:

```text
evánh56_ProjectMayhem_run_39128978458_logs.zip
```

The ZIP contents were not exposed as readable text.

## Repository tree

A non-truncated recursive tree for SHA `91860a951ea08e205ebbfd8389becce8647ebb7e` showed:

- `.github/`
- `ProjectMayhem/`
- `docs/`
- `reports/`
- `research/`
- `skills/`
- `tests/`
- `requirements-ci.txt`

No `src/` directory was returned.

## Dependencies

`requirements-ci.txt` contains:

```text
pandas==2.2.3
```

## Tests

`tests/test_offline.py` imports `ast`, `csv`, `importlib.util`, `os`, `Path`, `tempfile`, and `unittest`.

It dynamically loads:

```text
ProjectMayhem/FairValueGap.py
```

It does not import `main.py`, `Execution.py`, `OrderBlockAnalysis.py`, `Liquidity.py`, or `Strategy.py`.

The tests:

- parse all Python files under `ProjectMayhem/`;
- require at least one Python source file;
- dynamically locate exactly one `FairValueGap.py`;
- run from a temporary working directory;
- write `GBPUSD_15m_Data.csv`;
- write `FairValueGap_15m.csv`;
- call `self.fvg.search_for_fvg()`;
- test bullish detection;
- test bearish detection;
- test rejection of overlapping outer candles;
- test removal after a later boundary breach.

The bullish fixture is:

```python
[
    [199.0, 199.2, 198.9, 199.1],
    [199.3, 199.9, 199.25, 199.8],
    [199.9, 200.0, 199.85, 199.95],
]
```

The expected bullish output is one row with:

```text
Position = "Bullish"
Prev_candle ≈ 199.2
Next_candle ≈ 199.85
```

The bearish fixture is generated by:

```python
[
    [400 - o, 400 - low, 400 - high, 400 - close]
    for o, high, low, close in self.bullish_candles()
]
```

The expected bearish output is one row with:

```text
Position = "Bearish"
Prev_candle ≈ 200.8
Next_candle ≈ 200.15
```

The overlap test changes the third candle’s low to `199.1` and expects no rows. The later-boundary test appends:

```python
[199.9, 200.0, 199.1, 199.3]
```

and expects no retained gap.

## Source files

The following files returned signed raw-content download responses:

- `ProjectMayhem/main.py`
- `ProjectMayhem/Execution.py`
- `ProjectMayhem/FairValueGap.py`
- `ProjectMayhem/OrderBlockAnalysis.py`
- `ProjectMayhem/Liquidity.py`
- `ProjectMayhem/Strategy.py`

The source bodies were not returned inline, so source line numbers and complete source reproduction are unavailable.

The tree reported these sizes:

| Path | Size |
|---|---:|
| `ProjectMayhem/main.py` | 14,684 bytes |
| `ProjectMayhem/Execution.py` | 905 bytes |
| `ProjectMayhem/FairValueGap.py` | 2,551 bytes |
| `ProjectMayhem/OrderBlockAnalysis.py` | 7,206 bytes |
| `ProjectMayhem/Liquidity.py` | 3,223 bytes |
| `ProjectMayhem/Strategy.py` | 4,734 bytes |

Compiled cache files under `ProjectMayhem/__pycache__/` were skipped.

## CSV files

The tree returned:

```text
ProjectMayhem/Current_Candle_1m_Data.csv
ProjectMayhem/FairValueGap_15m.csv
ProjectMayhem/GBPUSD_15m_Data.csv
ProjectMayhem/GBPUSD_1hr_Data.csv
ProjectMayhem/Liquidity_15m.csv
ProjectMayhem/OrderBlock_15m.csv
ProjectMayhem/OrderBlock_1hr.csv
```

The available snapshots are named `GBPUSD`, while project documentation describes GBPJPY and USDJPY. No independently named USDJPY CSV was returned.

## Documentation

`docs/project_overview.md` states that:

- it was updated 18 October 2026;
- its version is `0.1`;
- the project targets GBPJPY and USDJPY;
- it uses H1 areas of interest and M15 confirmation;
- it is a Python/MT5 prototype, not a verified trading system;
- no broker session, live order, paper trade or profitability test was performed while preparing the documents;
- existing source describes implemented behavior, not necessarily intended or correct behavior;
- the historical entry point is documented as `src/ProjectMayhem/main.py`, while the actual tree has `ProjectMayhem/main.py`;
- six Python modules and seven CSV snapshots were inspected;
- limitations include hard-coded GBPJPY, GBPUSD filenames, incomplete strategy state handling, execution stubs and commented-out scheduling;
- credential exposure exists in `main.py`;
- `Execution.py::taketrade()` prints `"Work in Progress"`;
- `main()` returns without placing an order;
- an isolated offline harness, removal of broker side effects from imports and a dependency manifest were recommended.

Credential values were not reproduced. Required remediation is to remove embedded values, rotate any exposed credentials, use secret management, keep offline tests secret-free and avoid broker login at import time.

## Inspection limitations

No repository code was executed, dependencies were not installed, no MT5 or broker connection was made, no market data was retrieved, no orders were placed, no backtest was run, no workflow was dispatched or rerun, and no repository modifications were made.

---

# Appendix B — Offline Testing and Numerical Validation Handoff Returned Here

## Repository and revision

- Repository: `evanh56/ProjectMayhem`
- Branch: `main`
- Observed commit: `91860a951ea08e205ebbfd8389becce8647ebb7e` (`Correct Login`)
- Actual source path: `ProjectMayhem/`
- Related branch: `fix/offline-testability-m15-append`
- Existing CI run: `39128978458`, successful according to repository API metadata, at earlier SHA `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`
- No artifacts returned and log contents not exposed.

## Intended strategy

| Item | Requirement | Status |
|---|---|---|
| Instruments | GBPJPY and USDJPY | Owner requirement |
| Higher timeframe | H1 areas of interest | Owner requirement |
| Confirmation | M15 | Owner requirement |
| Target | Exactly 2R | Owner requirement |
| Intended maximum risk | 2% per trade | Owner requirement |
| Objective | Short-duration trading | Owner requirement |
| Frequency | 2–3 trades/day | Intent, not acceptance criterion |
| No forced trades | No trade without valid setup | Proposal |
| Execution | No production order placement available | Observed/documented fact |

The current offline tests are a narrow FVG detector contract. They do not validate the intended complete strategy.

Material mismatches include:

- GBPUSD fixture instead of GBPJPY or USDJPY;
- no H1 area selection;
- no M15 confirmation;
- no direction alignment;
- no order blocks;
- no liquidity-based stops;
- no entry timing;
- no risk sizing;
- no 2R target;
- no sessions;
- no holding period;
- no transaction costs;
- no portfolio exposure.

The test assertions are treated as implementation/test expectations, not owner-approved strategy definitions.

## Approved and unresolved calculations

Approved or sufficiently specified:

- intended risk budget: `0.02 × current account equity`;
- initial target: `2 × initial stop distance`;
- volume rounds down and is rejected when minimum volume exceeds the risk budget;
- H1/M15 joins use only information available at event time;
- supplied bullish FVG fixture expectation;
- supplied bearish FVG fixture expectation;
- supplied FVG invalidation expectation.

Unresolved:

- zone definitions;
- direction labels;
- confirmation timing;
- entry type and price;
- liquidity stop definition;
- sessions;
- maximum holding period;
- aggregate exposure;
- frequency semantics;
- evaluation and promotion criteria;
- news treatment;
- spread, slippage, commission and data freshness;
- order-block direction and boundaries;
- liquidity output interpretation;
- timezone and candle-completion semantics.

Undefined controls must fail closed.

## FVG boundaries and invalidation

For the bullish fixture:

```text
C1: O=199.0, H=199.2,  L=198.9,  C=199.1
C2: O=199.3, H=199.9,  L=199.25, C=199.8
C3: O=199.9, H=200.0,  L=199.85, C=199.95
```

The expected output is one bullish row with bounds represented by approximately `199.2` and `199.85`. The inferred bullish gap is:

```text
[199.20, 199.85]
```

The transformed bearish fixture expects approximately `200.15` and `200.80`.

The field names `Prev_candle` and `Next_candle` do not clearly identify lower and upper bounds. A canonical `min/max` representation was proposed, subject to approval.

The later boundary-breach test expects the gap to disappear after:

```text
O=199.9, H=200.0, L=199.1, C=199.3
```

The tests do not establish whether wick or close invalidation applies, whether invalidation is intrabar or at candle close, whether retests consume zones, or whether immutable event history is required.

## Order blocks, liquidity and timestamps

The supplied material does not define the order-block candle, direction, body/wick boundaries, timeframe, invalidation or conflict resolution.

It also does not define equal-high/equal-low tolerance, swing lookback, liquidity side, sweep semantics, stop anchor, stop buffer or spread/slippage handling.

The CSV timestamps lack timezone offset, broker/server timezone, candle-completion flag, extraction timestamp, symbol, broker and spread metadata.

A proposed interpretation is:

1. complete the H1 candle;
2. identify its zone only after completion;
3. process later completed M15 candles;
4. timestamp confirmation at M15 close unless another rule is approved;
5. permit entry only using quotes available after confirmation.

This is proposed, not approved.

## Proposed acceptance examples

### Bullish FVG

Expected:

```text
row_count = 1
Position = "Bullish"
lower_bound = 199.20
upper_bound = 199.85
```

### Overlap rejection

Changing the third candle low to `199.1` should produce:

```text
row_count = 0
```

### Later breach

A bullish zone with bounds `199.20` and `199.85`, followed by a candle with low `199.1`, should not remain retained under the current test contract.

### Timestamp gate

If an H1 candle closes at `10:00 UTC` and confirmation is observed on the `10:30 UTC` M15 close, the earliest permissible entry decision is after `10:30 UTC`.

### 2R example

For long entry `200.00` and stop `199.80`:

```text
Risk distance = 0.20
Target distance = 0.40
Target = 200.40
```

### Fail-closed sizing

For equity `10,000` and risk fraction `2%`, the intended budget is `200` account-currency units. Missing or stale entry, stop, tick value, conversion, cost or volume data must cause rejection. No lot-size result is available.

## Blockers and recommended next action

Material blockers are:

1. No independently identified GBPJPY or USDJPY data.
2. Missing symbol, broker, timezone, completion, spread and provenance metadata.
3. FVG boundary and invalidation semantics not approved.
4. Order-block semantics unresolved.
5. Liquidity and stop semantics unresolved.
6. Confirmation and entry timing unresolved.
7. Session and holding-period rules unresolved.
8. Portfolio and daily-loss controls unresolved.
9. No realistic cost model or trade-level data.
10. Current CI evidence is for an earlier commit with no artifacts.
11. No project-owned dependency manifest beyond `requirements-ci.txt`.
12. Credential exposure and import-time broker side effects remain documented risks.

Recommended next action is to resolve Q01–Q11, approve canonical definitions, supply identified data and metadata, establish costs, add deterministic tests, rerun at the current revision, and only then design chronological simulation.

Final status: offline evidence supports only narrow FVG fixture behavior and syntax-oriented checks. The intended strategy is not sufficiently specified for numerical backtesting, and no profitability conclusion is justified.

---

# Appendix C — Offline-Testing Systems Handoff Returned Here

## Repository and workflow

Observed repository:

- `evanh56/ProjectMayhem`
- branch `main`
- commit `91860a951ea08e205ebbfd8389becce8647ebb7e`
- source directory `ProjectMayhem/`
- related branch at the same commit
- no repository changes

Workflow behavior:

- manual `workflow_dispatch`;
- Ubuntu runner;
- Python 3.11;
- five-minute timeout;
- installs `requirements-ci.txt`;
- records commit, Python version and `pip freeze`;
- runs:

```bash
python -m unittest discover -s tests -p 'test_offline.py' -v
```

- uploads `reports/ci/` for one day;
- no workflow inputs;
- read-only contents permission;
- checkout credentials disabled.

`requirements-ci.txt` contains only:

```text
pandas==2.2.3
```

The existing API-recorded run is:

```text
Run ID: 39128978458
Status: completed
Conclusion: success
Workflow: Project Mayhem Offline Tests
Event: workflow_dispatch
Branch: main
Run head: ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8
Created: 2026-10-18T12:50:34Z
```

No artifacts were returned. A logs ZIP was available but not readable in this inspection. No individual test output is claimed.

## Tests inspected

`tests/test_offline.py`:

- parses all Python files under `ProjectMayhem`;
- dynamically loads only `ProjectMayhem/FairValueGap.py`;
- uses temporary files;
- tests `FairValueGap.search_for_fvg()`;
- uses `GBPUSD_15m_Data.csv` and `FairValueGap_15m.csv`;
- tests bullish detection, bearish detection, overlap rejection and later-boundary removal.

It does not test GBPJPY, USDJPY, H1/M15 joins, order blocks, liquidity, entry timing, stops, sizing, 2R target geometry, costs, sessions, holding time, exposure or broker reconciliation.

## Relevant documented implementation

Identified paths:

```text
ProjectMayhem/main.py
ProjectMayhem/Execution.py
ProjectMayhem/FairValueGap.py
ProjectMayhem/OrderBlockAnalysis.py
ProjectMayhem/Liquidity.py
ProjectMayhem/Strategy.py
```

Inline source bodies and source line numbers were unavailable.

Documented callable names and behavior include:

- `FairValueGap.search_for_fvg()`;
- `Execution.taketrade()`;
- `Execution.price_to_pip()`;
- `Execution.main()`;
- `taketrade()` prints `"Work in progress"` and does not place orders;
- `Execution.main()` does not place orders;
- `main.py` contains broker authentication assignments and an `mt.login` call;
- the historical entry point has broker-related import side effects;
- `price_to_pip` is not verified as risk-policy-compliant.

## Proposed isolated numerical interfaces

Proposed, not existing or applied:

```python
def detect_fvg(candles: Sequence[Candle]) -> list[FVG]:
    ...
```

```python
def detect_order_blocks(
    candles: Sequence[Candle],
    *,
    definition: OrderBlockDefinition,
) -> list[OrderBlock]:
    ...
```

```python
def calculate_target(
    *,
    entry: Decimal,
    stop: Decimal,
    side: Literal["buy", "sell"],
    reward_to_risk: Decimal = Decimal("2"),
) -> Decimal:
    ...
```

```python
def calculate_position_size(
    *,
    equity: Decimal,
    risk_fraction: Decimal,
    entry: Decimal,
    stop: Decimal,
    side: Literal["buy", "sell"],
    value_per_price_unit: Decimal,
    spread_cost: Decimal,
    slippage_cost: Decimal,
    volume_min: Decimal,
    volume_max: Decimal,
    volume_step: Decimal,
) -> Decimal:
    ...
```

These interfaces should reject invalid distances, invalid sides, non-finite values, missing symbol/account conversion information and volumes below broker minimum. No numerical implementation was applied.

## Verified findings

- Broker side effects and credential-related authentication are documented in `ProjectMayhem/main.py`.
- `Execution.taketrade()` is an execution stub.
- `Execution.main()` does not place an order.
- `Execution.price_to_pip()` is not verified sizing.
- Tests cover only FVG behavior.
- Fixtures use GBPUSD rather than GBPJPY/USDJPY.
- CSV snapshots lack independent symbol identity and provenance.
- Timestamps lack timezone and completion metadata.
- No execution, fill, cost, outcome or equity-curve data exists.
- Workflow evidence is from an earlier commit.
- No workflow artifacts were retained in the inspected run.

Previously documented but not newly re-verified findings include possible append failure, possible `NameError`, incomplete strategy state handling, scheduling limitations, look-ahead risk, execution stubs and credential exposure.

## Checks and capabilities

No checks were executed by this handoff. No code was run, dependencies installed, unittest executed, MT5 imported, broker authenticated, market data retrieved, backtest run, workflow dispatched or rerun, or repository modified.

Unavailable:

- workflow dispatch and rerun;
- readable workflow logs;
- artifact contents;
- inline source bodies and source line numbers;
- local execution;
- broker or MT5 session;
- credentials and account data;
- historical data retrieval;
- paper, live or backtest execution;
- full Pages, screenshot or PDF interpretation.

## Proposed smallest coherent extension

1. Keep broker integration out of offline-test imports.
2. Add pure helpers for FVGs, approved order blocks, 2R geometry and fail-closed sizing.
3. Add deterministic in-memory tests.
4. Test timestamp gating, no look-ahead joins, invalid stops, 2R geometry, risk caps, volume rounding, minimum-volume rejection and missing-data rejection.
5. Add symbol and timezone metadata.
6. Rerun at the current revision and retain artifacts.

This must wait for owner decisions on semantics, stops, sessions, entry timing, holding period, costs and portfolio controls.

---

# Appendix D — Numerical Validation and Risk/Execution Handoff Returned Here

## Status

No live or paper trading is authorised. No account was accessed, no credentials were used, no orders were placed and no repository changes were made.

## Repository and material

Observed:

- repository `evanh56/ProjectMayhem`;
- branch `main`;
- commit `91860a951ea08e205ebbfd8389becce8647ebb7e`;
- source path `ProjectMayhem/`;
- related branch at same revision;
- existing API-recorded CI run `39128978458` at earlier SHA `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`;
- no artifacts returned.

Inspected material consisted of the project overview, six named Python modules, seven CSV snapshots, offline tests, CI dependency file, workflow configuration, and repository metadata. Source bodies and line numbers were not exposed inline.

## Risk and target controls

The approved initial intended per-trade risk is 2% of current equity. The approved initial target is 2R. These are intended controls, not guarantees of realised loss or evidence of profitability.

Required gross risk formula:

```text
gross stop loss =
volume × (price distance / tick size) × tick value
```

Cost-adjusted intended risk must include spread, commission, slippage and other approved costs.

Volume must be rounded down to the broker step and rejected if below the broker minimum.

No numerical lot size is available because current equity, account currency, contract size, tick size, tick value, volume constraints, entry, stop, spread, commission, slippage, conversion rates and margin restrictions were not supplied or verified.

## Intended versus realised loss

Realised loss can exceed intended stop risk because of gaps, slippage, spread widening, rejected or delayed protective orders, connection failures, partial fills, commissions, financing, restart discrepancies and reconciliation failures.

The application must separately report:

- planned/intended risk at submission;
- actual realised loss after fills, costs and conversion.

The stop must not be described as a guaranteed loss limit.

## Combined GBPJPY and USDJPY exposure

Long GBPJPY and long USDJPY both create short-JPY exposure. Short positions create long-JPY exposure. The instruments also retain distinct GBP and USD exposure and are not interchangeable or perfectly hedged.

The application must calculate:

1. gross notional exposure;
2. net JPY exposure;
3. directional exposure by instrument;
4. aggregate open risk;
5. pending-order and partial-fill exposure.

No numerical exposure calculation is possible because no positions, quantities, prices, contracts or conversion rates were supplied.

## Missing account controls

The following remain undefined and must fail closed:

- maximum concurrent positions;
- aggregate open risk;
- combined JPY exposure;
- gross and net portfolio exposure;
- daily loss limit;
- realised plus unrealised loss treatment;
- maximum drawdown;
- maximum trades per day;
- per-symbol limits;
- cooldown rules;
- maximum holding period;
- spread, slippage and stale-data thresholds;
- news and market-closure restrictions;
- emergency shutdown threshold.

## Required execution controls

The system must reject stale or incomplete data, including missing or inconsistent quotes, unconfirmed candles, missing symbol/timezone/broker identity, incomplete history and excessive spread.

For rejected or partially filled orders, it must record broker identifiers, reconcile actual broker state, recalculate residual risk, protect filled quantities and avoid blind resubmission.

For duplicate submissions, it must use deterministic client identifiers, check local and broker state, suppress equivalent duplicates and use only bounded retries.

For disconnects and timeouts, it must halt new submissions, reconnect with bounded retries, reconcile positions/orders/fills before resuming and escalate unresolved discrepancies.

On restart, it must compare local state with broker positions, orders, fills and equity, identify unknown, duplicate, orphaned or unprotected positions, halt new trading and verify protection.

Protective orders must be verified after fills. Stops must not be widened, risk must not be increased after a loss, and an unprotected position must be escalated.

Emergency shutdown must prevent new orders, cancel eligible pending orders, preserve audit logs, reconcile final state and require explicit review before resumption.

## Credential handling

Documented credential-related locations are in `ProjectMayhem/main.py`, including module-level authentication assignments and an `mt.login` call.

Required actions:

- remove embedded credentials;
- rotate credentials that may have been committed;
- use secret management;
- remove import-time broker login;
- keep offline tests secret-free;
- do not connect an account for this validation.

## Paper-trading blockers

### P0

1. Remove credential exposure and import-time broker effects.
2. Define Q01–Q11, including entry, stop, timing, sessions and holding period.
3. Define aggregate risk, concurrency, daily loss, drawdown and JPY-exposure limits.
4. Implement and test fail-closed sizing with verified broker specifications.
5. Implement reconciliation, duplicate prevention, partial-fill handling and protection checks.
6. Supply identified timezone-aware GBPJPY and USDJPY data.
7. Establish spread, commission and slippage assumptions.

### P1

8. Add deterministic tests for geometry, sizing, rounding, minimum volume and invalid input.
9. Add no-look-ahead H1/M15 tests.
10. Add immutable signal/order/fill/trade records.
11. Rerun current-revision CI and retain readable artifacts.
12. Establish chronological development, validation and holdout windows.

### P2

13. Demonstrate paper execution over an approved period.
14. Reconcile orders, fills, positions, costs and equity.
15. Measure realised loss, slippage, rejected orders, disconnections, duplicate attempts and protection failures.
16. Obtain independent QA/risk review and product-owner approval.

## Checks

None were executed. No repository code was run, dependencies installed, workflow dispatched or rerun, broker or MT5 session opened, or paper/live order submitted.

The supplied arithmetic examples are independently derived and are not tool-executed results.

## Recommendation

**Reject for paper trading and live trading.**

The repository does not yet provide a numerically validated or operationally reliable implementation of the approved GBPJPY/USDJPY strategy. The release is blocked by unresolved strategy and account-level limits, absent verified metadata and costs, incomplete execution controls, credential/import risks, lack of reconciliation evidence and absence of current-revision numerical tests.

---

# Appendix E — QA Handoff

The QA handoff source returned nothing.

No QA test results, test counts, test names, pass/fail statuses, defect list or independent QA approval were supplied.

The report files were not written because this reporting process cannot write files or commit to the repository.