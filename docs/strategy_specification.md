# Project Mayhem — strategy specification

Updated: 18 October 2026. Version: 0.1. Status: initial documentation baseline.

Paths in this document are relative to the project root unless a Markdown link is used.

## Status and interpretation

This is a requirements baseline, not a claim that the strategy is profitable or fully specified. “Confirmed brief” means explicitly stated by the owner in the current conversation. “Observed” means present in the uploaded code or notes. “Proposed” requires a decision before it becomes an executable trading rule. Where a rule is unresolved, research can continue but agents must not silently invent live behaviour.

## Requirements from the current owner brief

| ID | Requirement | Status / implementation implication |
|---|---|---|
| S01 | Trade GBPJPY and USDJPY | Confirmed brief; independent pair state and identification required |
| S02 | Find hourly imbalance, FVG and/or order-block areas, then inspect M15 | Confirmed brief; H1 context must precede entry confirmation |
| S03 | Enter only after the required M15 imbalance, FVG and/or OB condition | Confirmed brief; exact trigger and Boolean combinations unresolved |
| S04 | Initial planned reward:risk exactly 2:1 | Confirmed initial brief; define R from entry to stop before sizing |
| S05 | Place stop using relevant liquidity against the trade | Confirmed concept; level selection, buffer and invalidation unresolved |
| S06 | Initial intended risk no greater than 2% per trade | Confirmed initial ceiling; sizing and gap/slippage treatment in risk policy |
| S07 | Seek approximately 2–3 trades per day | Owner objective; not evidence that that many valid opportunities exist |
| S08 | Avoid trades lasting multiple hours | Owner objective; numeric holding limit and time exit unresolved |
| S09 | Analyse each trade and improve the system | Owner objective; separate logging from validated release changes |
| S10 | Possible later risk up to 5% and targets up to 4R | Original future intent; not initial settings or automatic escalation permission under these documents |

The assistant recommended no forced trade quota, reviewed releases, and no automatic risk escalation. These remain explicitly proposed operating choices; see [decision log](decision_log.md).

## Intended event sequence

1. Read instrument-specific market data and check freshness, completeness and session eligibility.
2. Identify an H1 area using only information available at that event time.
3. Record when the area becomes knowable, its boundaries, direction, and invalidation state.
4. Observe the required interaction between price and that H1 area.
5. Evaluate the agreed M15 confirmation in the required temporal relationship to the H1 event.
6. Choose the approved entry and liquidity-based invalidation level. Reject invalid geometry.
7. Derive the 2R target and valid position size, then apply portfolio and execution checks.
8. In offline/paper evaluation, record every signal, rejection, fill, exit, cost and reason.
9. Review outcomes in batches and propose versioned changes; do not continuously rewrite a running strategy.

Steps involving undefined conditions are specification work, not executable permission. M1 data may later help with timing and fills, but the owner did not specify M1 as an additional strategy signal.

## Initial price geometry

For an entry E and stop S, define the positive price risk distance d = |E − S|.

| Direction | Required stop geometry | Initial target |
|---|---|---|
| Long | S < E | E + 2d |
| Short | S > E | E − 2d |

Reject d <= 0 and quantities below a valid broker minimum after rounding down. Planned 2R describes price geometry; net realised reward:risk can differ due to costs and fills. Do not move a structural stop simply to manufacture a desirable ratio. A time exit can realise less than 2R and must be modelled explicitly.

## Existing logic — observed, not endorsed

| Source | Observed rule | Specification concern |
|---|---|---|
| `FairValueGap.py::search_for_fvg` | Three candles; bullish/bearish middle candle, extra body conditions, outer-candle gap | Formation requires the next candle; current output Date is the middle candle, not confirmation time |
| Same module | Bullish branch uses outer total range > 0.00005; bearish branch uses gap > 0.00005 | Asymmetric thresholds; neither approved for JPY pairs |
| `FairValueGap.py::check_fvg` | Scans later rows for penetration past a boundary | Distinguish currently surviving zones from zones tradable earlier |
| `OrderBlockAnalysis.py::Analyse_Data` | Opposite-colour following candles and possible preceding-candle merge | First-row wraparound; formation and confirmation timing unresolved |
| `OrderBlockAnalysis.py::OB_check` | Containment then activation/invalidation based on later crossings | Directional semantics must be reconciled with strategy intent |
| `Liquidity.py::find_liq` | Wick-based thresholds include 0.06 and 0.00018 | Instrument scale, units and branch consistency unresolved |
| `Strategy.py::check_if_in_ob_hr` | Current M1 candle body overlaps an OB body area | Body versus wick and completed versus current candle not approved |
| `Strategy.py::run_strategy_check` | OB chain plus a separate FVG branch | Separate branch can bypass an hourly context; not proof of S02 compliance |
| `Strategy.py::correct_dir` | “Bullish” checks Close below Open; “Bearish” checks Close above Open | Labels and intended continuation/reversal need clarification |
| `Strategy.py::check_trading_time` | Local machine clock with 07:00–02:00 overnight interval | Not an approved London/New York session definition |

`docs/Strategy.txt` mentions liquidity sweeps, reversals, retracement and news as planning questions. They must not silently become mandatory filters. The RSI/engulfing example in that document is illustrative, not this project's approved strategy.

## Unresolved owner decisions

| Decision | Required clarification | Blocking scope |
|---|---|---|
| Q01 | Are imbalance and FVG synonyms or distinct detectors? Exact inequalities and minimum size? | Signal implementation |
| Q02 | OB direction, body/wick bounds, merge rules, displacement, confirmation, mitigation and invalidation? | Signal implementation |
| Q03 | Does M15 confirmation have to form after the H1 touch? Same direction? Inside the H1 area? | Entry implementation |
| Q04 | Is the trigger any one zone, an ordered combination, or a separate variant per zone? | Entry implementation |
| Q05 | Market versus limit entry; close confirmation versus intrabar action; expiry? | Fill simulation |
| Q06 | Which liquidity level sets the stop, with what buffer and minimum/maximum distance? | Sizing and exits |
| Q07 | Exact sessions, timezone, DST handling, rollover and news exclusions? | Session filters |
| Q08 | Numeric maximum holding time and forced-exit rule? Overnight/weekend handling? | Duration rule |
| Q09 | Is the 2–3 objective combined across pairs? Hard daily maximum? Re-entry and cooldown? | Frequency controls |
| Q10 | Per-trade configured risk, combined open risk, daily loss and drawdown limits? | Portfolio gate |
| Q11 | Required sample size, evaluation periods and performance thresholds? | Promotion decisions |

## Acceptance criteria for the first implementation cycle

- Synthetic positive, negative and boundary fixtures establish each approved rule and its earliest usable timestamp.
- No entry uses an incomplete confirmation candle unless an explicit intrabar rule is approved and tested.
- An M15-only opportunity cannot trigger an H1-context strategy.
- Pair state is separate; changing one pair's data cannot mutate the other's signals.
- Replaying the same data and configuration yields the same outputs without duplicate entries.
- Entry, stop, target and volume satisfy geometry, instrument constraints and approved risk checks.
- No future row changes an already-issued historical decision; later invalidation updates state prospectively.
- Ambiguous intrabar stops/targets use finer data or a declared conservative assumption.
- Results distinguish gross and net performance, costs and rejected opportunities.

These criteria define engineering behaviour; profitability thresholds remain Q11.
