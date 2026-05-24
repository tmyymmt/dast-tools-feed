"""tests/test_markdown_generator.py"""
import pytest

from scripts.markdown_generator import (
    _is_safe_href,
    generate_comparison_page,
    generate_comparison_page_ja,
    generate_tool_page,
    generate_tool_page_ja,
    render_html,
)
from scripts.models import ReleaseEntry

TOOL = {
    "id": "zap",
    "name": "OWASP ZAP",
    "type": "github",
    "repo": "zaproxy/zaproxy",
    "homepage": "https://www.zaproxy.org",
    "license": "Apache-2.0",
    "pricing": "Free",
    "description": "The world's most widely used open-source web application security scanner.",
    "description_ja": "世界で最も広く使われているオープンソースのWebアプリケーションセキュリティスキャナー。",
    "features": {
        "web_scanning": True,
        "api_scanning": True,
        "authenticated_scan": True,
        "active_scan": True,
        "passive_scan": True,
        "saas": False,
    },
}

ENTRIES = [
    ReleaseEntry(
        tool_id="zap",
        tool_name="OWASP ZAP",
        version="v2.15.0",
        published_at="2024-03-01T00:00:00Z",
        url="https://github.com/zaproxy/zaproxy/releases/tag/v2.15.0",
        summary="OWASP ZAP 2.15.0 released",
        body="## What's New\n- New scan rule added",
        category="feature",
    ),
    ReleaseEntry(
        tool_id="zap",
        tool_name="OWASP ZAP",
        version="v2.14.0",
        published_at="2024-02-01T00:00:00Z",
        url="https://github.com/zaproxy/zaproxy/releases/tag/v2.14.0",
        summary="OWASP ZAP 2.14.0 released",
        body="## Bug Fixes\n- Fixed memory leak",
        category="bugfix",
    ),
]


def test_generate_tool_page_contains_latest_version():
    result = generate_tool_page(TOOL, ENTRIES)
    assert "v2.15.0" in result


def test_generate_tool_page_contains_all_versions():
    result = generate_tool_page(TOOL, ENTRIES)
    assert "v2.15.0" in result
    assert "v2.14.0" in result


def test_generate_tool_page_contains_category():
    result = generate_tool_page(TOOL, ENTRIES)
    assert "`feature`" in result
    assert "`bugfix`" in result


def test_generate_tool_page_empty_entries():
    result = generate_tool_page(TOOL, [])
    assert "No release data available." in result
    assert "—" in result  # latest version shows —


def test_generate_tool_page_contains_features():
    result = generate_tool_page(TOOL, ENTRIES)
    assert "✅" in result
    assert "Apache-2.0" in result
    assert "Free" in result


def test_generate_tool_page_links_paid_to_pricing_page():
    tool = {
        **TOOL,
        "pricing": "Free (Community) / Paid (Pro/Enterprise)",
        "community_url": "https://portswigger.net/burp/communitydownload",
        "pricing_url": "https://portswigger.net/burp/pricing",
    }
    result = generate_tool_page(tool, ENTRIES)
    assert "[Free (Community)](https://portswigger.net/burp/communitydownload)" in result
    assert "[Paid](https://portswigger.net/burp/pricing)" in result


def test_generate_tool_page_ja_contains_japanese_headers():
    result = generate_tool_page_ja(TOOL, ENTRIES)
    assert "基本情報" in result
    assert "リリース履歴" in result
    assert "機能" in result
    assert "v2.15.0" in result


def test_generate_tool_page_ja_uses_description_ja():
    result = generate_tool_page_ja(TOOL, ENTRIES)
    assert "Webアプリケーションセキュリティスキャナー" in result


def test_generate_tool_page_ja_links_paid_to_pricing_page():
    tool = {
        **TOOL,
        "pricing": "Free (Community) / Paid (Pro/Enterprise)",
        "community_url": "https://portswigger.net/burp/communitydownload",
        "pricing_url": "https://portswigger.net/burp/pricing",
    }
    result = generate_tool_page_ja(tool, ENTRIES)
    assert "[Free (Community)](https://portswigger.net/burp/communitydownload)" in result
    assert "[Paid](https://portswigger.net/burp/pricing)" in result


