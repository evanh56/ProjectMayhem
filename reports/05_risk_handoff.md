# Numerical Validation and Risk/Execution Handoff

**Status:** No live or paper trading is authorised. No account was accessed, no credentials were used, no orders were placed, and no repository changes were made.

## Repository and revision observed

- Repository: `evanh56/ProjectMayhem`
- Branch: `main`
- Observed commit: `91860a951ea08e205ebbfd8389becce8647ebb7e`
- Source path: `ProjectMayhem/`
- Related branch `fix/offline-testability-m15-append` points to the same observed commit.
- Existing CI run `39128978458` was successful but ran against earlier commit `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`; no artifacts were returned.

## Material inspected

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
- Repository tree, branch and workflow metadata

The source-content responses did not expose complete source bodies or line numbers. Conclusions about implementation defects are therefore limited to the supplied inspection record and documented behaviour.

## Calculation table

| Item | Inputs and units | Formula | Result | Evidence source | Label |
|---|---|---|---|---|---|
| Initial risk budget | Equity \(E\), account-currency units; risk fraction \(r\), dimensionless | \(B = E \\times r\) | Must use current equity and approved \(r \\le 0.02\) | `risk_policy`, D002 | **Policy requirement; not executed** |
| Worked risk budget | \(E = 10{,}000\) account-currency units; \(r = 0.02\) | \(10{,}000 \\times 0.02\) | \(200\) account-currency units | Supplied engineer handoff | **Independently derived arithmetic; not tool-executed** |
| 2R distance | Entry \(P_e\), stop \(P_s\), quote-price units | \(d = |P_e-P_s|\) | Positive distance required | User instruction | **Approved calculation rule** |
| Long target | \(P_e\), \(d\), quote-price units | \(TP = P_e + 2d\) | Determined from supplied entry and stop | User instruction, D002 | **Approved calculation rule** |
| Short target | \(P_e\), \(d\), quote-price units | \(TP = P_e - 2d\) | Determined from supplied entry and stop | User instruction, D002 | **Approved calculation rule** |
| Long worked example | Entry 200.00, stop 199.80, quote-price units | \(d=|200.00-199.80|=0.20\); \(TP=200.00+2(0.20)\) | \(d=0.20\); target 200.40 | Supplied engineer handoff | **Independently derived arithmetic; not tool-executed** |
| Short worked example | Entry 200.00, stop 200.20, quote-price units | \(d=|200.00-200.20|=0.20\); \(TP=200.00-2(0.20)\) | \(d=0.20\); target 199.60 | User-specified formula applied to proposed values | **Independently derived arithmetic; not tool-executed** |
| Invalid 2R inputs | \(d=0\), or side not `long`/`short` | Reject if \(d \\le 0\) or side invalid | No target produced | User instruction | **Required deterministic control** |
| Risk per volume | Entry/stop distance in price units; tick size in price units; tick value in account currency per tick per volume unit; volume \(v\) | \(\text{gross stop loss}=v \\times (d/\text{tick size}) \\times \text{tick value}\) | Requires verified broker specification | `risk_policy` | **Required formula; not numerically executable from supplied data** |
| Cost-adjusted risk | Gross stop loss; spread, commission, expected slippage and other costs in account currency | \(\text{total intended risk}=\text{gross stop loss}+\text{spread cost}+\text{commission}+\text{slippage allowance}\) | Must not exceed risk budget | `risk_policy`, `data_dictionary` | **Required control; cost values missing** |
| Maximum unrounded volume | Risk budget \(B\), per-volume loss \(L_v\), account currency | \(v_{\max}=B/L_v\) | Cannot calculate without verified \(L_v\) | `risk_policy` | **Required formula; no lot size invented** |
| Broker-rounded volume | \(v_{\max}\), volume step \(s\) | \(v_{\text{rounded}}=\lfloor v_{\max}/s\rfloor s\) | Round down only | `risk_policy` | **Required deterministic control** |
| Minimum-volume check | Rounded volume; broker minimum \(v_{\min}\) | Reject if \(v_{\text{rounded}}<v_{\min}\) | No order if minimum exceeds risk budget | `risk_policy` | **Required deterministic control** |

