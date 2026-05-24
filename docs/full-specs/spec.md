# Full Specification

This directory contains the full specification of this project.

## Writing Guidelines

- The specification should be navigable starting from this file
- Manage specifications hierarchically to prevent individual files from becoming too large and hard to read
- When there is a large amount of specification content, start with a high-level, concise description and create child files for the details
- When creating child files
  - Include links to prerequisite information files

---

## 1. Target Tools

### In Scope

| Tool | Type | Source | Collection Method |
|---|---|---|---|
| OWASP ZAP | OSS | https://github.com/zaproxy/zaproxy | GitHub Releases API |
| Nuclei | OSS | https://github.com/projectdiscovery/nuclei | GitHub Releases API |
| sqlmap | OSS | https://github.com/sqlmapproject/sqlmap | GitHub Releases API |
| Nikto | OSS | https://github.com/sullo/nikto | GitHub Releases API |
| Wapiti | OSS | https://github.com/wapiti-scanner/wapiti | GitHub Releases API |
| Burp Suite | Commercial (SaaS/Desktop) | https://portswigger.net/burp/releases | HTML scraping |

### Out of Scope (reference only)

The following categories of tools are out of scope:

- **SCA (Software Composition Analysis)**: Tools that scan components and libraries for known CVEs (e.g., Trivy, Grype)
- **SAST (Static Application Security Testing)**: Tools that detect vulnerabilities by analyzing source code patterns (e.g., SonarQube, Semgrep)
- **SBOM generation/management only**: Tools that do not perform vulnerability scanning (e.g., microsoft/sbom-tool)

---

## 2. Feed Specification

### Formats

All three formats are supported:

- RSS 2.0
- Atom 1.0
- JSON Feed 1.1

### Feed Fields

- Version (tag name)
- Date/time (published date)
- URL (link to release page)
- Summary (title and overview)
- Change details (CHANGELOG / release notes body)
- Release type category (see below)

### Release Type Categories

Feeds are categorized by release type, also used for filtering:

- `feature`: Feature additions and changes
- `pricing`: Pricing changes
- `security`: Security fixes and hotfixes
- `bugfix`: Bug fixes
- `announcement`: Announcements, conference appearances, awards, etc.
- `other`: Other

### Update Frequency

- Weekly execution via GitHub Actions (every Saturday at JST 07:00 / UTC Friday 22:00)
- Or: create an Issue → Copilot creates a PR → review → merge to main

### Publication Endpoint

- Published via GitHub Pages

---

## 3. Data Collection

### Collection Methods

| Target Type | Method |
|---|---|
| GitHub OSS (OWASP ZAP, Nuclei, etc.) | GitHub Actions + GitHub Releases API (structured data) |
| Commercial (Burp Suite) | GitHub Actions + HTML scraping |

Burp Suite `published_at` should be derived in this order: date in release URL path (`/YYYY-M-D/...`), date in title (`YYYY-MM-DD`), year in version (`YYYY-01-01`), then current UTC time as final fallback.

### GitHub Releases API

- Endpoint: `https://api.github.com/repos/{owner}/{repo}/releases`
- Available fields: `tag_name` (version), `published_at` (date), `body` (CHANGELOG), `html_url`
- Rate limits: 60 req/hour unauthenticated, 5000 req/hour with token
- **Prefer API over scraping** (scraping breaks when HTML structure changes)

### Execution Model

- Polling (weekly scheduled execution) is the primary model
- Event-driven (GitHub webhooks, etc.) is not adopted as target services do not support it

---

## 4. Data Storage

- Collected data is stored as files within the repository (JSON intermediate format)
- All sources are normalized to a unified JSON intermediate format, from which RSS/Atom/JSON Feed files are generated
  - Minimizes impact when upstream sources change
- History is retained permanently and accumulates indefinitely (never deleted)
- Target tools are managed in a configuration file (YAML, etc.) so new tools can be added without code changes
- Merge deduplication key is release URL. When the same URL already exists, only missing `body` in the existing entry may be backfilled from new data; other existing fields are preserved.

---

## 5. Publication and Distribution

- Target users: general public
- Subscription methods: RSS readers, or direct access to repository files
- Filtering: available by release type category

### Published URL

https://tmyymmt.github.io/dast-tools-feed/

### Output File Structure (public/)

`public/` is not committed to the repository (gitignored). It is generated at runtime by GitHub Actions and deployed to GitHub Pages.

| Path | Content |
|---|---|
| `feeds/all.{rss,atom,json}` | Combined feed for all tools |
| `feeds/{tool_id}.{rss,atom,json}` | Per-tool feeds |
| `{tool_id}.html` / `{tool_id}_ja.html` | Per-tool summary pages (English/Japanese) |
| `comparison.html` / `comparison_ja.html` | All-tools comparison pages (Summary table + Detailed Comparison table) |
| `index.html` | Top page (feed list and links to comparison pages) |
| `.nojekyll` | Disables Jekyll processing on GitHub Pages |

HTML pages automatically apply dark mode by detecting browser/OS settings via the `prefers-color-scheme` media query.

Markdown-rendered HTML for published pages must be sanitized before writing. Dangerous tags are removed, unsupported tags are unwrapped, and `<a href>` allows only relative URLs or `http` / `https` / `mailto` schemes.

The tool list in `index.html` uses the same sort order as the Summary table: summary feature checkmark count descending, then `gui: true` first, then alphabetically by tool name. Rows in `comparison.html` are sorted independently per table: each table sorts by its own checkmark count descending, then by `gui: true` first, then alphabetically.

### Per-Tool Page Structure

Each per-tool page (`{tool_id}.html` / `{tool_id}_ja.html`) contains:

- Tool overview (title, description, type, license, homepage link)
- **Features table**: 9 feature flags with ✅/❌ status:
  - Web Application Scanning, API Scanning, Authenticated Scanning, Active Scanning, Passive Scanning, Web Crawler, CI/CD Integration, Report Generation, GUI
- Feature reference link to official documentation (`features_url` in tools.yml, fallback to `homepage`)
- Release History (list of releases with version, date, and description)
- Source URL link below the Release History heading, pointing to the upstream release page

### Comparison Page Structure

The comparison pages (`comparison.html` / `comparison_ja.html`) contain two tables:

- **Summary table**: Tool name (with link to per-tool page and feature reference link), latest version, last updated, type, license, pricing, and basic feature flags (Web Scan, API Scan, Auth, Active, Passive).
- **Detailed Comparison table**: Tool name (with link to per-tool page and feature reference link), all feature flags plus a Unique Features column. Feature flags covered:
  - Web Scan, API Scan, Auth, Active, Passive, Crawler, CI/CD, Report, GUI

Each table uses its own sort order: checkmark count within that table's feature columns descending, then gui true first, then alphabetical.

---

## 6. Non-Functional Requirements

See [spec-nonfunctional.md](spec-nonfunctional.md) for details.

- Prefer GitHub API over scraping; scraping is a last resort
- Tolerate partial failures; keep updating other tools' feeds on failure
- Use atomic writes to prevent publishing partially written files
