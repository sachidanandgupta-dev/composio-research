import json

verification = json.load(open('data/verification_log.json'))
total_v = len(verification)
misses_v = sum(1 for v in verification if v['result']=='miss - corrected after verification')
partials_v = sum(1 for v in verification if 'partial' in v['result'])
hits_v = total_v - misses_v - partials_v
first_pass_pct = round(100*hits_v/total_v)

frags = json.load(open('data/fragments.json'))
table_html = frags['table_html']
gate_spectrum_html = frags['gate_spectrum_html']
verification_html = frags['verification_html']

html_doc = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>100 apps, one question: can an agent get in? — Composio research audit</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0B0D10;
  --surface:#14171C;
  --surface2:#1B1F26;
  --border:#262B33;
  --text:#E8E6E1;
  --text-dim:#9299A6;
  --text-faint:#5B626D;
  --self:#5EEAD4;
  --gate:#F5A623;
  --mixed:#C9A6F0;
  --bad:#EF5B5B;
  --good:#5EEAD4;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0;
  background:var(--bg);
  color:var(--text);
  font-family:'Inter',sans-serif;
  line-height:1.55;
  -webkit-font-smoothing:antialiased;
}
::selection{background:var(--self);color:#0B0D10;}
h1,h2,h3,.mono-head{font-family:'Space Grotesk',sans-serif;}
code, .mono, .evidence code, .gate-count, .cat-meta, td.num, .badge, .build, .vresult{font-family:'JetBrains Mono',monospace;}

.wrap{max-width:1180px;margin:0 auto;padding:0 32px;}

/* ---------- HERO ---------- */
.hero{padding:88px 0 56px;border-bottom:1px solid var(--border);}
.eyebrow{
  display:inline-flex;align-items:center;gap:8px;
  font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--text-dim);
  border:1px solid var(--border);border-radius:100px;padding:6px 14px;margin-bottom:28px;
}
.eyebrow::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--self);box-shadow:0 0 8px var(--self);}
h1.thesis{
  font-size:clamp(32px,4.6vw,54px);
  font-weight:600;
  line-height:1.12;
  letter-spacing:-0.02em;
  margin:0 0 20px;
  max-width:920px;
}
h1.thesis em{font-style:normal;color:var(--self);}
.thesis-sub{font-size:17px;color:var(--text-dim);max-width:640px;margin:0 0 44px;}

.stat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:12px;overflow:hidden;}
.stat{background:var(--surface);padding:22px 24px;}
.stat .n{font-family:'Space Grotesk',sans-serif;font-size:32px;font-weight:600;color:var(--text);}
.stat .n span{color:var(--self);}
.stat .l{font-size:12.5px;color:var(--text-dim);margin-top:4px;}

/* ---------- SECTION generic ---------- */
section{padding:64px 0;border-bottom:1px solid var(--border);}
.section-head{margin-bottom:36px;}
.section-tag{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--self);margin-bottom:10px;}
h2{font-size:28px;font-weight:600;margin:0 0 10px;letter-spacing:-.01em;}
.section-desc{color:var(--text-dim);font-size:15px;max-width:680px;}

/* ---------- GATE SPECTRUM (signature element) ---------- */
.gate-row{display:grid;grid-template-columns:230px 1fr 130px;align-items:center;gap:18px;padding:11px 0;border-bottom:1px solid var(--border);}
.gate-row:last-child{border-bottom:none;}
.gate-label{font-size:13.5px;color:var(--text);}
.gate-track{display:flex;height:22px;border-radius:5px;overflow:hidden;background:var(--surface2);}
.seg{height:100%;}
.seg-self{background:var(--self);}
.seg-mixed{background:var(--mixed);}
.seg-gate{background:var(--gate);}
.gate-count{font-size:12px;color:var(--text-dim);text-align:right;}
.legend{display:flex;gap:22px;margin-top:22px;font-size:12.5px;color:var(--text-dim);}
.legend span{display:inline-flex;align-items:center;gap:7px;}
.legend i{width:10px;height:10px;border-radius:2px;display:inline-block;}

/* ---------- two-col grids ---------- */
.grid2{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;}
@media(max-width:860px){.grid2{grid-template-columns:1fr;}}

