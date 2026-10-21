# Offline-testing systems handoff

## Repository observed

- Repository: `evanh56/ProjectMayhem`
- Branch: `main`
- Observed commit: `91860a951ea08e205ebbfd8389becce8647ebb7e` (`Correct Login`)
- Source directory: `ProjectMayhem/`
- Related branch: `fix/offline-testability-m15-append`
- Related branch currently points to the same observed commit.
- No repository changes were made.

## Workflow inspection

Inspected:

```text
.github/workflows/offline-tests.yml
requirements-ci.txt
tests/test_offline.py
```

Workflow behavior:

- Manual `workflow_dispatch` only.
- Ubuntu runner.
- Python `3.11`.
- Five-minute timeout.
- Installs `requirements-ci.txt`.
- Records Python version, commit, and `pip freeze`.
- Runs:

```bash
python -m unittest discover -s tests -p 'test_offline.py' -v
```

- Uploads `reports/ci/` for one day.
- No workflow inputs are defined.
- Repository contents permission is read-only.
- Checkout credential persistence is disabled.

`requirements-ci.txt` contains only:

```text
pandas==2.2.3
```

### Existing workflow evidence

A real workflow run is recorded:

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

This run was against an earlier commit than the currently observed `main` commit.

No artifacts were returned:

```text
total_count: 0
```

A logs ZIP was available for download, but its contents were not exposed in this inspection. Therefore, the successful conclusion is known, but individual test output and dependency contents are not independently available here.

No failure result was supplied.

## Tests inspected

`tests/test_offline.py`:

- Parses all Python files under `ProjectMayhem/`.
- Dynamically loads only:

```text
ProjectMayhem/FairValueGap.py
```

- Uses temporary working-directory files.
- Tests `FairValueGap.search_for_fvg()`.
- Uses fixture filenames:
  - `GBPUSD_15m_Data.csv`
  - `FairValueGap_15m.csv`
- Tests:
  - bullish FVG detection;
  - bearish FVG detection;
  - rejection of overlapping outer candles;
  - removal after a later boundary breach.

The test suite does not test:

- GBPJPY;
- USDJPY;
- H1/M15 joins;
- order blocks;
- liquidity;
- entry timing;
- stops;
- position sizing;
- 2R target geometry;
- costs;
- sessions;
- maximum holding time;
- exposure controls;
- broker reconciliation.

The existing test is therefore a narrow FVG detector contract, not validation of the approved trading system.

## Relevant implementation inspected

The following source paths were identified and inspected through repository metadata/raw-content access:

```text
ProjectMayhem/main.py
ProjectMayhem/Execution.py
ProjectMayhem/FairValueGap.py
ProjectMayhem/OrderBlockAnalysis.py
ProjectMayhem/Liquidity.py
ProjectMayhem/Strategy.py
```

The raw-content responses supplied signed download locations rather than inline source bodies. Consequently, source line numbers and complete function inventories are not available from this inspection.

Observed or documented callable names:

- `FairValueGap.search_for_fvg()`
- `Execution.taketrade()`
- `Execution.price_to_pip()`
- `Execution.main()`

Documented behavior includes:

- `Execution.taketrade()` prints `"Work in progress"` and does not place orders.
- `Execution.main()` returns without placing an order.
- `main.py` contains broker-related authentication assignments and an `mt.login` call.
- The historical entry point performs broker-related side effects at import.
- `price_to_pip` is experimental and is not verified as a valid risk-policy implementation.

No credential values are reproduced.

## Functions suitable for isolated numerical testing

These should be pure, dependency-free functions in a future reviewed module. They are proposed interfaces, not existing functions and not applied changes.

### FVG detection

```python
def detect_fvg(candles: Sequence[Candle]) -> list[FVG]:
    ...
```

Required behavior must first be approved, but the current test contract implies:

- examine three sequential completed candles;
- bullish gap bounds derived from first-candle high and third-candle low;
- bearish gap bounds derived from the corresponding inverted relationship;
- reject overlapping outer candles;
- invalidate a gap after a later boundary breach.

A canonical result should retain:

```text
symbol
timeframe
formed_at
lower_bound
upper_bound
direction
invalidated_at
```

The existing `Prev_candle` and `Next_candle` names should be retained only for compatibility or explicitly migrated after approval.

### Order-block detection

No approved order-block definition is currently available. A future isolated interface could be:

```python
def detect_order_blocks(
    candles: Sequence[Candle],
    *,
    definition: OrderBlockDefinition,
) -> list[OrderBlock]:
    ...
```

The owner must define:

- source candle selection;
- bullish/bearish direction;
- body versus wick bounds;
- invalidation;
- timeframe;
- conflict handling with FVGs.

It would be incorrect to implement these semantics from the existing filename or labels alone.

### 2R geometry

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

For a long:

```text
risk_distance = entry - stop
target = entry + 2 * risk_distance
```

For a short:

```text
risk_distance = stop - entry
target = entry - 2 * risk_distance
```

The function should reject:

- non-positive risk distance;
- invalid side;
- non-finite prices;
- any reward-to-risk value other than the approved configured value when enforcing the initial strategy.

### Position sizing

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

