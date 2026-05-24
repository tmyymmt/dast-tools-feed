import logging
import re
from datetime import datetime, timezone
from typing import List

import requests
from bs4 import BeautifulSoup

from scripts.categorize import classify_release
from scripts.models import ReleaseEntry

logger = logging.getLogger(__name__)
BASE_URL = "https://portswigger.net"
INDEX_URL = f"{BASE_URL}/burp/releases"


def _fetch_page_body(url: str) -> str:
    """個別リリースページの本文テキストを取得する。失敗時は空文字を返す。"""
    try:
        resp = requests.get(url, timeout=30)
        if not resp.ok:
            logger.warning("Burp Suite page returned status %d: %s", resp.status_code, url)
            return ""
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        # Try to find the main content area
        for selector in ["article", "main", ".release-notes", ".content"]:
            content = soup.select_one(selector)
            if content:
                return content.get_text(separator="\n", strip=True)
        return ""
    except requests.RequestException as e:
        logger.warning("Failed to fetch Burp Suite page %s: %s", url, e)
        return ""


def collect_burpsuite() -> List[ReleaseEntry]:
    """Burp Suiteリリースノートページからリリース情報を収集する。

    エラー時は空リストを返す（部分失敗を許容）。
    """
    try:
        resp = requests.get(INDEX_URL, timeout=30)
        if not resp.ok:
            logger.warning("Burp Suite releases page returned status %d", resp.status_code)
            return []
    except requests.RequestException as e:
        logger.warning("Failed to fetch Burp Suite releases page: %s", e)
        return []

    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")
    entries = []

    # Parse release links from the releases index page
    for link in soup.find_all("a", href=re.compile(r"/burp/releases/\d")):
        href = link.get("href", "")
        url = f"{BASE_URL}{href}" if href.startswith("/") else href
        title = link.get_text(strip=True)
        if not title:
            continue

        # Extract version from href or title (e.g. "2024.1.1", "2024-1")
        version_match = re.search(r"(\d{4}[\.\-]\d+[\.\-]?\d*)", href)
        version = version_match.group(1).replace("-", ".") if version_match else title

        # Extract date from href or title
        date_match = re.search(r"/(\d{4})-(\d{1,2})-(\d{1,2})(?:/|$)", href)
        if date_match:
            published_at = (
                f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}T00:00:00Z"
            )
        else:
            title_date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", title)
            if title_date_match:
                published_at = (
                    f"{title_date_match.group(1)}-{title_date_match.group(2)}-{title_date_match.group(3)}T00:00:00Z"
                )
            else:
                # Try to extract year from version
                year_match = re.search(r"^(\d{4})", version)
                if year_match:
                    published_at = f"{year_match.group(1)}-01-01T00:00:00Z"
                else:
                    published_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        body = _fetch_page_body(url)

        entry = ReleaseEntry(
            tool_id="burpsuite",
            tool_name="Burp Suite",
            version=version,
            published_at=published_at,
            url=url,
            summary=title,
            body=body,
            category=classify_release(title, body, "scrape_burpsuite"),
        )
        entries.append(entry)

    return entries