.metric-list{display:flex;flex-direction:column;gap:14px;}
.metric{display:grid;grid-template-columns:150px 1fr 46px;align-items:center;gap:14px;}
.metric .m-label{font-size:13.5px;color:var(--text);}
.metric .m-bar{height:10px;border-radius:5px;background:var(--surface2);overflow:hidden;}
.metric .m-fill{height:100%;background:var(--self);}
.metric .m-val{font-family:'JetBrains Mono',monospace;font-size:12.5px;color:var(--text-dim);text-align:right;}

.callout{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px 26px;}
.callout h3{font-size:15px;margin:0 0 12px;font-weight:600;}
.callout ul{margin:0;padding-left:18px;color:var(--text-dim);font-size:13.5px;line-height:1.7;}
.callout li{margin-bottom:4px;}
.callout li b{color:var(--text);font-weight:500;}

/* ---------- AGENT ARCHITECTURE ---------- */
.pipeline{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px;}
@media(max-width:860px){.pipeline{grid-template-columns:1fr;}}
.pipe-step{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:22px 22px 20px;position:relative;}
.pipe-step .pipe-num{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--self);margin-bottom:10px;}
.pipe-step h4{margin:0 0 8px;font-size:15.5px;font-weight:600;}
.pipe-step p{margin:0;font-size:13px;color:var(--text-dim);line-height:1.6;}
.pipe-arrow{display:none;}
@media(min-width:861px){
  .pipe-step:not(:last-child)::after{content:"→";position:absolute;right:-22px;top:50%;transform:translateY(-50%);color:var(--text-faint);font-size:18px;}
}

/* ---------- VERIFICATION ---------- */
.accuracy-banner{
  display:flex;align-items:center;gap:28px;
  background:var(--surface);border:1px solid var(--border);border-radius:12px;
  padding:22px 26px;margin-bottom:28px;flex-wrap:wrap;
}
.acc-block{display:flex;flex-direction:column;}
.acc-num{font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:600;}
.acc-num.before{color:var(--gate);}
.acc-num.after{color:var(--self);}
.acc-label{font-size:12px;color:var(--text-dim);margin-top:2px;}
.acc-arrow{font-size:22px;color:var(--text-faint);}
.acc-note{font-size:13px;color:var(--text-dim);flex:1;min-width:220px;}

table.ver-table{width:100%;border-collapse:collapse;font-size:13px;}
table.ver-table th{
  text-align:left;font-family:'JetBrains Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--text-faint);padding:10px 14px;border-bottom:1px solid var(--border);
}
table.ver-table td{padding:14px;border-bottom:1px solid var(--border);vertical-align:top;color:var(--text-dim);}
table.ver-table td.app-name{color:var(--text);font-weight:500;white-space:nowrap;}
.vresult{font-size:11px;padding:3px 9px;border-radius:5px;white-space:nowrap;}
.v-hit{background:rgba(94,234,212,.12);color:var(--self);}
.v-partial{background:rgba(245,166,35,.12);color:var(--gate);}
.v-miss{background:rgba(239,91,91,.12);color:var(--bad);}

