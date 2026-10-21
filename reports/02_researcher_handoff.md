# Offline Testing and Numerical Validation Handoff

## 0. Repository, branch, and evidence basis

- **Repository:** `evanh56/ProjectMayhem`
- **Branch inspected:** `main`
- **Current observed commit:** `8feb36db91d7144b4a190a302634ddd30c449c0b`
- **Observed commit message:** Merge pull request #2 from `improvement/offline-foundation-v1`
- **Source path:** `ProjectMayhem/`; no legacy `src/ProjectMayhem/` directory was present.
- **Historical CI run observed:** run `39128978458`, head `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8`, conclusion `success`.
- **Important limitation:** the historical CI head differs from the current `main` head. The current commit was not shown to have run successfully.
- **No local test execution, broker connection, MT5 authentication, backtest, paper trade, or live trade was performed.**
- **No profitability conclusion is supported.**

### Files and records inspected

Repository inspection covered:

- `ProjectMayhem/main.py`
- `ProjectMayhem/FairValueGap.py`
- `ProjectMayhem/OrderBlockAnalysis.py`
- `ProjectMayhem/Liquidity.py`
- `ProjectMayhem/Strategy.py`
- `ProjectMayhem/Execution.py`
- seven CSV snapshots under `ProjectMayhem/`
- `tests/test_offline.py`
- `.github/workflows/offline-tests.yml`
- `requirements-ci.txt`
- the supplied documentation digest:
  - `docs/project_overview.md`
  - `docs/Strategy.txt`
  - `docs/data_dictionary.md`
  - `docs/decision_log.md`
  - `docs/experiment_log.md`
  - `docs/risk_policy.md`
  - `docs/strategy_specification.md`

Screenshots, PDFs, Pages files, and other binary research materials were **not reviewed**, because their contents were not supplied.

---

# 1. Intended strategy versus implementation and test expectations

## 1.1 Confirmed intended requirements

The following are owner requirements or decision-log requirements:

| Requirement | Status | Source |
|---|---|---|
| Instruments are GBPJPY and USDJPY | Confirmed | `project_overview`; D001 |
| Use hourly context and 15-minute confirmation | Confirmed | `project_overview`; D001 |
| Initial target is exactly 2R | Confirmed | `project_overview`; `risk_policy`; D002 |
| Intended maximum risk is 2% of current equity per trade | Confirmed | `project_overview`; `risk_policy`; D002 |
| Seek approximately 2–3 trades per day | Owner-stated aspiration, not fully operationalised | D003 |
| Do not force trades when no valid setup exists | Confirmed | D009 |
| Fail closed when execution controls are undefined | Confirmed | `risk_policy` |
| No live or paper execution is authorised by these documents | Confirmed | `project_overview`; `risk_policy` |

The intended strategy does **not** yet define the precise OB, FVG, liquidity, direction, confirmation, entry, stop, session, or holding-period calculations.

## 1.2 Implemented behaviour

| Area | Implemented behaviour | Reconciliation |
|---|---|---|
| Symbol | `main.py` uses hard-coded `GBPJPY` | Incomplete: no independent USDJPY stream; filenames are `GBPUSD_*` |
| Timeframes | Retrieves M15 and H1 data, with M1 data also present | Broadly consistent with H1/M15 intent, but current-bar handling is unsafe |
| FVG | Detects three-candle structures using candle body direction, fixed price thresholds, and later-row invalidation | Implementation detail, not an approved strategy definition |
| Order blocks | Direction is based on `Open - Close > 0`; later candles are scanned for containment, activation, and invalidation | Not reconciled to an approved OB definition; look-ahead risk exists |
| Liquidity | Uses fixed wick thresholds and stores a high or low as the liquidity level | No approved definition of liquidity sweep or stop placement exists |
| Direction confirmation | `Strategy.py` uses global state and later candle checks | Incomplete and not event-time-safe |
| Session | `Strategy.py` checks `07:00` to `02:00`, crossing midnight | This is implemented behaviour, not an owner-approved session |
| Entry | No complete entry rule or order construction | Unresolved |
| Stop | `Execution.py` contains experimental arithmetic and `Sl = 350`; no validated liquidity stop | Not compliant with risk policy |
| Take-profit | No complete implementation | Only the 2R target is approved |
| Execution | `taketrade()` prints `"Work in progress"` and returns | No order placement exists |
| Risk sizing | Uses balance-derived arithmetic rather than current equity, stop-loss loss, contract data, costs, and broker constraints | Not approved and not compliant |

Sources: `main.py`, `FairValueGap.py`, `OrderBlockAnalysis.py`, `Liquidity.py`, `Strategy.py`, `Execution.py`; `risk_policy`; `data_dictionary`.

## 1.3 What `tests/test_offline.py` actually establishes

The current offline tests:

