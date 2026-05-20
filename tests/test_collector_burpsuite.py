import responses

from scripts.collectors.burpsuite import collect_burpsuite

BURPSUITE_HTML = """
<html><body>
<ul class="releases-list">
  <li><a href="/burp/releases/2024-3-1">Burp Suite 2024.3.1</a></li>
  <li><a href="/burp/releases/2024-2-0">[Hotfix] Burp Suite 2024.2.0</a></li>
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
<h1>[Hotfix] Burp Suite 2024.2.0</h1>
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
        "https://portswigger.net/burp/releases/2024-2-0",
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
    assert "portswigger.net" in entries[0].url


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


@responses.activate
def test_collect_burpsuite_returns_empty_on_error():
    responses.add(
        responses.GET,
        "https://portswigger.net/burp/releases",
        status=500,
    )
    entries = collect_burpsuite()
    assert entries == []