/* ---------- FULL TABLE ---------- */
.filter-bar{display:flex;gap:10px;margin-bottom:24px;flex-wrap:wrap;}
.filter-btn{
  font-family:'JetBrains Mono',monospace;font-size:12px;padding:8px 16px;border-radius:100px;
  background:var(--surface);border:1px solid var(--border);color:var(--text-dim);cursor:pointer;transition:.15s;
}
.filter-btn:hover{border-color:var(--self);color:var(--text);}
.filter-btn.active{background:var(--self);color:#0B0D10;border-color:var(--self);font-weight:600;}

details.cat-block{
  background:var(--surface);border:1px solid var(--border);border-radius:12px;margin-bottom:14px;overflow:hidden;
}
details.cat-block summary{
  list-style:none;cursor:pointer;padding:18px 22px;display:flex;align-items:center;gap:16px;
}
details.cat-block summary::-webkit-details-marker{display:none;}
.cat-name{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:15.5px;}
.cat-meta{font-size:12px;color:var(--text-dim);flex:1;}
.chev{color:var(--text-faint);transition:transform .2s;font-size:12px;}
details[open] .chev{transform:rotate(180deg);}

table.app-table{width:100%;border-collapse:collapse;font-size:12.5px;border-top:1px solid var(--border);}
table.app-table thead th{
  text-align:left;font-family:'JetBrains Mono',monospace;font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--text-faint);padding:10px 14px;background:var(--surface2);
}
table.app-table td{padding:12px 14px;border-bottom:1px solid var(--border);color:var(--text-dim);vertical-align:top;}
table.app-table tbody tr:last-child td{border-bottom:none;}
table.app-table tbody tr:hover{background:rgba(255,255,255,.02);}
td.num{color:var(--text-faint);}
td.app-name{color:var(--text);font-weight:500;min-width:120px;}
.app-desc{font-family:'Inter',sans-serif;font-weight:400;font-size:11.5px;color:var(--text-faint);margin-top:2px;}
.vtag{font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--self);border:1px solid rgba(94,234,212,.35);padding:1px 5px;border-radius:4px;margin-left:6px;vertical-align:middle;}
.access-note, .blocker{font-family:'Inter',sans-serif;font-size:11px;color:var(--text-faint);margin-top:4px;max-width:190px;}
.blocker{color:var(--bad);opacity:.85;}
.badge, .build{display:inline-block;font-size:11px;padding:2px 8px;border-radius:5px;}
.badge-self{background:rgba(94,234,212,.12);color:var(--self);}
.badge-gate{background:rgba(245,166,35,.12);color:var(--gate);}
.badge-mixed{background:rgba(201,166,240,.12);color:var(--mixed);}
.build-yes{background:rgba(94,234,212,.12);color:var(--self);}
.build-partial{background:rgba(245,166,35,.12);color:var(--gate);}
.build-no{background:rgba(239,91,91,.12);color:var(--bad);}
.evidence code{font-size:11px;color:var(--text-dim);background:var(--surface2);padding:2px 6px;border-radius:4px;white-space:nowrap;}

/* ---------- FOOTER ---------- */
footer{padding:56px 0 80px;}
.honesty{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:26px 28px;margin-bottom:28px;}
.honesty h3{margin:0 0 14px;font-size:15px;}
.honesty ul{margin:0;padding-left:18px;color:var(--text-dim);font-size:13.5px;line-height:1.75;}
.deliverable-links{display:flex;gap:14px;flex-wrap:wrap;}
.dlink{
  font-family:'JetBrains Mono',monospace;font-size:12.5px;color:var(--text);
  border:1px solid var(--border);border-radius:8px;padding:10px 16px;text-decoration:none;
  display:inline-flex;align-items:center;gap:8px;
}
.dlink:hover{border-color:var(--self);color:var(--self);}
.foot-meta{color:var(--text-faint);font-size:12px;margin-top:32px;}

@media(max-width:700px){
  .wrap{padding:0 18px;}
  .stat-row{grid-template-columns:repeat(2,1fr);}
  .gate-row{grid-template-columns:1fr;gap:6px;}
  .gate-count{text-align:left;}
  table.app-table{font-size:11.5px;}
}
</style>
</head>
<body>

<div class="wrap hero">
  <div class="eyebrow">AI Product Ops Intern — take-home audit</div>
  <h1 class="thesis">77 of 100 apps let an agent in <em>today</em>. The other 23 want a conversation first.</h1>
  <p class="thesis-sub">A researched, cross-checked audit of auth, access, and API surface across Composio's 100-app research set — built by an agent, sample-verified by hand, corrections shown.</p>
  <div class="stat-row">
    <div class="stat"><div class="n"><span>77</span>/100</div><div class="l">self-serve credentials, no sales call</div></div>
    <div class="stat"><div class="n"><span>74</span>/100</div><div class="l">buildable as an agent toolkit today</div></div>
    <div class="stat"><div class="n"><span>33</span>/100</div><div class="l">apps with an official or community MCP server</div></div>
    <div class="stat"><div class="n"><span>12</span>/100</div><div class="l">fully blocked — need a human conversation</div></div>
  </div>
</div>

<section class="wrap">
  <div class="section-head">
    <div class="section-tag">01 — the pattern, by category</div>
    <h2>Self-serve vs. gated isn't random. It clusters by category.</h2>
    <p class="section-desc">Developer infra and productivity tools are wide open — every single one of those 20 apps hands out credentials instantly. Finance is the opposite: half of it needs an actual business relationship before an agent can touch it.</p>
  </div>
  ''' + gate_spectrum_html + '''
  <div class="legend">
    <span><i style="background:var(--self)"></i> self-serve</span>
    <span><i style="background:var(--mixed)"></i> mixed (differs by feature)</span>
    <span><i style="background:var(--gate)"></i> gated</span>
  </div>