1. Parse all Python files under `ProjectMayhem/` for syntax.
2. Dynamically load only `ProjectMayhem/FairValueGap.py`.
3. Test four FVG cases:
   - bullish gap detected;
   - bearish gap detected;
   - overlapping outer candles rejected;
   - later boundary breach removes the gap.

They do **not** test:

- MT5 isolation or import side effects;
- credentials;
- USDJPY handling;
- completed-candle filtering;
- timestamp provenance;
- OB logic;
- liquidity logic;
- Strategy direction or session logic;
- entry, stop, take-profit, or sizing;
- order placement;
- duplicate prevention or trade lifecycle;
- current `main` commit specifically.

The FVG tests therefore validate selected implementation behaviour only. They do not approve the FVG formula as the trading specification.

---

# 2. Approved calculations and unresolved decisions Q01–Q11

## 2.1 Calculations currently approved

Only the following numerical concepts are approved:

### Target

- **Target multiple:** exactly **2R**.
- Source: `project_overview`, `risk_policy`, D002.
- Exact entry, stop, price basis, and order type remain unresolved.

### Intended per-trade risk

- **Maximum intended risk:** **2% of current equity per trade**.
- Source: `project_overview`, `risk_policy`, D002.
- Required sizing inputs include current equity, approved risk fraction, stop-loss loss, contract information, account currency, commission, execution costs, broker volume constraints, and fresh quote.
- No production calculation currently implements this policy.

### Timeframe sequence

- H1 context followed by M15 confirmation.
- Source: D001 and `project_overview`.
- The exact event-time relationship remains unresolved.

## 2.2 Unresolved calculations and decisions

| Question range | Unresolved item | Required decision |
|---|---|---|
| **Q01–Q04** | Zone definitions | Define exact H1 OB and FVG conditions, boundaries, direction labels, and whether zones use bodies, wicks, or both |
| **Q01–Q04** | Direction labels | Define bullish/bearish semantics, including doji candles and conflicting OB/FVG directions |
| **Q01–Q04** | Confirmation timing | Define which completed H1 and M15 bars may be used and the earliest executable timestamp |
| **Q05–Q08** | Entry rule | Define market, limit, or stop entry; entry price; trigger candle; expiry; and whether retests are permitted |
| **Q05–Q08** | Liquidity stop | Define liquidity event, reference level, stop offset, spread treatment, and invalidation |
| **Q05–Q08** | Session | Resolve London, New York, Asia, or another session; define timezone and daylight-saving treatment |
| **Q05–Q08** | Maximum holding period | Define bars, hours, session close, and handling of open positions at expiry |
| **Q09–Q10** | Portfolio limits | Define aggregate open risk, JPY exposure, concurrent trades, daily loss, drawdown, cooldown, and frequency semantics |
| **Q09–Q10** | Frequency | Clarify whether 2–3 trades/day is a cap, target, or observation |
| **Q11** | Evaluation evidence | Define chronological splits, untouched holdout, cost assumptions, metrics, uncertainty reporting, and promotion thresholds |

Additional unresolved items include spread, commission, slippage, data freshness, price basis, contract specification, stop/freeze levels, and account-currency conversion. Sources: `risk_policy`, `data_dictionary`, D003, Q01–Q11 decision entries.

---

# 3. Review of FVG, OB, liquidity, and confirmation timestamps

## 3.1 Fair Value Gap boundaries

### Implemented bullish formula

For a candidate current candle:

```text
current close > current open
previous high < current close
next low > current open
next high - previous low > 0.00005
```

Stored bullish fields:

```text
Prev_candle = previous high
Next_candle = next low
```

The effective candidate gap is therefore approximately:

```text
[previous high, next low]
```

### Implemented bearish formula

```text
current close < current open
previous low > current close
next high < current open
previous low - next high > 0.00005
```

Stored bearish fields:

```text
Prev_candle = previous low
Next_candle = next high
```

The effective bearish gap is approximately:

```text
[next high, previous low]
```

### Invalidation

Later rows invalidate:

- bullish FVG if later `Close < Next_candle` or `Low < Next_candle`;
- bearish FVG if later `Close > Next_candle` or `High > Next_candle`.

### Issues

- `0.00005` is a raw price threshold and is not normalised for GBPJPY or USDJPY precision.
- The detector needs a future candle to identify the three-candle structure.
- The later-row invalidation scan makes the stored result a retrospective snapshot rather than an immutable event.
- The output does not preserve the full event context, confirmation timestamp, symbol, broker, price basis, or completion status.
- The tests expect these implementation boundaries, but do not establish that they are the intended trading boundaries.

Sources: `FairValueGap.py`, `tests/test_offline.py`, `data_dictionary`.

## 3.2 Order-block direction and boundaries

Implemented direction:

```python
Open - Close > 0  => bearish
otherwise         => bullish
```

