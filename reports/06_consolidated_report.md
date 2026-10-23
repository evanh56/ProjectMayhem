# Consolidated Project Mayhem Offline Testing and Numerical Validation Report

**Report date:** 2026-10-21  
**Repository:** `evanh56/ProjectMayhem`  
**Reviewed branch:** `main`  
**Observed reviewed commit:** `8feb36db91d7144b4a190a302634ddd30c449c0b`  
**Source path:** `ProjectMayhem/`

## 1. Evidence basis and workflow result

No raw workflow run log was supplied in the user-provided run-log section. The supplied inspection record states that a historical GitHub Actions run was retrieved, but its downloadable log contents were not read. Therefore, the requested log-derived fields are unavailable:

- run ID from the raw log: not shown in the supplied raw log;
- test count: not shown;
- individual test names and results: not shown;
- Python version: not shown;
- tested commit from `git rev-parse`, `git log`, or fetched ref: not shown in a read run log;
- artifact name, artifact ID, size, and SHA256: not shown;
- workflow `OK` or failed status from the raw log: not available.

No run was dispatched by this inspection, and no raw run log was retrieved or read. The missing capability is access to workflow-log contents or a workflow-dispatch/rerun action.

The repository inspection separately reports a historical GitHub Actions run with metadata:

- Run ID: `39128978458`
- Status: `completed`
- Conclusion: `success`
- Head SHA: `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`
- Artifacts: none returned
- Logs: downloadable ZIP descriptor returned, but contents not read

Those metadata are not treated as the requested raw run-log evidence. The reported historical head differs from the reviewed `main` commit, so the current reviewed commit has not been shown to pass.

Because no test count or test names appear in the supplied raw log, this report claims neither. Passing starter tests, even if the historical success metadata is considered, do not establish strategy correctness, absence of look-ahead bias, valid position sizing, execution safety, or profitability.

## 2. Tested-versus-reviewed commit comparison

The reviewed commit is observed as:

```text
8feb36db91d7144b4a190a302634ddd30c449c0b
```

The inspection record reports a historical workflow head as:

```text
ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8
```

Both values are present in the inspection record, so the available metadata indicate that the historical run was against a different commit from the reviewed `main` commit. The raw run log did not show a tested commit through `git rev-parse`, `git log`, or a fetched ref.

## 3. Calculation and numerical-validation table

No repository calculations were executed during this inspection. The table below distinguishes hand-derived arithmetic and proposed expectations from executed output.

| Calculation or check | Inputs and units | Formula or rule | Result | Evidence source | Label |
|---|---|---|---|---|---|
| Long 2R target | Entry `200.00` price units; stop `199.70` price units | `R = abs(entry - stop)`; long target `= entry + 2R` | `R = 0.30`; target `200.60` price units | Risk handoff worked example | Independently derived arithmetic |
| Short 2R target | Entry `200.00` price units; stop `200.30` price units | `R = abs(entry - stop)`; short target `= entry - 2R` | `R = 0.30`; target `199.40` price units | Risk handoff worked example | Independently derived arithmetic |
| Zero-distance stop validation | Entry equals stop | Reject when `abs(entry - stop) == 0` | Rejected | Risk handoff | Independently derived validation rule |
| Invalid long stop | Stop is not below long entry | Long-side validation requires a positive protective distance in the expected direction | Rejected | Risk handoff | Independently derived validation rule |
| Invalid short stop | Stop is not above short entry | Short-side validation requires a positive protective distance in the expected direction | Rejected | Risk handoff | Independently derived validation rule |
| Bullish FVG fixture | Three candles with previous high `199.20` and next low `199.85` | Repository FVG conditions and `next low > current open` | Expected `Bullish`, `Prev_candle = 199.20`, `Next_candle = 199.85` | `tests/test_offline.py` and `FairValueGap.py` description | Proposed expected result; not executed here |
| Bearish FVG fixture | Bearish-oriented three-candle fixture | Repository bearish FVG conditions | Expected one `Bearish` row | `tests/test_offline.py` description | Proposed expected result; not executed here |
| FVG later breach | Later low `199.80`; bullish boundary `199.85` | Bullish invalidation if later low or close is below `Next_candle` | Expected FVG removal | `FairValueGap.py` description | Proposed expected result; not executed here |
| Bearish OB example | Open `200.10`; close `199.90` | `Open - Close > 0` means bearish | Bearish zone approximately `199.90`–`200.10` | `OrderBlockAnalysis.py` and `Strategy.py` descriptions | Proposed expected result; not executed here |
| Liquidity example | High `200.50`; close `200.40` | `High - Close > 0.06` | Candidate accepted at level `200.50` | `Liquidity.py` description | Proposed expected result; not executed here |
| Maximum intended risk | Approved fraction, no account values supplied | `risk_fraction <= 0.02` | No tradable amount calculated | Risk policy and risk handoff | Requirement, not executed output |
| Position sizing | Equity, tick size/value, contract size, costs, quotes, constraints | Cost-inclusive loss must not exceed risk budget, then round down to broker volume step | No volume calculated because required inputs are unavailable | Risk handoff | Not executed; no value invented |
| Combined JPY exposure | No positions, volumes, prices, or contract data supplied | Sum signed GBPJPY and USDJPY JPY exposure | No numerical exposure calculated | Risk handoff | Not executed; no value invented |

