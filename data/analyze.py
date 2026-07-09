import json, re
from collections import Counter, defaultdict

data = json.load(open('data/apps.json'))

def norm_access(a):
    a = a.lower()
    if 'gated' in a and 'self-serve' in a:
        return 'mixed'
    if 'gated' in a:
        return 'gated'
    return 'self-serve'

def norm_auth(a):
    a = a.lower()
    if 'oauth' in a:
        return 'OAuth2'
    if 'api key' in a or 'api token' in a or 'access token' in a or 'personal access' in a:
        return 'API key / token'
    if 'basic' in a:
        return 'Basic auth'
    if 'none' in a:
        return 'No auth (local/open tool)'
    return 'Other'

for d in data:
    d['access_norm'] = norm_access(d['access'])
    d['auth_norm'] = norm_auth(d['auth'])

# Overall stats
access_counts = Counter(d['access_norm'] for d in data)
auth_counts = Counter(d['auth_norm'] for d in data)
build_counts = Counter(d['buildable'] for d in data)
mcp_official = sum(1 for d in data if 'official mcp' in d['mcp'].lower())
mcp_community = sum(1 for d in data if 'community mcp' in d['mcp'].lower())
mcp_none = sum(1 for d in data if d['mcp'].lower() in ('none', 'none official', 'none found'))

print("=== ACCESS PATTERN ===")
for k, v in access_counts.most_common():
    print(f"{k}: {v} ({v}%)")

print("\n=== AUTH METHOD ===")
for k, v in auth_counts.most_common():
    print(f"{k}: {v} ({v}%)")

print("\n=== BUILDABILITY ===")
for k, v in build_counts.most_common():
    print(f"{k}: {v}")

print(f"\n=== MCP ===\nOfficial MCP: {mcp_official}\nCommunity MCP: {mcp_community}\nNo MCP found: {mcp_none}")

print("\n=== BY CATEGORY: gated count ===")
cat_gated = defaultdict(lambda: [0,0])
for d in data:
    cat_gated[d['category']][1] += 1
    if d['access_norm'] in ('gated','mixed'):
        cat_gated[d['category']][0] += 1
for cat, (gated, total) in cat_gated.items():
    print(f"{cat}: {gated}/{total} gated or mixed")

print("\n=== Fully blocked (buildable=no) ===")
for d in data:
    if d['buildable'] == 'no':
        print(f"- {d['name']} ({d['category']}): {d['blocker']}")

json.dump(data, open('data/apps_enriched.json','w'), indent=1)
