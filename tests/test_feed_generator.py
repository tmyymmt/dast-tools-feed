import json
import xml.etree.ElementTree as ET

from scripts.feed_generator import generate_atom, generate_json_feed, generate_rss
from scripts.models import ReleaseEntry


def make_entries():
    return [
        ReleaseEntry(
            tool_id="zap",
            tool_name="OWASP ZAP",
            version="v2.15.0",
            published_at="2024-01-15T10:00:00Z",
            url="https://github.com/zaproxy/zaproxy/releases/tag/v2.15.0",
            summary="OWASP ZAP 2.15.0",
            body="## Changes\n- feat: add new scan rule",
            category="feature",
        ),
        ReleaseEntry(
            tool_id="nuclei",
            tool_name="Nuclei",
            version="v3.2.0",
            published_at="2024-01-10T10:00:00Z",
            url="https://github.com/projectdiscovery/nuclei/releases/tag/v3.2.0",
            summary="Nuclei v3.2.0",
            body="## Bug Fixes\n- fix: false positive in template",
            category="bugfix",
        ),
    ]


def test_generate_rss_is_valid_xml():
    content = generate_rss(make_entries(), feed_title="DAST Tools Feed", feed_url="https://example.com/all.rss")
    root = ET.fromstring(content)
    assert root.tag == "rss"
    assert root.attrib.get("version") == "2.0"


def test_generate_rss_contains_entries():
    content = generate_rss(make_entries(), feed_title="DAST Tools Feed", feed_url="https://example.com/all.rss")
    assert b"OWASP ZAP 2.15.0" in content
    assert b"Nuclei v3.2.0" in content


def test_generate_rss_with_empty_entries():
    content = generate_rss([], feed_title="DAST Tools Feed", feed_url="https://example.com/all.rss")
    root = ET.fromstring(content)
    assert root.tag == "rss"


def test_generate_atom_is_valid_xml():
    content = generate_atom(make_entries(), feed_title="DAST Tools Feed", feed_url="https://example.com/all.atom")
    root = ET.fromstring(content)
    assert "feed" in root.tag


def test_generate_atom_contains_entries():
    content = generate_atom(make_entries(), feed_title="DAST Tools Feed", feed_url="https://example.com/all.atom")
    assert b"OWASP ZAP 2.15.0" in content


def test_generate_json_feed_is_valid_json():
    content = generate_json_feed(make_entries(), feed_title="DAST Tools Feed", feed_url="https://example.com/all.json")
    data = json.loads(content)
    assert data["version"] == "https://jsonfeed.org/version/1.1"
    assert data["title"] == "DAST Tools Feed"
    assert len(data["items"]) == 2


def test_generate_json_feed_contains_category_as_tag():
    content = generate_json_feed(make_entries(), feed_title="DAST Tools Feed", feed_url="https://example.com/all.json")
    data = json.loads(content)
    assert data["items"][0]["tags"] == ["feature"]
    assert data["items"][1]["tags"] == ["bugfix"]


def test_generate_json_feed_contains_tool_id():
    content = generate_json_feed(make_entries(), feed_title="DAST Tools Feed", feed_url="https://example.com/all.json")
    data = json.loads(content)
    assert data["items"][0]["_tool_id"] == "zap"
