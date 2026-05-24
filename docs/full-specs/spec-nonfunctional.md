# Non-Functional Requirements

> Prerequisite: [Full Specification](spec.md)

---

## Reducing Maintenance Burden

- Prefer GitHub API over scraping
- OSS tools on GitHub can be added with low cost; add commercial tools that require scraping with caution
- Unify internal data format as JSON to limit the impact of upstream changes
- Manage tool list in a configuration file (YAML, etc.) so new tools can be added without code changes
- When scraped HTML changes unexpectedly, emit a warning but do not break the feed

## Behavior on Failure

| Scenario | Behavior |
|---|---|
| Partial failure | If one tool's collection fails, still update feeds for other tools |
| Atomic writes | Write to a temp file then rename; never publish a partially written file |
| Rate limiting | On GitHub API 429, skip that run and retry on the next scheduled execution |
| 404 / page gone | Log the error and preserve existing data as-is |
| GitHub Actions alerts | On workflow failure, auto-create an Issue if no open `feed-failure` Issue already exists |
| Feed validation | Generated RSS/Atom/JSON feeds are written directly without additional parsing or schema validation |
| Rollback | Data is stored in Git, so broken state can be reverted with `git revert` |

## License

MIT License
