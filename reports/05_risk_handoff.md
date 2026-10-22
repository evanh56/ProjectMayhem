# QA / Trading Risk and Execution Handoff

## Evidence basis

| Item | Result | Evidence |
|---|---|---|
| Repository | `evanh56/ProjectMayhem` | Supplied repository inspection record |
| Branch | `main` | Supplied repository inspection record |
| Observed commit | `8feb36db91d7144b4a190a302634ddd30c449c0b` | Supplied repository inspection record |
| Material inspected | `main.py`, `Execution.py`, `Strategy.py`, `FairValueGap.py`, `OrderBlockAnalysis.py`, `Liquidity.py`, tests, workflow, dependency manifest, seven CSV snapshots, supplied risk and strategy documents | Supplied inspection record and handoffs |
| Historical CI evidence | Run `39128978458` passed at a different head, `ad1e0ee0b4727cbd23e9cb5d97b6e6d0a28476a8` | Supplied GitHub inspection record |
| Current-commit test result | Not established | Historical CI head differs from observed `main` |
| Orders or broker access | None | Supplied inspection record |
| Live or paper authorisation | None | Risk policy |

This handoff does **not** authorise live trading, paper trading, broker connection, credential access, deployment, or limit changes.

---

## Independently derived 2R geometry

The following is arithmetic derived from the requested definition. It was not executed against the repository.

| Case | Inputs and units | Formula | Result | Evidence / label |
|---|---|---|---|---|
| Long example | Entry `200.00` price units; stop `199.70` price units | `d = abs(entry - stop)`; `long target = entry + 2d` | `d = 0.30` price units; target `200.60` price units | Independently derived arithmetic; proposed expected result, not tool-executed |
| Short example | Entry `200.00` price units; stop `200.30` price units | `d = abs(entry - stop)`; `short target = entry - 2d` | `d = 0.30` price units; target `199.40` price units | Independently derived arithmetic; proposed expected result, not tool-executed |
| Zero-distance case | Entry equals stop; `d = 0` price units | Reject when `d == 0` | Rejected | Independently derived validation rule |
| Invalid long-side case | Stop is not below entry | Long-side validation requires a positive protective distance in the expected direction | Rejected | Independently derived validation rule |
| Invalid short-side case | Stop is not above entry | Short-side validation requires a positive protective distance in the expected direction | Rejected | Independently derived validation rule |

The approved strategy target is exactly **2R**. The worked prices above are examples only and are not repository data or trading instructions.

---

## Position-sizing control

The approved risk fraction is no greater than **2%**, represented mathematically as:

```text
risk_fraction <= 0.02
```

The repository does not provide enough verified inputs to calculate a tradable volume.

### Required formula

Let:

```text
risk_budget_account_currency
    = current_equity_account_currency × approved_risk_fraction

stop_distance_ticks
    = abs(entry_price - stop_price) / verified_tick_size

gross_stop_loss(volume)
    = stop_distance_ticks
      × verified_tick_value_account_currency_per_volume_unit
      × volume

total_intended_loss(volume)
    = gross_stop_loss(volume)
      + commission(volume)
      + spread_cost(volume)
      + permitted_slippage_allowance(volume)
```

The valid volume must satisfy:

```text
total_intended_loss(volume) <= risk_budget_account_currency
```

Then:

```text
rounded_volume
    = floor(raw_volume / volume_step) × volume_step
```

The application must reject when:

- required inputs are missing or stale;
- the calculated volume is below the broker minimum;
- the calculated volume exceeds the broker maximum;
- the rounded volume is zero;
- post-rounding loss exceeds the risk budget;
- entry or stop violates price precision, stop-level, or freeze-level rules;
- account currency conversion is unavailable or stale.

`contract_size` must also be verified because tick-value interpretation can depend on the instrument specification and volume convention.

### Required inputs and current availability

