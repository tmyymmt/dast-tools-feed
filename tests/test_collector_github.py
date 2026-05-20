import responses

from scripts.collectors.github import collect_github_releases

MOCK_RELEASES = [
    {
        "tag_name": "v2.15.0",
        "published_at": "2024-01-15T10:00:00Z",
        "html_url": "https://github.com/zaproxy/zaproxy/releases/tag/v2.15.0",
        "name": "OWASP ZAP 2.15.0",
        "body": "## Changes\n- feat: add new scan rule",
    },
    {
        "tag_name": "v2.14.0",
        "published_at": "2023-12-01T10:00:00Z",
        "html_url": "https://github.com/zaproxy/zaproxy/releases/tag/v2.14.0",
        "name": "OWASP ZAP 2.14.0",
        "body": "## Bug Fixes\n- fix: memory leak in spider",
    },
]


@responses.activate
def test_collect_github_releases_returns_entries():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/zaproxy/zaproxy/releases",
        json=MOCK_RELEASES,
        status=200,
    )
    entries = collect_github_releases(
        tool_id="zap",
        tool_name="OWASP ZAP",
        repo="zaproxy/zaproxy",
        github_token=None,
    )
    assert len(entries) == 2
    assert entries[0].version == "v2.15.0"
    assert entries[0].tool_id == "zap"
    assert entries[0].tool_name == "OWASP ZAP"
    assert entries[0].url == "https://github.com/zaproxy/zaproxy/releases/tag/v2.15.0"
    assert entries[0].category in ("feature", "bugfix", "security", "other", "announcement", "pricing")


@responses.activate
def test_collect_github_releases_returns_empty_on_404():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/unknown/notfound/releases",
        json={"message": "Not Found"},
        status=404,
    )
    entries = collect_github_releases(
        tool_id="notfound",
        tool_name="NotFound",
        repo="unknown/notfound",
        github_token=None,
    )
    assert entries == []


@responses.activate
def test_collect_github_releases_returns_empty_on_rate_limit():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/zaproxy/zaproxy/releases",
        status=429,
    )
    entries = collect_github_releases(
        tool_id="zap",
        tool_name="OWASP ZAP",
        repo="zaproxy/zaproxy",
        github_token=None,
    )
    assert entries == []


@responses.activate
def test_collect_github_releases_uses_token_in_header():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/zaproxy/zaproxy/releases",
        json=MOCK_RELEASES,
        status=200,
    )
    collect_github_releases(
        tool_id="zap",
        tool_name="OWASP ZAP",
        repo="zaproxy/zaproxy",
        github_token="test-token",
    )
    assert responses.calls[0].request.headers.get("Authorization") == "Bearer test-token"