### Missing sizing inputs

A tradable lot size cannot be calculated from the supplied material. Required inputs are missing or unverified:

1. Current account equity.
2. Account currency.
3. Symbol-specific contract size.
4. Tick size.
5. Tick value and whether it is quoted in account currency.
6. Volume minimum, maximum and step.
7. Verified entry and stop prices.
8. Bid/ask spread at submission.
9. Commission schedule.
10. Slippage allowance or execution-cost model.
11. Currency conversion rates for any non-account-currency profit or loss.
12. Margin and stop/freeze-level restrictions.
13. Symbol identity and broker specification for both GBPJPY and USDJPY.

The supplied CSVs do not provide these values. No lot size, pip value or conversion rate should be inferred.

## Intended stop risk versus realised loss

The 2% value is an **intended risk budget**, not a guaranteed maximum realised loss.

Realised loss can exceed the calculated stop risk because:

- a gap can cause the stop to fill away from its stop price;
- fast-market slippage can exceed the configured allowance;
- spread widening can trigger or worsen execution;
- stop/freeze restrictions can delay or reject protective-order changes;
- connection loss can prevent submission, modification or closure;
- partial fills can leave residual exposure;
- commissions and financing costs add to the loss;
- a rejected or missing protective order can leave the position unprotected;
- restart or reconciliation failures can cause local state to differ from broker state.

The application must report both:

- **planned/intended risk** at submission; and
- **actual realised loss** after fills, costs and conversion.

It must not describe the stop as a guaranteed loss limit.

## Combined GBPJPY and USDJPY exposure

The two instruments share JPY as the quote currency:

- A **long GBPJPY** is long GBP and short JPY.
- A **long USDJPY** is long USD and short JPY.
- Holding both long positions creates combined short-JPY exposure.
- A **short GBPJPY** and **short USDJPY** create combined long-JPY exposure.
- Opposing positions may reduce directional JPY exposure but still retain basis, spread, timing, and instrument-specific risks.
- GBPJPY also carries GBP exposure; USDJPY carries USD exposure. They are not interchangeable or perfectly hedged.

The application must calculate exposure from actual position quantities and current conversion rates, then aggregate:

1. gross notional exposure;
2. net JPY exposure;
3. directional exposure by instrument;
4. aggregate open risk to protective stops;
5. exposure after pending orders and partial fills.

No numerical combined exposure can be calculated because no positions, quantities, prices, contract specifications or conversion rates were supplied.

## Missing account-level limits

The approved material specifies only an initial maximum intended risk of **2% per trade** and a planned **2R** target. The following remain undefined and must be treated as missing configuration rather than unlimited:

- maximum concurrent positions;
- maximum aggregate open risk;
- maximum combined JPY exposure;
- maximum gross and net portfolio exposure;
- daily loss limit;
- daily realised plus unrealised loss treatment;
- maximum drawdown;
- maximum trades per day;
- per-symbol trade limits;
- cooldown after a loss or rejected order;
- maximum holding period;
- spread, slippage and stale-data thresholds;
- news or market-closure restrictions;
- emergency shutdown threshold.

Orders must fail closed when any required limit is undefined.

## Required deterministic execution controls

The application must reject or halt in the following cases:

### Stale or incomplete data

Reject the signal when:

- quote age exceeds the approved threshold;
- bid or ask is missing, non-finite or inconsistent;
- the candle is not confirmed complete;
- symbol, timeframe, timezone or broker identity is missing;
- required H1/M15 history is incomplete;
- spread exceeds its approved bound.

### Rejected or partially filled orders

- Record broker request and response identifiers.
- Do not assume rejection means no exposure; reconcile actual broker positions.
- For a partial fill, recalculate residual risk and attach protection to the filled quantity.
- Reject or cancel the remainder if the resulting exposure would breach limits.
- Do not resubmit blindly.

### Duplicate submissions

Use a deterministic client order identifier derived from strategy signal, symbol, side and signal timestamp. Before submission and after timeout:

- check local idempotency state;
- query broker orders and positions;
- suppress a duplicate if an equivalent order or position exists;
- use bounded retries only.

