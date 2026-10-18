# Project Mayhem — decision log

Updated: 18 October 2026. Version: 0.1. Status: initial documentation baseline.

Paths in this document are relative to the project root unless a Markdown link is used.

## Status convention

- **Owner-stated:** explicitly present in the user's current instructions.
- **Observed baseline:** verified in supplied files; not an endorsement.
- **Proposed:** assistant recommendation or unresolved implementation choice; not approved by silence.
- **Superseded:** retained with a link to the replacing decision.

A request to create these documents does not approve every proposed strategy interpretation or grant external execution access. No approval is fabricated below.

## Initial register

| ID | Date | Decision / fact | Status | Source / implication |
|---|---|---|---|---|
| D001 | 2026-10-18 | Target GBPJPY and USDJPY with hourly context and M15 confirmation | Owner-stated | Current Senior Engineer brief; implementation currently selects only GBPJPY |
| D002 | 2026-10-18 | Initial planned RR exactly 2:1; intended maximum 2% per trade | Owner-stated | Initial brief; operational sizing not implemented |
| D003 | 2026-10-18 | Seek 2–3 trades/day and short holding periods | Owner-stated objective | Numeric session, frequency and holding rules remain unresolved |
| D004 | 2026-10-18 | Prefer a free-service crew experiment without a large bill | Owner-stated | No paid services or automatic paid fallback should be configured |
| D005 | 2026-10-18 | Create the six project documents in the supplied folder | Owner-stated | Scope of this documentation update |
| D006 | 2026-10-18 | Use researcher, engineer, independent QA and risk reviewer | Proposed team baseline | Recommended earlier; adding documents does not instantiate agents |
| D007 | 2026-10-18 | Start with a manual sequential audit; delegation/memory/planning off | Proposed operating baseline | Verify available settings and included model before kickoff |
| D008 | 2026-10-18 | Analyse every trade, promote changes through independent review | Proposed change control | Replaces unbounded self-editing as a recommendation; no runtime change made |
| D009 | 2026-10-18 | No forced trades when no valid setup exists | Proposed interpretation | Resolve alongside Q09 before strategy execution |
| D010 | 2026-10-18 | Future risk up to 5% and targets up to 4R were mentioned | Owner-stated future intent | Do not use as initial configuration; approval criteria unresolved |
| D011 | 2026-10-18 | Block autonomous risk escalation and separate paper/live promotion | Proposed operating baseline | Requires explicit release decisions; no live access provided |
| D012 | 2026-10-18 | MT5 is the historical data/API choice | Observed baseline | `docs/Strategy.txt`, Phase 1; platform and broker remain unverified |
| D013 | 2026-10-18 | Six modules parse; seven CSV fixtures inspected; no supplied tests or manifest | Observed baseline | EXP-000; not runtime success |
| D014 | 2026-10-18 | Preserve original code/research/data in this update | Documentation scope | Only six Markdown files added; inherited credentials remain in source |

## Pending decisions

Use Q01–Q11 from [strategy specification](strategy_specification.md). The priority sequence is:

1. Confirm zone definitions, direction labels and confirmation timing (Q01–Q04).
2. Define entry, liquidity stop, sessions and maximum holding time (Q05–Q08).
3. Set portfolio limits and frequency semantics (Q09–Q10).
4. Agree evaluation evidence and promotion criteria (Q11).
5. Verify model/tool charging, project-scoped access and isolated execution before the first crew run.

Unresolved numeric controls are not zero, unlimited or default values. They are missing configuration.

## Template for future entries

Copy this structure for a real decision. Do not overwrite previous approvals.

- **ID:** D015 or next unused ID.
- **Date/time and timezone:** Actual decision time.
- **Owner/approver:** Person granting approval; agent proposals are not approvals.
- **Question and alternatives:** The concrete choice and options considered.
- **Decision and status:** Exact selected behaviour, or explicitly proposed/pending.
- **Evidence:** Source files, experiment IDs, code/data versions and reports.
- **Scope:** Affected symbols, strategy version, environment and parameters.
- **Acceptance criteria / limits:** Numeric criteria where applicable.
- **Implementation and rollback:** Change reference and prior version.
- **Supersedes:** Prior decision IDs, if any.

Keep provider billing decisions separate from strategy decisions. Retain rejected hypotheses and unprofitable results so future agents do not repeat them as new discoveries.
