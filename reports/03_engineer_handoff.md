# Offline-testing systems handoff

## Repository state observed

- **Repository:** `evanh56/ProjectMayhem`
- **Branch:** `main`
- **Observed commit:** `8feb36db91d7144b4a190a302634ddd30c449c0b`
- **Source directory:** `ProjectMayhem/`
- **No source, test, workflow, or documentation files were modified.**
- **No broker-connected entry point was imported or run.**
- **No credentials are reproduced.**

A historical GitHub Actions run was supplied:

- **Run:** `39128978458`
- **Head:** `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`
- **Conclusion:** `success`
- **Relationship to current `main`:** not applicable; the run head differs from the observed current commit.
- **Artifacts:** none returned.
- **Logs:** a downloadable archive descriptor was returned, but the log contents were not read.

Therefore, there is no execution result establishing that current `main` passes offline tests.

## Files and functions inspected

### Workflow and dependencies

- `.github/workflows/offline-tests.yml`
  - Checks out the repository.
  - Uses Python 3.11.
  - Installs `requirements-ci.txt`.
  - Runs `python -m unittest discover -s tests -p 'test_offline.py' -v`.
  - Attempts to upload `reports/ci/`.
  - Has `workflow_dispatch` and a push trigger only for `improvement/offline-foundation-v1`.
  - Has no workflow inputs.
  - Has a five-minute timeout.

- `requirements-ci.txt`
  - Contains only:
    ```text
    pandas==2.2.3
    ```
  - This is insufficient for the runtime imports observed in the application, which include `MetaTrader5`, `pytz`, and `tzlocal`.

### Tests

- `tests/test_offline.py`
  - `SourceChecks.test_python_source_has_valid_syntax`
  - `FairValueGapChecks.test_detects_bullish_gap`
  - `FairValueGapChecks.test_detects_bearish_gap`
  - `FairValueGapChecks.test_rejects_overlapping_outer_candles`
  - `FairValueGapChecks.test_removes_gap_after_later_boundary_breach`

The tests parse source and dynamically load only `ProjectMayhem/FairValueGap.py`. They do not import `main.py`, `Execution.py`, `Strategy.py`, `Liquidity.py`, or `OrderBlockAnalysis.py`.

### Implementation

- `ProjectMayhem/main.py`
  - MT5 login and account access.
  - Candle retrieval and CSV writing.
  - Scheduling and application entry points.
  - `main()`, `run_scheduler()`, `check_1m()`, `check_15m()`, `check_1hr()`.
  - Module-level MT5 login occurs before the `__main__` guard.

- `ProjectMayhem/FairValueGap.py`
  - `add_fvg()`
  - `check_fvg()`
  - `search_for_fvg()`
  - `main()`

- `ProjectMayhem/OrderBlockAnalysis.py`
  - `countRows()`
  - `AddOb()`
  - `check_prev()`
  - `Next_candle()`
  - `OB_check()`
  - `Analyse_Data()`
  - `main()`

- `ProjectMayhem/Liquidity.py`
  - `Add_liq()`
  - `check_liq()`
  - `find_liq()`
  - `main()`

- `ProjectMayhem/Strategy.py`
  - `check_trading_time()`
  - `check_if_in_ob_hr()`
  - `correct_dir()`
  - `check_if_in_fvg()`
  - `run_strategy_check()`
  - `main()`

- `ProjectMayhem/Execution.py`
  - `price_to_pip()`
  - `taketrade()`
  - `main()`

## Findings and evidence

### 1. Broker side effects and credential exposure remain

**Path/function:** `ProjectMayhem/main.py`, module-level code and MT5 login setup.

Observed:

- MT5 login is executed at import time.
- Credential assignments exist in the file.
- MT5 calls include `initialize()`, `login()`, `account_info()`, `copy_rates_from_pos()`, and `shutdown()`.

This prevents `main.py` from being safely imported by offline tests and remains a credential and isolation blocker.

### 2. Instrument and data-file mismatch remains

**Paths/functions:**

- `ProjectMayhem/main.py`
- `ProjectMayhem/FairValueGap.py::search_for_fvg()`
- `ProjectMayhem/Liquidity.py::find_liq()`

Observed:

- Runtime symbol is `GBPJPY`.
- Data files are named `GBPUSD_15m_Data.csv` and `GBPUSD_1hr_Data.csv`.
- No independent USDJPY stream or symbol column was observed.