def test_generate_comparison_page_contains_all_tools():
    tools = [TOOL, {**TOOL, "id": "nuclei", "name": "Nuclei"}]
    entries_by_tool = {"zap": ENTRIES, "nuclei": []}
    result = generate_comparison_page(tools, entries_by_tool)
    assert "OWASP ZAP" in result
    assert "Nuclei" in result
    assert "v2.15.0" in result


def test_generate_comparison_page_ja_contains_japanese_header():
    tools = [TOOL]
    result = generate_comparison_page_ja(tools, {"zap": ENTRIES})
    assert "DASTツール比較" in result
    assert "比較" in result


def test_generate_comparison_page_empty_entries_shows_dash():
    tools = [TOOL]
    result = generate_comparison_page(tools, {"zap": []})
    assert "—" in result


def test_generate_comparison_page_links_to_html():
    tools = [TOOL]
    result = generate_comparison_page(tools, {"zap": ENTRIES})
    assert "zap.html" in result
    assert ".md" not in result


def test_generate_comparison_page_ja_links_to_html():
    tools = [TOOL]
    result = generate_comparison_page_ja(tools, {"zap": ENTRIES})
    assert "zap_ja.html" in result
    assert ".md" not in result


def test_generate_comparison_page_links_paid_to_pricing_page():
    tool = {
        **TOOL,
        "id": "burpsuite",
        "name": "Burp Suite",
        "pricing": "Free (Community) / Paid (Pro/Enterprise)",
        "community_url": "https://portswigger.net/burp/communitydownload",
        "pricing_url": "https://portswigger.net/burp/pricing",
    }
    result = generate_comparison_page([tool], {"burpsuite": []})
    assert "[Free (Community)](https://portswigger.net/burp/communitydownload)" in result
    assert "[Paid](https://portswigger.net/burp/pricing)" in result


def test_generate_comparison_page_ja_links_paid_to_pricing_page():
    tool = {
        **TOOL,
        "id": "burpsuite",
        "name": "Burp Suite",
        "pricing": "Free (Community) / Paid (Pro/Enterprise)",
        "community_url": "https://portswigger.net/burp/communitydownload",
        "pricing_url": "https://portswigger.net/burp/pricing",
    }
    result = generate_comparison_page_ja([tool], {"burpsuite": []})
    assert "[Free (Community)](https://portswigger.net/burp/communitydownload)" in result
    assert "[Paid](https://portswigger.net/burp/pricing)" in result


def test_render_html_returns_html_document():
    result = render_html("Test Title", "# Hello\n\nWorld")
    assert "<!DOCTYPE html>" in result
    assert "<title>Test Title</title>" in result
    assert "<h1>Hello</h1>" in result


def test_render_html_lang_ja():
    result = render_html("テスト", "# こんにちは", lang="ja")
    assert 'lang="ja"' in result


def test_render_html_escapes_title_and_sanitizes_body():
    result = render_html(
        '<script>alert("title")</script>',
        '# Hello\n\n<script>alert("body")</script>\n\n[bad](javascript:alert(1))\n\n[bad2]( javascript:alert(2))',
    )
    assert "<script" not in result
    assert 'javascript:alert(1)' not in result
    assert 'javascript:alert(2)' not in result
    assert "<title>&lt;script&gt;alert(&quot;title&quot;)&lt;/script&gt;</title>" in result


def test_is_safe_href_rejects_control_char_prefix():
    assert _is_safe_href("\x00javascript:alert(1)") is False


@pytest.mark.parametrize("href", ["//example.com/path", "\\\\example.com\\path"])
def test_is_safe_href_rejects_protocol_relative_and_unc_like_paths(href):
    assert _is_safe_href(href) is False


def test_render_html_renders_table():
    md = "| A | B |\n|---|---|\n| 1 | 2 |"
    result = render_html("T", md)
    assert "<table>" in result


def test_render_html_contains_dark_mode():
    result = render_html("T", "# Hello")
    assert "prefers-color-scheme: dark" in result
