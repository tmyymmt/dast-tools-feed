# DAST Tools Feed

Release information feeds for DAST (Dynamic Application Security Testing) tools.

Updated weekly via GitHub Actions. Subscribe with any RSS reader.

🌐 **Live site**: https://tmyymmt.github.io/dast-tools-feed/

## What is DAST?

Dynamic Application Security Testing (DAST) refers to security testing techniques that analyze running applications by sending requests and observing responses, without access to source code. DAST tools simulate real-world attacks to detect vulnerabilities such as XSS, SQL injection, authentication flaws, and misconfigurations.

## Covered Tools

| Tool | Type | License |
|------|------|---------|
| [OWASP ZAP](https://www.zaproxy.org) | OSS | Apache-2.0 |
| [Nuclei](https://nuclei.projectdiscovery.io) | OSS | MIT |
| [sqlmap](https://sqlmap.org) | OSS | GPL-2.0 |
| [Nikto](https://cirt.net/Nikto2) | OSS | GPL-2.0 |
| [Wapiti](https://wapiti-scanner.github.io) | OSS | GPL-2.0 |
| [Burp Suite](https://portswigger.net/burp) | Commercial | Proprietary |

## Feed URLs

### All Tools (Combined)

| Format | URL |
|--------|-----|
| RSS 2.0 | `https://tmyymmt.github.io/dast-tools-feed/feeds/all.rss` |
| Atom 1.0 | `https://tmyymmt.github.io/dast-tools-feed/feeds/all.atom` |
| JSON Feed 1.1 | `https://tmyymmt.github.io/dast-tools-feed/feeds/all.json` |

### Per-Tool Feeds

Replace `{tool_id}` with: `zap`, `nuclei`, `sqlmap`, `nikto`, `wapiti`, `burpsuite`

| Format | URL |
|--------|-----|
| RSS 2.0 | `https://tmyymmt.github.io/dast-tools-feed/feeds/{tool_id}.rss` |
| Atom 1.0 | `https://tmyymmt.github.io/dast-tools-feed/feeds/{tool_id}.atom` |
| JSON Feed 1.1 | `https://tmyymmt.github.io/dast-tools-feed/feeds/{tool_id}.json` |

## Pages

- **Comparison**: [English](https://tmyymmt.github.io/dast-tools-feed/comparison.html) / [Japanese](https://tmyymmt.github.io/dast-tools-feed/comparison_ja.html)
- **Per-tool summaries**: `https://tmyymmt.github.io/dast-tools-feed/{tool_id}.html`

## Release Categories

Releases are categorized for easy filtering:

| Category | Description |
|----------|-------------|
| `feature` | Feature additions and changes |
| `bugfix` | Bug fixes |
| `security` | Security fixes and hotfixes |
| `pricing` | Pricing changes |
| `announcement` | Announcements, events, awards |
| `other` | Other |

## Repository Structure

```
.
├── scripts/            # Python scripts
│   ├── main.py         # Entry point
│   ├── models.py       # Data models
│   ├── categorize.py   # Release categorization
│   ├── storage.py      # JSON storage
│   ├── feed_generator.py   # RSS/Atom/JSON Feed generation
│   ├── markdown_generator.py  # HTML page generation
│   └── collectors/     # Data collectors per tool type
│       ├── github.py   # GitHub Releases API collector
│       └── burpsuite.py  # Burp Suite HTML scraper
├── tools/
│   └── tools.yml       # Tool configuration
├── data/               # Persisted release data (JSON)
├── public/             # Generated output (gitignored, deployed to GitHub Pages)
├── tests/              # Test suite
└── docs/               # Specifications
```

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# Run collection and generate feeds/pages
FEED_BASE_URL="https://tmyymmt.github.io/dast-tools-feed/feeds" python -m scripts.main

# Run tests
pytest tests/
```

## License

MIT License