### 3. Runtime dependency manifest is incomplete

**Path:** `requirements-ci.txt`

Only `pandas==2.2.3` is declared, while source imports additional external packages. The CI manifest is adequate only for the supplied narrow test suite, not for the application runtime.

### 4. Execution and risk controls remain incomplete

**Path/functions:** `ProjectMayhem/Execution.py::price_to_pip()`, `taketrade()`, `main()`.

Observed:

- `taketrade()` prints `"Work in progress"` and returns.
- No MT5 `order_send` path was observed.
- Stop-loss and take-profit construction are absent.
- `price_to_pip()` uses experimental balance-derived arithmetic.
- It does not implement the documented current-equity, stop-loss-loss, contract, account-currency, cost, or broker-constraint checks.

The documented 2% risk policy is therefore not implemented.

### 5. Forming-candle and timestamp issues remain

**Path/functions:** `ProjectMayhem/main.py`, candle retrieval and CSV-writing functions.

Observed:

- Retrieval starts at MT5 position zero.
- No explicit completed-candle filter was observed.
- Timestamps are converted to Europe/London and then made timezone-naive.
- CSVs lack completion metadata, symbol identity, price basis, and extraction provenance.

### 6. FVG implementation is testable but not approved as the final strategy definition

**Path/function:** `ProjectMayhem/FairValueGap.py::search_for_fvg()`.

Observed implementation:

- Three-candle bullish and bearish conditions.
- Raw threshold `0.00005`.
- Later-row invalidation scans.
- Output fields `Date`, `Prev_candle`, `Next_candle`, and `Position`.

The existing tests validate selected implementation behaviour. They do not establish that these formulas are the approved FVG specification. The fixed raw-price threshold is also not instrument-normalised for GBPJPY and USDJPY.

### 7. Order-block implementation remains look-ahead-sensitive

**Path/functions:** `ProjectMayhem/OrderBlockAnalysis.py::OB_check()`, `Analyse_Data()`, `main()`.

Observed:

- Direction is based on `Open - Close > 0`.
- Later candles are scanned for containment, activation, and invalidation.
- A doji or equal-open/close candle falls into the bullish branch.
- Global counters and later-row scans affect outputs.

The approved OB definition, body/wick bounds, doji handling, and event-time semantics remain unresolved.

### 8. Liquidity implementation remains undefined for trading use

**Path/functions:** `ProjectMayhem/Liquidity.py::check_liq()`, `find_liq()`.

Observed:

- Raw thresholds include `0.06` and `0.00018`.
- Levels are derived from candle highs or lows.
- No approved sweep definition, stop offset, spread adjustment, or invalidation rule exists.

### 9. Strategy state and session rules remain incomplete

**Path/functions:** `ProjectMayhem/Strategy.py::run_strategy_check()`, `check_trading_time()`, `correct_dir()`, `check_if_in_fvg()`.

Observed:

- Global state is used for hourly and M15 zones.
- Confirmation/indexing behaviour is incomplete.
- A `07:00` to `02:00` crossing-midnight session is implemented, but it is not confirmed as an owner-approved session.
- Entry, stop, expiry, and maximum holding-period rules are not complete.

### 10. CI evidence is stale relative to current `main`

The supplied successful run is real evidence for run `39128978458`, but its head SHA is `ad1e0ee0...`, not current `main` SHA `8feb36db...`. No current-commit pass can be inferred.

The run returned no artifacts despite artifact upload being configured.

## Isolated numerical-test suitability

### Currently usable without MT5

`ProjectMayhem/FairValueGap.py::search_for_fvg()` is the only implementation function currently exercised in an isolated manner by the supplied tests. The existing test harness dynamically loads the module with `importlib.util` and changes into a temporary working directory.

This approach should remain limited to FVG until module import behaviour is independently verified.

### Not currently suitable for direct isolated numerical testing

- `ProjectMayhem/main.py`: unsafe to import because of module-level MT5 login and broker side effects.
- `ProjectMayhem/Execution.py`: contains MT5-dependent account access and does not implement approved sizing.
- `ProjectMayhem/Strategy.py`: depends on file inputs and mutable global state.
- `ProjectMayhem/Liquidity.py`: file-oriented and stateful.
- `ProjectMayhem/OrderBlockAnalysis.py`: file-oriented, counter-dependent, and later-row/state sensitive.