Required controls:

- risk budget must not exceed `equity * 0.02`;
- current equity must be supplied;
- stop distance must be positive;
- execution costs must be included;
- volume must be rounded down to the broker step;
- reject if rounded volume is below the broker minimum;
- reject missing, stale, or invalid symbol/account conversion data;
- do not invent pip value, contract size, or currency conversion.

This function cannot be numerically validated for GBPJPY or USDJPY from the supplied snapshots because the required symbol metadata and account-currency conversion data are absent.

## Verified findings and evidence

Line numbers are unavailable because the raw source bodies were not returned inline.

| Finding | Evidence |
|---|---|
| Broker side effects and credential-related authentication exist in `ProjectMayhem/main.py` | Inspection record and `docs/project_overview.md`; exact credential values intentionally not reproduced |
| `Execution.taketrade()` is an execution stub | Documented behavior: prints `"Work in progress"` |
| `Execution.main()` does not place an order | Documented behavior: returns |
| `Execution.price_to_pip()` is not verified risk sizing | `risk_policy` |
| Existing tests cover only FVG behavior | `tests/test_offline.py` |
| Test fixtures use `GBPUSD`, not the required GBPJPY/USDJPY datasets | `tests/test_offline.py`; CSV filenames |
| CSV snapshots lack independent symbol identity and provenance | `data_dictionary` |
| No separate USDJPY series was supplied | Repository tree and `data_dictionary` |
| Timestamps lack timezone and candle-completion metadata | `data_dictionary` |
| No execution, fill, cost, outcome, or equity-curve data exists | `data_dictionary` |
| Current workflow evidence is from an earlier commit | Workflow run SHA versus current branch SHA |
| No workflow artifacts were retained in the inspected run | Artifact API result |

## Previously documented findings

Previously documented findings still stand based on the supplied inspection record:

- hard-coded or mismatched instrument handling;
- GBPUSD filenames inconsistent with the stated GBPJPY/USDJPY scope;
- absent independent USDJPY data;
- possible append failure;
- possible `NameError`;
- incomplete strategy state handling;
- scheduling limitations;
- look-ahead risk;
- execution stubs;
- credential exposure/import-time broker side effects;
- missing executable coverage for sizing, execution controls, and performance;
- insufficient historical data for an edge claim.

The source bodies and line-number evidence were not available in this session, so findings such as the possible append failure and possible `NameError` are retained as previously documented findings rather than newly re-verified defects.

## Checks executed in this handoff

None.

I did not:

- execute the repository locally;
- install dependencies;
- run `unittest`;
- import application modules;
- import MT5;
- authenticate;
- connect to a broker;
- retrieve market data;
- run a backtest;
- dispatch or re-run the workflow;
- modify files or branches.

The existing workflow run is real repository evidence, but it was not executed by me and was not run at the currently observed commit.

## Smallest coherent repair or test extension

Proposed only; not applied:

1. Keep broker integration out of import paths used by offline tests.
2. Move or add pure numerical helpers for:
   - FVG detection;
   - approved order-block detection;
   - 2R target geometry;
   - fail-closed position sizing.
3. Add deterministic unit tests using in-memory candles and explicit symbol metadata.
4. Add tests for:
   - completed-candle timestamp gating;
   - no look-ahead H1/M15 joins;
   - invalid stops;
   - exact 2R geometry;
   - risk cap enforcement;
   - volume-step rounding;
   - minimum-volume rejection;
   - missing-data rejection.
5. Add symbol and timezone metadata to future fixtures.
6. Re-run the workflow at the current commit and retain artifacts.

This extension must wait for owner decisions on FVG semantics, order blocks, liquidity stops, sessions, entry timing, holding period, costs, and portfolio controls.

## Assumptions and blockers

- Undefined strategy or risk controls are treated as missing configuration and must fail closed.
- The test fixture’s FVG semantics are implementation expectations, not automatically approved strategy definitions.
- No order-block formula may be inferred from terminology alone.
- No numerical position-size result may be produced without verified instrument and account-currency metadata.
- No profitability, P&L, drawdown, win-rate, or trading-edge conclusion is justified.

## Capabilities and files not accessible or not verified

- Workflow dispatch capability.
- Workflow re-run capability.
- Readable contents of the downloaded workflow-log ZIP.
- Workflow artifact contents; none were returned.
- Inline source bodies for the six raw-content responses.
- Source line numbers for implementation defects.
- Local Python execution.
- Local dependency installation.
- Broker or MT5 session.
- Credentials or account information.
- Historical data retrieval.
- Paper trading, live trading, or backtesting execution.
- Full interpretation of Pages documents, screenshots, and the complete PDF.
- Independent market-data provenance.

## Recommended next action

The product owner should resolve Q01–Q11, then approve a reviewed offline-test change that:

- removes import-time broker side effects from testable paths;
- establishes pure numerical interfaces;
- adds deterministic tests for FVG, order blocks, 2R geometry, sizing, and temporal joins;
- supplies identified GBPJPY and USDJPY data with timezone and completion metadata;
- defines realistic cost assumptions;
- runs and archives the suite at the current commit before any historical simulation or paper trading.