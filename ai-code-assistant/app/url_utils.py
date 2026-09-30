"""Helpers for fetching and cleaning URL content for the AI Code Assistant."""

from __future__ import annotations

import re
from html import unescape
from urllib.request import Request, urlopen


def extract_text_from_html(html: str) -> str:
    """Extract readable text from HTML by stripping tags and normalizing whitespace."""
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_url_content(url: str) -> str:
    """Fetch a URL and return cleaned visible text content."""
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=10) as response:
        html = response.read().decode("utf-8", errors="ignore")
    return extract_text_from_html(html)