### Disconnects and timeouts

- Enter a fail-closed state.
- Stop new submissions.
- Reconnect with bounded retry count and timeout.
- Reconcile broker orders, positions and fills before resuming.
- Escalate if reconciliation cannot be completed.
- Do not infer broker state from local CSV files.

### Restart and reconciliation

On startup or restart:

1. load local state;
2. query broker positions, orders, fills and account equity;
3. compare broker state with local state;
4. identify unknown, duplicate, orphaned or unprotected positions;
5. halt new trading until discrepancies are resolved;
6. verify protective orders for every open position.

### Protective orders

A position must not be considered valid unless its stop and target status are confirmed. The system must:

- verify protective orders after fill;
- reject or immediately escalate an unprotected position;
- never widen a stop;
- never average down or increase risk after a loss;
- avoid changing approved controls after an individual trade.

### Emergency shutdown

A deterministic emergency stop must:

- prevent new orders;
- cancel eligible pending orders;
- attempt protection or closure according to an owner-approved procedure;
- preserve audit logs;
- reconcile final broker state;
- require explicit operator review before resumption.

## Credential handling

Credential locations identified in the supplied material:

- `ProjectMayhem/main.py`, including documented module-level authentication assignments and an `mt.login` call.

Credential values are intentionally not reproduced.

Required actions:

- remove embedded credentials from source;
- rotate any credentials that may have been committed;
- use secret management for any future broker-connected environment;
- remove import-time broker login side effects;
- keep offline tests secret-free;
- do not connect to an account for this validation.

## Prioritised paper-trading blockers

Paper trading should not begin until the following are resolved:

### P0 — hard blockers

1. Remove credential exposure and import-time broker side effects.
2. Define Q01–Q11, including entry, stop, confirmation timing, sessions and holding period.
3. Define aggregate open-risk, concurrency, daily-loss, drawdown and JPY-exposure limits.
4. Implement and test fail-closed sizing using verified symbol and account-currency specifications.
5. Implement broker-state reconciliation, duplicate prevention, partial-fill handling and protective-order verification.
6. Supply identified, timezone-aware GBPJPY and USDJPY data with candle-completion metadata.
7. Establish spread, commission and slippage assumptions.

### P1 — required before meaningful numerical evaluation

8. Add deterministic tests for 2R geometry, sizing, rounding, minimum volume and invalid inputs.
9. Add no-look-ahead H1/M15 temporal-join tests.
10. Add immutable signal/order/fill/trade records with unique identifiers.
11. Re-run CI at the current commit and retain readable artifacts.
12. Establish chronological development, validation and untouched evaluation windows.

### P2 — required before any promotion decision

13. Demonstrate paper execution over an approved evaluation period.
14. Reconcile every order, fill, position, cost and equity update with the broker.
15. Measure realised loss, slippage, rejected orders, disconnections, duplicate attempts and protection failures.
16. Obtain independent QA/risk review and product-owner approval.

## Checks executed

**None.**

No repository code was run, no dependencies were installed, no workflow was dispatched or rerun, no broker or MT5 session was opened, and no paper or live order was submitted.

The arithmetic examples above are independently derived from stated inputs and formulas; they are not tool-executed results.

## Assumptions and blockers

- The 2% figure is the approved initial maximum intended per-trade risk, not a guarantee of realised loss.
- The 2R target is approved, but entry and stop definitions are unresolved.
- Undefined controls are missing configuration and must fail closed.
- Existing FVG tests are narrow implementation expectations, not approval of the complete trading strategy.
- No numerical lot size is available or appropriate without broker specifications and account-currency conversion.
- No profitability, drawdown, execution-quality or trading-edge conclusion is justified.

## Recommendation

**Release recommendation: Reject for paper trading and live trading.**

The repository does not yet provide a numerically validated, operationally reliable implementation of the approved GBPJPY/USDJPY strategy. The release is blocked by unresolved strategy and account-level limits, absent verified instrument metadata and cost inputs, incomplete execution controls, credential/import risks, lack of reconciliation evidence, and absence of current-revision numerical tests.

Final release authority remains with the product owner.
