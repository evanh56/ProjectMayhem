# Project Mayhem — development and trading risk policy

Updated: 18 October 2026. Version: 0.1. Status: initial documentation baseline.

Paths in this document are relative to the project root unless a Markdown link is used.

## Authority and scope

Evan Harrington is the product owner and release authority. The current owner brief sets an initial intended maximum 2% risk per trade and planned 2R target. Other numeric account-level thresholds have not been supplied. No new daily-loss, exposure, drawdown, holding-time or profitability thresholds are approved by this document.

This documentation update authorises no broker connection, purchase, live trade, code deployment or risk escalation. Initial agent work is an offline/read-only audit. Controlled paper trading is a later phase, not proof that a release is safe for live use.

## Trading limits and missing decisions

| Control | Baseline | Status |
|---|---|---|
| Target instruments | GBPJPY, USDJPY | Current owner brief |
| Initial intended per-trade risk | At most 2% | Current owner ceiling; actual configured fraction still to be selected |
| Initial target | Exactly 2R planned price geometry | Current owner brief |
| Aggregate open risk | Not specified | Required before execution |
| Concurrent positions | Not specified | Required before execution |
| Daily loss / drawdown stop | Not specified | Required before execution |
| Trade-count limit / cooldown | Not specified | Do not equate the 2–3 aspiration with a hard limit |
| Maximum holding period | Not specified | “Not multiple hours” needs a numeric rule |
| Spread, slippage and freshness bounds | Not specified | Derive and approve per instrument/environment |
| Later 5% risk / 4R targets | Future proposal only for the initial configuration | No automatic escalation |

Fail closed on an undefined required execution control: reject the order and report the missing configuration. This must be implemented in code; this policy alone changes no runtime behaviour.

## Position sizing requirements

Use current account equity and the approved risk fraction, not a hard-coded nominal pip count. Calculate loss at the proposed stop for the correct symbol, side, volume and account currency using verified contract information. Include applicable commission and an explicit execution-cost allowance without double-counting spread.

Choose the largest valid broker volume whose intended loss remains within the risk budget. Respect minimum/maximum volume, volume step, tick size/value, price precision, stop/freeze restrictions, available margin and currency conversion. Round volume down; reject if even the minimum lot exceeds the budget. Recheck at submission against a fresh quote and actual entry assumptions.

A stop order does not guarantee a maximum realised loss: gaps, slippage and failures can exceed intended stop risk. Report this distinction in every evaluation. `Execution.py::price_to_pip` is an experimental calculation using balance and fixed `pips = 7`; it is not a verified implementation of this policy.

## Portfolio and operational controls

GBPJPY and USDJPY share JPY exposure. Check combined risk and directional exposure, not just each ticket. Model realised and unrealised losses consistently at account level.

Before any execution phase, verify stale/incomplete data rejection, unique signal/order identifiers, duplicate prevention, partial fills, rejected orders, protected positions, disconnect/restart reconciliation, bounded retries, emergency stop and position handling on shutdown. Reconcile with the broker rather than trusting local CSV state.

Never widen a stop, average down, increase risk after losses, or change approved controls as a response to a single trade without an explicitly approved strategy revision.

## Agent capability boundaries

| Capability | Researcher | Engineer | QA | Risk reviewer |
|---|---|---|---|---|
| Read approved code/docs/data | Yes | Yes | Yes | Yes |
| Edit application code | No | Development workspace after assigned implementation task | No | No |
| Create tests | Propose fixtures | Yes | Independent test workspace | Propose scenarios |
| Run code | Approved calculations only | Isolated runner | Isolated runner | Fixed checks only |
| Write reports | Own reports | Own reports | Own reports | Own reports |
| Access credentials or submit orders | No | No | No | No |
| Merge, deploy, purchase or increase risk | No | No | No | No |

The initial audit grants no source edits to any role. Enforce boundaries in tools, filesystem permissions, process credentials and network access. Backstories and agent promises do not enforce them. If separate write permissions are unavailable, use read-only review and returned patches.

## Credentials and inherited material

`src/ProjectMayhem/main.py` contains embedded account authentication values and a module-level login call. Values are deliberately not copied into these documents. Treat the archive as private, keep it out of agent knowledge ingestion and public repositories until credentials are externalised, and rotate exposed credentials if they are still usable. This update preserves the supplied source; it does not sanitise it.

Use a separate, secret-free development workspace and no broker session for offline tests. Importing the current entry point is not an offline-safe inspection method. Historical virtual environments and unrelated personal files should not be mounted into execution sandboxes.

## Cost controls

The owner explicitly requires a free-service experiment without a large bill. Run only with account-verified included models or genuinely local inference. No paid provider keys, paid fallback, automatic top-ups, paid search, rented sandbox, or new data subscription should be available to the crew. Stop and report quota exhaustion.

Use manual sequential runs with bounded iterations/timeouts/retries and inspect usage after the first small check. Do not launch on every candle, trade or file change. Check the current account's limits; public pricing claims are not runtime spending controls. Knowledge embeddings, memory, planning and evaluation may invoke additional services and remain off until verified.

## Release and change process

1. Record the hypothesis, approved scope, code/data baseline and acceptance criteria.
2. Implement in an isolated branch/workspace; preserve the prior version.
3. Run relevant tests and reproducible historical evaluation with realistic costs and event-time data handling.
4. Obtain independent QA and risk findings. Resolve blockers or reject the change.
5. Product owner approves any promotion to a separately configured paper environment; live promotion is a separate decision.
6. Record deployed version, monitoring and rollback procedure. Production does not edit itself.

Log each trade, but assess strategy changes over defined samples. Keep an untouched evaluation period; do not repeatedly tune against the final test. Every new risk or RR setting requires a separately recorded decision and evaluation.