Consequences:

- A doji or equal-open/close candle is classified as bullish.
- This behaviour is not documented as an approved strategy rule.

Strategy zone bounds:

- bullish: bottom `Open`, top `Close`;
- bearish: bottom `Close`, top `Open`.

`OrderBlockAnalysis.py` also uses the candle body with:

```text
lo_body = min(Open, Close)
hi_body = max(Open, Close)
```

The module scans later candles for containment, activation, and invalidation. This introduces possible look-ahead and indexing effects. The output is not a time-stamped immutable OB event history.

The approved strategy definition of an OB remains unresolved under Q01–Q04.

## 3.3 Liquidity levels

Observed candidate rules include:

- bearish candle: `Close - Low > 0.06`, with level based on `Low`;
- bullish candle: `High - Close > 0.06`, with level based on `High`;
- secondary wick thresholds of `0.00018`.

Problems:

- The thresholds use raw price units and are not instrument-normalised.
- The relationship between the `0.06` and `0.00018` branches is unclear.
- It is not defined whether a level is a swing high/low, wick extreme, equal high/low, or another liquidity pool.
- There is no approved rule for what constitutes a liquidity sweep.
- There is no approved stop offset or spread/slippage treatment.

The liquidity stop remains unresolved under Q05–Q08.

## 3.4 Confirmation timestamps

Observed timestamp risks:

- MT5 retrieval starts at position zero, so the latest bar may still be forming.
- Timestamps are converted to Europe/London and then made timezone-naive.
- CSVs lack completion metadata, UTC offset, symbol, price basis, and extraction provenance.
- FVGs use a three-candle structure but are later invalidated using future rows.
- OBs and liquidity records are derived using later candles.
- Strategy state uses global variables and does not establish a complete event-time sequence.

Required interpretation:

- No signal may use a candle before its close.
- H1/M15 joins must use only information available at the confirmation event.
- A zone invalidated by a later candle must not be treated as known-invalid before that later candle closes.
- The earliest executable timestamp must be explicitly defined in Q03–Q04 and Q05.

This is a required data-integrity rule, but the exact timestamp convention remains unresolved.

---

# 4. Proposed worked acceptance examples

The following are **proposed acceptance examples only**. They are not current requirements, do not demonstrate that the repository passes, and must not be treated as trading instructions until approved.

## Example A — Proposed bullish FVG boundary

**Assumptions**

- **A1, proposed:** prices are comparable decimal price units.
- **A2, proposed:** all three candles are completed M15 candles.
- **A3, proposed:** the detector uses the repository’s current formulas.
- **A4, proposed:** the gap is represented as a closed/open interval according to an explicitly agreed convention; that convention is currently unresolved.

Inputs:

| Candle | Open | High | Low | Close |
|---|---:|---:|---:|---:|
| Previous | 199.00 | 199.20 | 198.90 | 199.10 |
| Current | 199.30 | 199.90 | 199.25 | 199.80 |
| Next | 199.90 | 200.00 | 199.85 | 199.95 |

Expected implementation output:

```text
Position    = Bullish
Prev_candle = 199.20
Next_candle = 199.85
Gap bounds  = [199.20, 199.85]  # proposed representation
```

The outer candles do not overlap because:

```text
previous high = 199.20 < next low = 199.85
```

This matches the expectations asserted in `tests/test_offline.py`.

## Example B — Proposed bullish FVG invalidation

**Assumptions**

- **A5, proposed:** invalidation is assessed only after the later M15 candle has closed.
- **A6, proposed:** the current implementation’s bullish invalidation rule is retained.

Existing bullish boundary:

```text
Next_candle = 199.85
```

Later completed candle:

```text
Low   = 199.80
Close = 199.90
```

Expected implementation result:

```text
FVG removed
```

Reason:

```text
later low 199.80 < bullish boundary 199.85
```

The timestamp at which the removal becomes knowable is the close time of the later candle, not the original FVG timestamp.

## Example C — Proposed OB direction and zone

**Assumptions**

- **A7, proposed:** retain the current body-based direction rule.
- **A8, proposed:** the OB zone contains only the candle body.
- **A9, proposed:** prices are JPY-pair price units.

Input candle:

```text
Open  = 200.10
High  = 200.40
Low   = 199.80
Close = 199.90
```

Expected output under the current implementation:

```text
Open - Close = 0.20 > 0
Direction    = Bearish
Zone bottom  = 199.90
Zone top     = 200.10
```

This is an implementation acceptance example, not an approved OB definition. An equal-open/close candle would currently be classified bullish; that behaviour requires an owner decision.

## Example D — Proposed liquidity level

**Assumptions**

- **A10, proposed:** use the repository’s `0.06` threshold.
- **A11, proposed:** the level is the candle wick extreme.
- **A12, proposed:** no spread or offset is added for this detector test.