| Input | Units | Required use | Current evidence |
|---|---|---|---|
| Current equity | Account currency | Establish the `2%` risk budget | Not supplied as a verified runtime value |
| Account currency | Currency code | Convert instrument loss and costs | Not supplied |
| Approved risk fraction | Decimal fraction, maximum `0.02` | Risk budget | Owner requirement in `risk_policy` |
| Entry price | Instrument price units | Stop distance and execution cost | Entry rule unresolved |
| Stop price | Instrument price units | Stop distance | Liquidity stop and stop rule unresolved |
| Tick size | Instrument price units per tick | Convert price distance to ticks | Not supplied |
| Tick value | Account currency per tick per volume unit | Monetary stop-loss calculation | Not supplied |
| Contract size | Base units per broker volume unit | Validate monetary conversion | Not supplied |
| Volume minimum | Broker volume units | Minimum-volume validation | Not supplied |
| Volume maximum | Broker volume units | Maximum-volume validation | Not supplied |
| Volume step | Broker volume units | Round down deterministically | Not supplied |
| Commission | Account currency per volume or transaction | Include transaction costs | Not specified |
| Spread | Price or account-currency cost | Include entry/exit cost | Not specified |
| Slippage allowance | Price or account-currency cost | Stress intended loss | Not specified |
| Currency conversion rate | Conversion-rate units | Convert loss to account currency | Not supplied |
| Fresh bid/ask quote | Instrument price units | Recheck sizing at submission | Not available without broker data |
| Stop/freeze constraints | Price units | Validate order and protective order placement | Not supplied |

No tradable lot size is calculated or invented.

### Current implementation assessment

`Execution.py::price_to_pip()` is experimental and does not implement the required equity, account-currency, contract, cost, stop-distance, or broker-volume validation. `taketrade()` is a stub and no order-placement path was observed.

---

## Intended stop risk versus realised loss

The intended stop risk is a budgeted estimate, not a guaranteed maximum realised loss.

### Intended calculation

```text
intended_stop_loss
    = price-distance loss at the verified stop
      + commission
      + spread cost
      + defined slippage allowance
```

This must remain no greater than the approved risk budget after volume rounding.

### Circumstances that can exceed intended loss

- price gaps through the stop;
- market slippage during fast movement or news;
- spread widening causing an adverse fill or stop trigger;
- rejected, delayed, or missing protective orders;
- connection loss between signal, entry, and protection;
- partial fill where the protection volume is incomplete;
- broker execution rules differing from the assumed model;
- stale quotes used for sizing;
- incorrect tick-value or currency conversion;
- restart before position reconciliation;
- duplicate entry submission;
- commission or swap costs omitted from the model;
- stop or volume rounding changing the actual exposure.

The application must expose these as risk states and fail closed where protection or sizing cannot be verified.

---

## Combined GBPJPY and USDJPY exposure

For an instrument quoted as `BASE/JPY`, define signed JPY exposure as:

```text
JPY_exposure
    = -direction × base_volume × contract_size × execution_price
```

where:

- `direction = +1` for a long position;
- `direction = -1` for a short position;
- `base_volume × contract_size` is base-currency notional;
- execution price is JPY per unit of base currency.

Therefore:

| Position | Base exposure | JPY exposure |
|---|---|---|
| Long GBPJPY | Long GBP | Short JPY |
| Short GBPJPY | Short GBP | Long JPY |
| Long USDJPY | Long USD | Short JPY |
| Short USDJPY | Short USD | Long JPY |

Two long positions in GBPJPY and USDJPY both create short JPY exposure. Two short positions both create long JPY exposure. Opposite directions can offset JPY exposure, but they still retain separate GBP and USD risks and may not hedge one another reliably.

The portfolio control must calculate, at minimum:

```text
net_JPY_exposure
    = signed GBPJPY JPY exposure
      + signed USDJPY JPY exposure
```

It should also retain:

- gross JPY exposure;
- directional JPY exposure;
- GBP notional;
- USD notional;
- per-symbol open risk;
- aggregate open risk;
- stress loss under adverse JPY movement;
- correlation and concentration flags.

No account positions, volumes, prices, or account currency were supplied. Consequently, no numerical combined exposure is calculated.

---

## Missing account-level limits

The following controls are absent or unresolved and must not be treated as unlimited or zero:

- maximum concurrent positions;
- maximum concurrent positions per symbol;
- maximum aggregate open risk;
- maximum combined JPY exposure;
- maximum gross notional;
- maximum daily loss;
- maximum drawdown;
- maximum trades per day;
- cooldown after a loss or execution failure;
- maximum holding period;
- maximum spread;
- maximum slippage;
- minimum market-data freshness;
- maximum retry count;
- emergency shutdown condition;
- behaviour after a rejected or partially filled order.

The risk policy requires undefined execution controls to fail closed.

---

## Required deterministic execution controls

The application must implement and test the following controls rather than relying on operator or agent instructions.