### Proposed pure numerical interfaces

These are recommendations only; they are not present in the repository and were not added.

```python
def detect_fvg(candles, threshold, symbol):
    ...


def detect_order_block(candles, definition):
    ...


def calculate_target(entry_price, stop_price, direction, reward_risk=2.0):
    ...


def calculate_position_size(
    equity,
    risk_fraction,
    entry_price,
    stop_price,
    contract_loss_model,
    commission,
    slippage,
    volume_constraints,
):
    ...
```

The pure functions should accept explicit data and configuration, return deterministic values, and have no MT5, filesystem, credential, scheduling, or global-state dependency.

For approved 2R geometry only:

- Long: `target = entry + 2 * (entry - stop)`
- Short: `target = entry - 2 * (stop - entry)`

This is arithmetic guidance, not a completed strategy implementation.

Sizing must fail closed when equity, contract information, account currency, costs, stop-loss loss, or broker volume constraints are unavailable. No numeric defaults should be invented.

## Checks executed

No repository tests, workflow, application modules, broker calls, backtests, or numerical simulations were executed during this handoff.

The only execution evidence available is the supplied historical GitHub Actions result for run `39128978458`. Its logs were not read, its artifacts list was empty, and it does not correspond to the observed current `main` commit.

## Previously documented findings

Previously documented findings F01–F10 remain materially present based on the current inspection, including:

- credential exposure;
- broker side effects on import;
- GBPJPY/GBPUSD naming mismatch;
- missing independent USDJPY stream;
- append and data-handling concerns;
- possible name/indexing errors;
- invalid confirmation/indexing behaviour;
- scheduling concerns;
- look-ahead effects;
- missing execution, sizing, and testing evidence.

No finding was marked resolved by this read-only inspection.

## Assumptions and blockers

### Assumptions

- The supplied inspection record is the complete evidence base.
- The historical CI run is not treated as a current-branch test result.
- Existing FVG tests are treated as implementation tests, not strategy approval.
- Unresolved Q01–Q11 decisions remain unresolved.
- No missing risk or execution parameter is replaced with a default.

### Blockers

- Current `main` has not been shown to pass offline tests.
- `main.py` cannot safely serve as an offline import target.
- Credentials remain in source and should be rotated and removed through an approved remediation.
- No complete runtime dependency manifest exists.
- No symbol-specific, provenance-preserving GBPJPY and USDJPY dataset pair is available.
- OB, FVG, liquidity, confirmation, entry, stop, session, holding-period, portfolio, and evaluation rules are not fully approved.
- Execution and risk sizing are not implemented.
- Binary research materials, including screenshots, PDFs, and Pages documents, were not available for review.

## Capabilities and files not accessible or not performed

- No local filesystem or local Python execution was available.
- No workflow dispatch action was available.
- No workflow rerun action was available.
- No current-commit workflow execution was performed.
- The historical workflow log archive was not opened or read.
- No workflow artifacts were available; GitHub returned zero artifacts for the supplied run.
- No broker connection, MT5 initialization, authentication, account access, paper trade, live trade, or backtest was performed.
- No binary Pages documents, screenshots, or PDF contents were supplied for inspection.
- No source-writing, test-writing, workflow-editing, commit, push, pull-request, merge, or deployment capability was used.

## Recommended next action

The smallest coherent repair/test extension should be proposed—not applied—as follows:

1. Rotate and remove exposed credentials under an approved security change.
2. Add an import-safe offline boundary so broker setup occurs only inside an explicit runtime function.
3. Run the workflow against exact current `main` and retain its logs and artifacts.
4. Add offline tests for:
   - import isolation;
   - symbol/file identity;
   - completed-candle handling;
   - timestamp and provenance preservation;
   - deterministic FVG, OB, and liquidity calculations;
   - 2R geometry;
   - fail-closed sizing validation.
5. Resolve Q01–Q11 before treating numerical strategy tests as evidence of trading performance.
6. Build separate, provenance-preserving GBPJPY and USDJPY historical inputs.
7. Only then perform chronological, cost-adjusted historical evaluation followed by controlled paper-testing review.

No profitability, paper-trading, live-readiness, or risk-policy compliance conclusion is supported by the supplied evidence.