Input bullish candle:

```text
High  = 200.50
Close = 200.40
High - Close = 0.10
```

Expected detector output:

```text
Liquidity type  = High
Liquidity level = 200.50
Candidate       = accepted because 0.10 > 0.06
```

This does not define a valid trading stop. Sweep semantics and stop placement remain unresolved.

## Example E — Proposed 2R target arithmetic

**Assumptions**

- **A13, proposed:** long entry and stop are known at execution.
- **A14, proposed:** `R` is the absolute entry-to-stop price distance.
- **A15, proposed:** costs are handled separately and are not included in this simple arithmetic example.

Long trade:

```text
Entry = 200.00
Stop  = 199.70
R     = 200.00 - 199.70 = 0.30
```

Approved target multiple:

```text
Target = Entry + 2R
       = 200.00 + 0.60
       = 200.60
```

Short equivalent:

```text
Entry = 200.00
Stop  = 200.30
R     = 0.30
Target = 200.00 - 0.60 = 199.40
```

These examples demonstrate the 2R arithmetic only. They do not approve the entry or stop calculation.

## Example F — Proposed event-time acceptance

**Assumptions**

- **A16, proposed:** an H1 candle labelled 10:00 represents the interval 10:00–11:00.
- **A17, proposed:** an M15 candle labelled 11:00 represents the interval 11:00–11:15.
- **A18, proposed:** signals may use only completed candles.

Expected chronology:

```text
H1 context becomes available: after 11:00
M15 confirmation becomes available: after 11:15
Earliest possible execution: after 11:15, subject to the approved entry rule
```

This timestamp convention is proposed because the repository does not preserve sufficient completion metadata to establish the correct convention.

---

# 5. Assumptions, blockers, and next action

## 5.1 Assumptions

All assumptions below are **proposed**, not confirmed requirements:

- Prices in the examples are decimal instrument prices.
- The current FVG formulas are used only to reproduce existing tests.
- FVG boundaries are represented by the two outer-candle levels.
- OB zones use candle bodies rather than full wicks.
- A doji requires an explicit policy rather than inheriting the current bullish fallback.
- Signals use completed candles only.
- Event timestamps should be retained with timezone and completion status.
- Cost-adjusted performance, if later evaluated, must include spread, commission, slippage, and realistic execution timing.
- The 2R target is measured from actual entry and stop prices, not from an assumed candle close.
- The 2% risk limit applies to current equity and must be checked at order submission.
- No numeric default should be substituted for an unresolved control.

## 5.2 Blockers

1. **Current `main` commit has no confirmed test result.**
2. **The only successful CI result is for a different commit and returned no artifacts.**
3. **No local execution was performed in this handoff.**
4. **`main.py` has broker side effects on import.**
5. **Credential assignments exist in `ProjectMayhem/main.py`; values are intentionally not reproduced.**
6. **No complete dependency manifest exists; runtime imports exceed `requirements-ci.txt`.**
7. **GBPJPY runtime selection conflicts with GBPUSD filenames.**
8. **No independent USDJPY data stream is present.**
9. **Latest-candle completion is not established.**
10. **Timezone and provenance metadata are stripped or absent.**
11. **FVG, OB, and liquidity outputs are retrospective or look-ahead-sensitive snapshots.**
12. **OB, liquidity, entry, stop, session, holding-period, and portfolio rules remain unresolved.**
13. **Execution, sizing, stop-loss, take-profit, and order lifecycle are incomplete.**
14. **No evaluation window, cost model, or promotion threshold has been approved.**
15. **Screenshots, PDFs, and Pages documents were not reviewed because contents were not provided.**

## 5.3 Recommended next action

Prioritised next steps:

1. **Preserve evidence and rotate/remove exposed credentials** without reproducing them.
2. **Create a secret-free offline harness** so importing application modules cannot initialise MT5 or authenticate.
3. **Run the offline workflow against the exact current `main` commit** and retain test logs and artifacts.
4. **Add tests for import isolation, completed-candle filtering, timestamp preservation, symbol identity, and CSV validation.**
5. **Resolve Q01–Q08 before numerical strategy testing:** zone definitions, direction, confirmation, entry, liquidity stop, session, and holding period.
6. **Resolve Q09–Q11:** portfolio limits, frequency semantics, evaluation split, costs, metrics, and promotion criteria.
7. **Create symbol-specific, provenance-preserving GBPJPY and USDJPY datasets.**
8. **Implement an event-time-safe reference calculation outside production execution code.**
9. **Compare current formulas against the approved reference implementation using chronological, untouched data.**
10. **Do not derive profitability or approve paper/live promotion until the above controls and evidence exist.**

No profitability, paper-trading, live-readiness, or risk-policy compliance conclusion is supported by the supplied evidence.