The 2R examples are arithmetic illustrations only. They do not validate repository implementation, approve entry or stop rules, or demonstrate profitability.

## 4. Implementation defects

1. `ProjectMayhem/main.py` performs MT5 login at module scope, creating broker side effects on import.
2. Credential assignments are present in `ProjectMayhem/main.py`; values are intentionally not reproduced.
3. Runtime symbol selection is `GBPJPY`, while data files are named `GBPUSD_*`.
4. No independent USDJPY data stream or symbol column was observed.
5. `requirements-ci.txt` contains only `pandas==2.2.3`, while runtime imports also include `MetaTrader5`, `pytz`, and `tzlocal`.
6. `Execution.py::taketrade()` prints `"Work in progress"` and returns.
7. No working MT5 `order_send` path was observed.
8. Position sizing uses experimental balance-derived arithmetic and does not implement the documented current-equity, stop-loss, contract, currency, cost, or broker-constraint requirements.
9. Stop-loss and take-profit order construction are incomplete or absent.
10. MT5 retrieval begins at position zero, and no explicit completed-candle filter was observed.
11. Timestamps are converted to Europe/London and then made timezone-naive.
12. CSV outputs lack sufficient symbol, completion, offset, price-basis, and extraction-provenance information.
13. FVG detection uses fixed raw-price thresholds and retrospective later-row invalidation.
14. Order-block logic scans later candles and relies on global counters, creating look-ahead and indexing concerns.
15. Liquidity logic uses fixed raw thresholds whose trading interpretation is unresolved.
16. Strategy state relies on globals and does not implement a complete event-time-safe order lifecycle.
17. Existing offline tests exercise syntax and FVG behavior only.
18. The historical successful workflow result is associated with a different commit from the reviewed `main`.
19. The historical workflow returned no artifacts despite artifact upload being configured.
20. No current-commit test execution, backtest, paper trade, live trade, broker connection, or profitability evaluation was performed.

## 5. Unresolved requirements

The following decisions remain unresolved and must not be replaced with invented defaults:

- exact H1 order-block definition;
- exact FVG definition and boundary convention;
- body-versus-wick zone boundaries;
- bullish, bearish, and doji handling;
- event-time relationship between H1 and M15 candles;
- completed-candle convention;
- entry type, entry price, trigger, expiry, and retest policy;
- liquidity event definition;
- liquidity-based stop level and offset;
- spread and slippage treatment;
- trading session and daylight-saving handling;
- maximum holding period;
- maximum concurrent positions;
- aggregate open risk;
- combined GBPJPY/USDJPY JPY exposure limit;
- daily loss and drawdown limits;
- cooldown and retry limits;
- interpretation of the 2–3 trades-per-day aspiration;
- chronological evaluation splits;
- untouched holdout policy;
- cost model;
- performance metrics;
- uncertainty reporting;
- promotion thresholds.

The approved numerical concepts are limited to an intended maximum risk of 2% of current equity per trade, an intended target of exactly 2R, and an H1-context/M15-confirmation sequence. Their production implementation remains incomplete.

## 6. Missing data and execution capabilities

Unavailable or not performed:

- raw workflow log contents;
- workflow test count and individual result lines;
- tested commit as printed by the workflow;
- Python version from the run log;
- artifact name, ID, size, and SHA256;
- local Python execution;
- repository test execution by this inspection;
- current-commit workflow dispatch or rerun;
- workflow-log reading;
- artifact contents;
- broker connection or MT5 authentication;
- account equity, currency, contract, tick, volume, quote, cost, or constraint data;
- independent symbol-specific GBPJPY and USDJPY datasets;
- backtest;
- paper trade;
- live trade;
- profitability evidence;
- binary research materials such as screenshots, PDFs, and Pages documents.

## 7. One prioritised implementation task

**Task:** Create and validate a secret-free, broker-free offline numerical-validation boundary.

**Assigned agent:** Engineering agent, with QA review and Risk/Product Owner approval.

**Dependencies:**

1. Rotate and remove exposed broker credentials through an approved security change.
2. Resolve the exact current `main` revision to be tested.
3. Obtain approved Q01–Q11 definitions for zones, confirmation, entry, stop, session, holding period, limits, and evaluation.
4. Obtain symbol-specific, provenance-preserving GBPJPY and USDJPY data.
5. Define the required runtime dependency manifest.

**Acceptance criteria:**

- Importing application calculation modules performs no MT5 initialization, login, account access, or credential access.
- Deterministic pure functions exist for approved FVG, OB, liquidity, 2R, and fail-closed sizing calculations.
- Tests cover completed-candle handling, timestamp and symbol provenance, look-ahead prevention, 2R directionality, invalid stop geometry, missing sizing inputs, cost-inclusive risk, and volume constraints.
- The workflow runs against the exact reviewed `main` commit.
- The raw log records the tested commit, Python version, test count, individual test results, and artifact metadata.
- No tradable volume is produced when required account, contract, cost, quote, or broker-constraint data are missing.
- Evidence is independently reviewed before any paper-trading consideration.

This task must be proposed only; no repair, rerun, or implementation was performed here.

## 8. Observable usage and cost

Observable usage and cost are unverified.

No broker connection, MT5 session, order, paper trade, live trade, backtest, paid service, or resource-consumption record was supplied. The workflow metadata indicate a historical GitHub Actions run, but no billing, runner cost, artifact storage cost, or other usage cost was provided. No cost estimate is made.
