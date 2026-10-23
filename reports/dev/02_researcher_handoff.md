# Researcher handoff — DEMO-only strategy specification

The supplied researcher handoff is a research/specification handoff only. No code was changed, no commands were run, no broker was accessed, and no trades were placed.

## Status

- status: Research-stage specification and engineering handoff; no implementation or trading authorization
- starting_commit: `main` at `f9b530de4f48c7bc94a3c92fd068afec03f4b787`
- candidate_commit: none - research stage
- files_changed: none
- test_result: not applicable

## Key blockers

Unverified GBPJPY/USDJPY data provenance; GBPUSD filename/runtime-symbol mismatch; absent timezone and completed-candle metadata; unresolved Q01–Q11 strategy definitions; incomplete execution and reconciliation; incomplete risk controls; no current-commit test execution; no chronological performance evidence.

## Specification status

The handoff defines proposed completed-candle H1/M15 sequencing, normalized FVGs, configurable order blocks, liquidity-based stops, executable bid/ask entry, immutable 2R geometry, a 2% maximum risk ceiling, conservative demo defaults, fail-closed controls, broker-boundary requirements, provenance rules, unresolved decisions Q01–Q11, and acceptance criteria. These remain specification material, not implemented behavior.
