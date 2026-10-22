# Researcher handoff — constrained engineering patch

**Specification:** RS-ENG-0.1  
**Baseline:** `main` at `8feb36db91d7144b4a190a302634ddd30c449c0b`

## Authorised scope

1. Make imports offline-safe and broker startup explicit.
2. Remove embedded credentials from current source without reproducing them.
3. Repair M15 incremental CSV writing.
4. Add regression tests and ensure test discovery.

No strategy redesign, trading, broker connection, profitability claim, or production execution is authorised.

## Behavioural constraints

FVG, order-block, liquidity, 2R, intended 2% risk, and M15 confirmation behaviours must remain unchanged. Import/startup separation is the intentional runtime-boundary change. The M15 writer must preserve paths, columns, ordering, serialisation, timestamps, precision, initial writes, and genuine appends, while making empty input a no-op with no file mutation. Deduplication, sorting, schema migration, timestamp reconciliation, and other ambiguous behaviours must not be invented.

## Proposed regression evidence

Test import isolation, credential-removal structure without printing secrets, empty and non-empty writer paths, existing-file preservation, existing FVG regressions, and CI discovery. The engineer was instructed to characterise the writer, move MT5 startup behind explicit invocation, remove credentials, add tests, and run CI against the exact development commit.

## Handoff conclusion

The repair may improve testability and prevent invalid M15 writes, but supplies no evidence that the strategy is profitable, executable, non-repainting, or ready for paper or live trading.