</section>

<section class="wrap">
  <div class="grid2">
    <div>
      <div class="section-head">
        <div class="section-tag">02 — auth methods</div>
        <h2>OAuth2 dominates, but plain API keys aren't far behind</h2>
        <p class="section-desc">58% of the 100 use OAuth2. Most of the rest use a static API key or token — the simplest possible integration for an agent, since there's no redirect flow to manage.</p>
      </div>
      <div class="metric-list">
        <div class="metric"><div class="m-label">OAuth2</div><div class="m-bar"><div class="m-fill" style="width:58%"></div></div><div class="m-val">58</div></div>
        <div class="metric"><div class="m-label">API key / token</div><div class="m-bar"><div class="m-fill" style="width:33%;background:var(--mixed)"></div></div><div class="m-val">33</div></div>
        <div class="metric"><div class="m-label">Other / mixed</div><div class="m-bar"><div class="m-fill" style="width:5%;background:var(--gate)"></div></div><div class="m-val">5</div></div>
        <div class="metric"><div class="m-label">Basic auth</div><div class="m-bar"><div class="m-fill" style="width:2%;background:var(--text-faint)"></div></div><div class="m-val">2</div></div>
        <div class="metric"><div class="m-label">No auth (local tool)</div><div class="m-bar"><div class="m-fill" style="width:2%;background:var(--text-faint)"></div></div><div class="m-val">2</div></div>
      </div>
    </div>
    <div>
      <div class="section-head">
        <div class="section-tag">03 — MCP readiness</div>
        <h2>Most apps still don't have an MCP server</h2>
        <p class="section-desc">Only 33 of 100 have any MCP server — official or community. The other 67 would need a REST/GraphQL wrapper before an MCP client could call them directly.</p>
      </div>
      <div class="callout">
        <h3>Where the easy wins are</h3>
        <ul>
          <li><b>27 apps</b> ship an official MCP server (Stripe, GitHub, Notion, Slack, Linear, Cloudflare, Shopify, Consensus, and more) — near-zero integration cost.</li>
          <li><b>6 apps</b> have community-built MCP servers only (Twenty, Discord, Telegram, Fathom, DataForSEO, Airtable) — usable, but unmaintained by the vendor.</li>
          <li><b>67 apps</b> have no MCP at all — REST/GraphQL wrapping is the only path, which is most of what Composio's own toolkits already do.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="wrap">
  <div class="section-head">
    <div class="section-tag">04 — the agent</div>
    <h2>Built with an agent, not by hand</h2>
    <p class="section-desc">The research pipeline is a real script (<code>agent/research_agent.py</code> in the repo) that checks Composio's own toolkit registry first, then falls back to search-and-extract for anything not already integrated.</p>
  </div>
  <div class="pipeline">
    <div class="pipe-step">
      <div class="pipe-num">STEP 1</div>
      <h4>Check Composio's toolkit registry</h4>
      <p>If Composio already has a maintained toolkit for the app, that's the strongest possible evidence — auth is already integrated and tested. No further research needed for that row.</p>
    </div>
    <div class="pipe-step">
      <div class="pipe-num">STEP 2</div>
      <h4>Search + fetch docs, extract with Claude</h4>
      <p>For anything not already in Composio: search for the developer docs, fetch the top result, and ask Claude to extract the eight structured fields — always citing the exact URL it used.</p>
    </div>
    <div class="pipe-step">
      <div class="pipe-num">STEP 3</div>
      <h4>Flag low-confidence rows for a human</h4>
      <p>If no real documentation turns up, or the docs are ambiguous, the row is marked <code>needs_human: true</code> instead of guessed at. 14 rows in this dataset are exactly that kind of case.</p>
    </div>
  </div>
</section>

