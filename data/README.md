# Data

The point economy. **These files are the source of truth for what things cost** — the balance
engine reads them directly, and `docs/rulebook/12-keywords.md` is generated from
`keywords.yaml`.

| File | Contents |
|---|---|
| `keywords.yaml` | 22 faction-exclusive Roles, with point cost and owning faction |
| `effects.yaml` | 52 effect types with point costs — the vocabulary abilities are priced in |
| `status-effects.yaml` | 6 statuses. **Contains a known conflict with the rulebook — see OQ-08** |

Changing a point value changes every card that uses it. After any edit:

```bash
python tools/balance.py --failing
```

Adding a keyword or effect means pricing it against at least two existing entries and saying so
in `docs/design/decisions.md`. Gate MG1 in the gameplay rubric.
