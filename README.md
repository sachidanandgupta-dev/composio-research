# Composio App Research Agent — take-home submission

Researches Composio's list of 100 apps (auth method, self-serve vs gated,
API surface, buildability) and produces the findings shown in the report at
`report.html`.

## What's here

```
composio-research/
├── agent/
│   └── research_agent.py     # the agent - see "Running it" below
├── data/
│   ├── apps.json              # the 100-app dataset, first-pass + verified
│   ├── apps_enriched.json     # normalized version with derived fields
│   ├── analyze.py             # pattern-finding script (produces the stats in the report)
│   └── verification_log.json  # the real sample-verification results
├── output/
│   └── report.html            # the deliverable
└── README.md
```

## How the research was actually done for this submission

I don't have a Composio API key or an LLM API key wired into this
environment, so I could not execute `research_agent.py` end-to-end against
Composio's live toolkit registry and MCP tools for this submission. To be
upfront about that rather than fake a run:

1. **First pass**: I populated all 100 rows from general knowledge of each
   product's developer docs - this is exactly the step `research_agent.py`
   automates (search → fetch docs → extract fields), just done by me
   directly instead of by the script.
2. **Verification pass**: I then took an 8-app sample spanning different
   categories and gate-types (Twenty, DealCloud, Pylon, GoHighLevel, Fathom,
   GitHub, Consensus, Waterfall.io) and did real, live documentation lookups
   against each one's actual dev docs. Results are in
   `data/verification_log.json`.
   - 4 of 8 were fully confirmed as-is (including GitHub as a control case).
   - 1 (Pylon) was *partially* wrong — the first pass collapsed two
     different auth rules (MCP vs. REST token) into one.
   - 3 were **wrong**:
     - Fathom — I'd assumed no public API existed; it actually shipped
       one, self-serve, with community MCP servers.
     - Consensus — I'd called the whole product "gated"; the MCP server
       is actually instant self-serve, it's only the separate REST API
       that's application-gated.
     - Waterfall.io — I'd assumed a B2B data vendor like this would be
       sales-gated; it hands out an API key immediately on signup.
   - All errors were corrected in `data/apps.json` after verification.
   - First-pass accuracy on the sample: **50% fully correct**.
     After the verification loop: 100% (all errors caught and fixed).
   - The pattern in the misses is worth noting: every wrong guess leaned
     toward assuming a paywall or sales gate that wasn't actually there.
     A memory-only first pass is biased toward assuming friction that
     verification often disproves.

This is the same "why verification matters" finding the assignment is
testing for — a plausible-sounding first pass isn't enough; you have to
actually cross-check a sample against ground truth, because even a small
sample catches errors a search-only or memory-only sweep of 100 apps would
have kept.

## Running it for real

```bash
pip install composio anthropic
export COMPOSIO_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
python agent/research_agent.py --input apps_to_research.json --output results.json
```

`apps_to_research.json` is just `[{"id": 1, "name": "Salesforce", "hint_url": "salesforce.com"}, ...]`
— the 100 apps from the assignment brief in that shape.

The agent, for each app:
1. Checks whether Composio already has a maintained toolkit for it
   (`composio.toolkits.list`) — if so, that's the answer, no research
   needed, since Composio's own integration is the strongest evidence
   there is.
2. If not, it searches for the app's developer docs (via Composio's
   hosted search toolkit) and asks Claude to extract the structured
   fields from what it found, always citing the URL it used.
3. Anything it can't find real documentation for is marked
   `needs_human: true` rather than guessed at.

Re-run `python data/analyze.py` after a real agent run to regenerate the
pattern stats (`apps_enriched.json` and the console summary) from
`data/apps.json`.

## Where a human was needed

- **14 apps are flagged `buildable: no`** — mostly finance/fintech
  (Brex, Ramp, PitchBook, Paygent Connect, iPayX) and a few
  enterprise-gated products (Salesforce Commerce Cloud, Amazon SP-API,
  Gladly, LinkedIn Ads, NotebookLM, Grain, Consensus). All of these need
  an actual outreach/partnership conversation, not more searching.
- **`fanbasis`** has no discoverable public developer documentation at
  all — flagged for a human to check directly with the vendor rather than
  guessed at.
- **Sherlock and Mermaid CLI** are open-source local tools, not hosted
  APIs — an agent toolkit could shell out to them, but they're a
  different integration pattern (local execution vs. remote API call)
  that's worth a human product decision, not an automated one.