### Order rejection and validation

Reject before submission when:

- symbol identity is not verified;
- quote data is stale or incomplete;
- entry, stop, or target is invalid;
- risk sizing inputs are missing;
- aggregate limits would be breached;
- volume cannot be rounded within broker constraints;
- spread, slippage, margin, or stop-level checks fail;
- the strategy decision is duplicated or has expired.

### Duplicate submissions

Each signal and order requires a persistent unique identifier. The system must:

- reject an already-submitted signal ID;
- use an idempotency key where supported;
- record request, response, broker order ID, and timestamps;
- prevent retries from creating a second position;
- reconcile broker state before retrying after an uncertain response.

### Disconnects and bounded retries

On connection loss:

- stop new submissions;
- preserve the pending request and state;
- use bounded retries only;
- do not assume an unsuccessful response means no order exists;
- query broker state before retrying;
- escalate to emergency handling when position protection cannot be verified.

### Partial fills

For a partial fill:

- record filled and remaining quantities separately;
- place or verify protection for the filled quantity;
- recalculate residual exposure;
- cancel or expire the remainder according to the approved order policy;
- recheck aggregate limits;
- prevent the unfilled remainder from being treated as an active position.

### Restarts

On restart:

- enter reconciliation mode before new signals;
- reload durable signal, order, fill, and position records;
- query broker positions and working orders;
- match broker records to internal records;
- identify unknown, missing, duplicate, or unprotected positions;
- block trading until discrepancies are resolved or emergency shutdown is approved.

### Protective orders

For every fill:

- verify the protective stop exists at the approved level;
- verify its volume covers the filled position;
- reject or escalate if protection is absent, rejected, or materially different;
- never widen the stop or increase risk automatically.

### Emergency shutdown

The system requires a deterministic emergency-stop mechanism that:

- blocks new orders;
- cancels eligible working entry orders;
- reports all open positions and protection status;
- handles unknown order state conservatively;
- persists the shutdown reason;
- requires explicit authorised recovery.

---

## Credential handling

Credential locations observed:

- `ProjectMayhem/main.py`, including module-level broker configuration and login logic;
- authentication examples or placeholders in `docs/Strategy.txt`.

Credential values are not reproduced. Exposed credentials should be rotated and removed from source and history through an approved security process. Broker authentication must not occur during module import, and offline tests must not require or access credentials.

---

## Prioritised paper-trading blockers

Paper trading should remain blocked until the following are resolved and evidenced:

| Priority | Blocker |
|---|---|
| Critical | Remove or rotate exposed credentials and make imports broker-free |
| Critical | Define and test current-equity, account-currency, cost-inclusive position sizing |
| Critical | Implement protective-order handling, rejection, partial-fill, duplicate, disconnect, restart, and reconciliation controls |
| Critical | Resolve GBPJPY/GBPUSD mismatch and provide an independent USDJPY stream |
| Critical | Define Q01–Q08: zones, direction, confirmation timing, entry, stop, session, and holding period |
| Critical | Define Q09–Q10 account-level limits, including aggregate open risk and shared JPY exposure |
| High | Preserve timestamp, timezone, completion, symbol, price-basis, and extraction provenance |
| High | Remove look-ahead effects from FVG, OB, liquidity, and confirmation logic |
| High | Establish a complete dependency manifest and run tests against the exact current commit |
| High | Add deterministic numerical tests for 2R geometry and fail-closed sizing |
| High | Define costs, slippage, spread, freshness, and broker constraint assumptions |
| High | Define Q11 evaluation evidence, chronological data splits, acceptance criteria, and promotion gates |

---

## Checks executed

No tests, numerical simulations, imports, broker calls, backtests, paper trades, or live trades were executed for this handoff.

The historical CI result is not treated as current evidence because its head differs from the observed `main` commit and no artifacts were returned.

---

## Recommendation

**Recommendation: reject paper-trading promotion and reject any live release.**

The repository is an incomplete MT5 prototype. Execution is stubbed, approved position sizing is absent, instrument data is inconsistent, USDJPY is not independently represented, portfolio and JPY exposure limits are undefined, and key order-lifecycle controls are unimplemented or unverified.

The next release should be limited to an offline, secret-free numerical-validation release. It should not connect to an account or submit orders until the blockers above have deterministic implementation, independent tests, current-commit evidence, and product-owner approval.