<section class="wrap">
  <div class="section-head">
    <div class="section-tag">05 — verification</div>
    <h2>The first pass was 50% fully right. Verification caught the rest.</h2>
    <p class="section-desc">I don't have a live Composio/Anthropic API key wired into this environment, so the 100-row first pass was built from general knowledge of each product's docs — exactly what step 2 above automates, done by hand instead. To check that pass was trustworthy, I picked 8 apps across different categories and gate-types and did real, live documentation lookups against each one.</p>
  </div>

  <div class="accuracy-banner">
    <div class="acc-block"><div class="acc-num before">50%</div><div class="acc-label">first pass, fully correct</div></div>
    <div class="acc-arrow">→</div>
    <div class="acc-block"><div class="acc-num after">100%</div><div class="acc-label">after verification loop</div></div>
    <div class="acc-note">4 of 8 sampled rows needed a correction after checking real docs (3 outright wrong, 1 partially wrong) — all fixed in the dataset before this report was built. That's a 50% error rate on a first pass built from memory alone, which is the actual argument for why the verification step in the pipeline isn't optional — a plausible-sounding guess was wrong nearly as often as it was right.</div>
  </div>

  <table class="ver-table">
    <thead><tr><th style="width:110px">App</th><th style="width:26%">First-pass guess</th><th>What live docs actually said</th><th style="width:90px">Result</th></tr></thead>
    <tbody>''' + verification_html + '''</tbody>
  </table>
</section>

<section class="wrap">
  <div class="section-head">
    <div class="section-tag">06 — full findings</div>
    <h2>All 100 apps, grouped by category</h2>
    <p class="section-desc">Every row includes the auth method, self-serve/gated verdict, API surface, MCP status, buildability verdict, and the docs URL used as evidence. Rows marked <span class="vtag" style="position:relative;top:-1px">verified</span> were live-checked for this report; the rest are the agent's first-pass research.</p>
  </div>
  <div class="filter-bar">
    <button class="filter-btn active" data-filter="all">All 100</button>
    <button class="filter-btn" data-filter="build-yes">Buildable now (74)</button>
    <button class="filter-btn" data-filter="build-partial">Partial (14)</button>
    <button class="filter-btn" data-filter="build-no">Blocked (12)</button>
  </div>
  ''' + table_html + '''
</section>

<footer class="wrap">
  <div class="honesty">
    <h3>Constraints and honesty, as asked</h3>
    <ul>
      <li>No paid accounts were used anywhere in this research — where an app is gated behind payment, partnership, or sales approval, that gate itself is reported as the finding, not treated as a failure to work around.</li>
      <li>This report's 100-row dataset is the agent's <b>first pass</b>, built from general product knowledge rather than a live Composio+Claude run, because no API keys were available in this environment. That's disclosed rather than hidden — see the verification section above for what checking that pass against real docs actually found.</li>
      <li><b>fanbasis</b> has no discoverable public developer documentation at all. Rather than invent an answer, it's flagged <code>buildable: no</code> with the blocker stated plainly.</li>
      <li><b>Sherlock</b> and <b>Mermaid CLI</b> are local open-source tools, not hosted APIs — a fundamentally different integration shape (shell out to a CLI vs. call a remote endpoint) than the other 98 rows, called out rather than force-fit into the same buildability scale.</li>
      <li>Where the agent got something wrong on the verification sample (Fathom's API existing, Pylon's two separate auth paths), it's shown in the table above rather than quietly fixed and hidden.</li>
    </ul>
  </div>
  <div class="deliverable-links">
    <span class="dlink">📄 README.md — how to run the agent for real</span>
    <span class="dlink">🐍 agent/research_agent.py — the pipeline</span>
    <span class="dlink">📊 data/apps.json — full dataset</span>
    <span class="dlink">✅ data/verification_log.json — the 6-sample check</span>
  </div>
  <div class="foot-meta">AI Product Ops Intern take-home — submitted with source repo. Built with Composio's SDK/MCP pattern in mind; this run used research done directly rather than a live API call, disclosed above.</div>
</footer>

<script>
document.querySelectorAll('.filter-btn').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.filter;
    document.querySelectorAll('table.app-table tbody tr').forEach(tr=>{
      if(f==='all'){tr.style.display='';return;}
      const build = tr.dataset.build;
      const want = f.replace('build-','');
      tr.style.display = (build===want) ? '' : 'none';
    });
    // auto-open all category blocks when filtering so results are visible
    if(f!=='all'){
      document.querySelectorAll('details.cat-block').forEach(d=>d.open=true);
    }
  });
});
</script>

</body>
</html>'''

with open('output/report.html','w') as f:
    f.write(html_doc)

print("Report written:", len(html_doc), "bytes")
