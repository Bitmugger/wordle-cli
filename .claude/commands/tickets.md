Fetch all tickets from the wordle-cli GitHub Project (project #2, owner Bitmugger) and display them as a markdown table sorted by issue number with columns: #, Title, Status, Branch.

Use this exact command to fetch the data:
```
gh project item-list 2 --owner Bitmugger --format json | python3 -c "
import json, sys
data = json.load(sys.stdin)
items = sorted(data['items'], key=lambda x: x['content']['number'])
print('| # | Title | Status | Branch |')
print('|---|-------|--------|--------|')
for item in items:
    num = item['content']['number']
    title = item['content']['title']
    status = item.get('status') or '—'
    branch = item.get('branch') or '—'
    print(f'| {num} | {title} | {status} | {branch} |')
"
```

Print the resulting table.
