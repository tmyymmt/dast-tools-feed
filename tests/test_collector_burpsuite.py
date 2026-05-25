import responses

from scripts.collectors.burpsuite import _fetch_page_body, _fetch_page_info, collect_burpsuite

BURPSUITE_HTML = """
<html><body>
<ul class="releases-list">
  <li><a href="/burp/releases/2024-3-1">Burp Suite 2024.3.1</a></li>
  <li><a href="/burp/releases/2024-2-1">[Hotfix] Burp Suite 2024.2.1</a></li>
</ul>
</body></html>
"""

BURPSUITE_PAGE_HTML = """
<html><body>
<main>
<h1>Burp Suite 2024.3.1 Release Notes</h1>
<p>This release adds new active scan capabilities and improves the crawler.</p>
</main>
</body></html>
"""

BURPSUITE_HOTFIX_PAGE_HTML = """
<html><body>
<main>
<h1>[Hotfix] Burp Suite 2024.2.1</h1>
<p>Critical security fix for CVE-2024-12345.</p>
</main>
</body></html>
"""


def _add_burpsuite_page_mocks():
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases/2024-3-1",
        body=BURPSUITE_PAGE_HTML,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases/2024-2-1",
        body=BURPSUITE_HOTFIX_PAGE_HTML,
        status=200,
    )


@responses.activate
def test_collect_burpsuite_returns_entries():
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases",
        body=BURPSUITE_HTML,
        status=200,
    )
    _add_burpsuite_page_mocks()
    entries = collect_burpsuite()
    assert len(entries) >= 1
    assert entries[0].tool_id == "burpsuite"
    assert entries[0].tool_name == "Burp Suite"
    assert entries[0].url.startswith("https://portswigger.net/")


@responses.activate
def test_collect_burpsuite_body_contains_page_content():
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases",
        body=BURPSUITE_HTML,
        status=200,
    )
    _add_burpsuite_page_mocks()
    entries = collect_burpsuite()
    regular = next(e for e in entries if "Hotfix" not in e.summary)
    assert "crawler" in regular.body or "active scan" in regular.body or "scan" in regular.body.lower()
    assert regular.published_at == "2024-03-01T00:00:00Z"


@responses.activate
def test_collect_burpsuite_hotfix_categorized_as_security():
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases",
        body=BURPSUITE_HTML,
        status=200,
    )
    _add_burpsuite_page_mocks()
    entries = collect_burpsuite()
    hotfix_entries = [e for e in entries if "Hotfix" in e.summary or "hotfix" in e.url]
    assert any(e.category == "security" for e in hotfix_entries)
    assert any(e.published_at == "2024-02-01T00:00:00Z" for e in hotfix_entries)


@responses.activate
def test_fetch_page_body_supports_class_selectors():
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases/2024-4-1",
        body="""
        <html><body>
        <div class="release-notes">
          <p>Release notes loaded from a CSS class selector.</p>
        </div>
        </body></html>
        """,
        status=200,
    )
    body = _fetch_page_body("https://portswigger.net/burp/releases/2024-4-1")
    assert "CSS class selector" in body


@responses.activate
def test_collect_burpsuite_returns_empty_on_error():
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases",
        status=500,
    )
    entries = collect_burpsuite()
    assert entries == []


# --- Tests for the current (post-2025) URL format ---

NEW_BURPSUITE_HTML = """
<html><body>
<ul class="releases-list">
  <li><a href="/burp/releases/professional-community-2025-10-6">Professional / Community 2025.10.6</a></li>
  <li><a href="/burp/releases/professional-community-2025-7-2">Professional / Community 2025.7.2</a></li>
</ul>
</body></html>
"""

NEW_BURPSUITE_PAGE_HTML = """
<html><body>
<main>
<h2>Professional / Community 2025.10.6 Stable</h2>
<div class="release-meta">
  <span class="release-date">Monday, 24 November 2025 at 08:17 UTC</span>
</div>
<ul class="release-changelog">
  <li>Upgraded Burp's browser to Chromium 130.0.6723.117.</li>
  <li>Bug fixes and improvements.</li>
</ul>
</main>
</body></html>
"""

NEW_BURPSUITE_PAGE_HTML_2 = """
<html><body>
<main>
<h2>Professional / Community 2025.7.2 Stable</h2>
<div class="release-meta">
  <span class="release-date">Monday, 14 July 2025 at 10:00 UTC</span>
</div>
<ul class="release-changelog">
  <li>Bug fixes.</li>
</ul>
</main>
</body></html>
"""


def _add_new_burpsuite_page_mocks():
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases/professional-community-2025-10-6",
        body=NEW_BURPSUITE_PAGE_HTML,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases/professional-community-2025-7-2",
        body=NEW_BURPSUITE_PAGE_HTML_2,
        status=200,
    )


@responses.activate
def test_collect_burpsuite_new_url_format_returns_entries():
    """New professional-community URL format is collected correctly."""
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases",
        body=NEW_BURPSUITE_HTML,
        status=200,
    )
    _add_new_burpsuite_page_mocks()
    entries = collect_burpsuite()
    assert len(entries) >= 1
    assert entries[0].tool_id == "burpsuite"
    assert entries[0].tool_name == "Burp Suite"
    assert entries[0].url.startswith("https://portswigger.net/burp/releases/professional-community-")


@responses.activate
def test_collect_burpsuite_new_url_format_version_extracted():
    """Version is correctly extracted from the new URL path."""
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases",
        body=NEW_BURPSUITE_HTML,
        status=200,
    )
    _add_new_burpsuite_page_mocks()
    entries = collect_burpsuite()
    assert any(e.version == "2025.10.6" for e in entries)
    assert any(e.version == "2025.7.2" for e in entries)


@responses.activate
def test_collect_burpsuite_new_url_format_date_from_page():
    """Release date is extracted from the .release-date span on the individual page."""
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases",
        body=NEW_BURPSUITE_HTML,
        status=200,
    )
    _add_new_burpsuite_page_mocks()
    entries = collect_burpsuite()
    entry = next(e for e in entries if e.version == "2025.10.6")
    assert entry.published_at == "2025-11-24T00:00:00Z"


@responses.activate
def test_fetch_page_info_returns_body_and_date():
    """_fetch_page_info returns body text and parsed date."""
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases/professional-community-2025-10-6",
        body=NEW_BURPSUITE_PAGE_HTML,
        status=200,
    )
    body, date = _fetch_page_info("https://portswigger.net/burp/releases/professional-community-2025-10-6")
    assert "Chromium" in body or "Bug fixes" in body
    assert date == "2025-11-24T00:00:00Z"


@responses.activate
def test_fetch_page_body_supports_release_block_selector():
    """_fetch_page_body finds content in .release-block elements."""
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases/professional-community-2025-4-1",
        body="""
        <html><body>
        <div class="release-block">
          <p>Content from release-block selector.</p>
        </div>
        </body></html>
        """,
        status=200,
    )
    body = _fetch_page_body("https://portswigger.net/burp/releases/professional-community-2025-4-1")
    assert "release-block selector" in body
