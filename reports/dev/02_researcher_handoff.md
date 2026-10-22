# Researcher handoff — scoped engineering repair

**Baseline:** `main` at `8feb36db91d7144b4a190a302634ddd30c449c0b`

## Authorised scope

1. Offline-safe imports and explicit broker startup.
2. Removal of embedded credentials from current source.
3. Repair of M15 incremental CSV writing.
4. Regression tests and test discovery.

No strategy redesign, trading, broker connection, or production execution is authorised.

## Constraints

Existing FVG, order-block, liquidity, 2R, 2% risk, H1/M15 confirmation, and no-forced-trade definitions must remain unchanged. Duplicate handling and completed-candle semantics remain unresolved and must not be decided implicitly by this repair.

## Writer contract

Preserve the existing CSV header, column order, serialization, and input ordering. Before initial completion write all received rows. After initial completion write only the newest row without rewriting the file. Do not introduce deduplication, timestamp sorting, timezone relabelling, or strategy filtering. Empty input must not create market data.

## Proposed regression coverage

Offline import isolation, explicit startup, missing-configuration failure, absence of embedded credential values, initial and incremental M15 writes, empty input, existing FVG tests, and configured unittest discovery were proposed. Evidence from later handoffs is recorded separately.
